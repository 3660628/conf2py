# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    return dict(page=db.plugin_wiki_page(slug='index'))

def attendees():
    orderby=db.auth_user.first_name|db.auth_user.last_name
    query=db.auth_user.plan_to_attend_workshop==True
    if not auth.user or not auth.user.manager:
        query=query&(db.auth_user.make_profile_public==True)
    attendees=db(query).select(orderby=orderby)
    return dict(attendees=attendees)

def agenda(): return dict()

def get(table,onerror='list_papers'):
    url=URL(onerror)
    try:
        id=int(request.args(0))
    except:
        redirect(url)
    record=table[id]
    if not record:
        redirect(url)
    return record

@auth.requires_login()
def register_other():
    db.auth_user.email.writable=db.auth_user.email.readable=True
    db.auth_user.registered_by.default=auth.user.id
    record=db.auth_user(request.args(0) or 0,registered_by=auth.user.id)
    if record and record.paid:
        db.auth_user.rate.writable=False
        db.auth_user.tutorials.writable=False    
    if record:
        form=crud.update(db.auth_user,
                         record,
                         message='User updated')
    else:
        form=crud.create(db.auth_user,
                         message='User created')
    users=db(db.auth_user.registered_by==auth.user.id).select()
    return dict(form=form,users=users)

@auth.requires_login()
def pay():
    if auth.user.paid or auth.user.payment_amount==0:
        session.flash='You have no balance'
        redirect(URL('index'))
    users=db(db.auth_user.registered_by==auth.user.id)\
        (db.auth_user.paid==False).select()
    form=SQLFORM.factory(Field('card_number',requires=IS_MATCH('\d{16}')),
                         Field('expiration',requires=IS_MATCH('\d\d/\d\d'),
                               comment="01/10"),
                         Field('first_name',default=auth.user.first_name),
                         Field('last_name',default=auth.user.last_name),
                         Field('cvv_code',requires=IS_MATCH('\d{3}'),comment='123'))
    message = ''    
    balance = auth.user.payment_amount+sum(x.payment_amount for x in users)
    items = UL(LI("$%(payment_amount)s for %(first_name)s %(last_name)s" % auth.user),*[LI("$%(payment_amount)s for %(first_name)s %(last_name)s" % user) for user in users])    
    if form.accepts(request.vars,session): 
        import uuid
        from gluon.contrib.AuthorizeNet import AIM
        try:
            payment = AIM(*settings.authorize_net)
            invoice=str(uuid.uuid4())
            expiration=form.vars.expiration.replace('/','20')
            payment.setTransaction(form.vars.card_number, 
                                   expiration,auth.user.payment_amount, 
                                   form.vars.cvv_code, 0.0, invoice)
            payment.setParameter('x_cust_id', str(auth.user.id))
            payment.setParameter('x_first_name', auth.user.first_name)
            payment.setParameter('x_last_name', auth.user.last_name)
            payment.setParameter('x_email', auth.user.email)
            payment.process()
            if payment.isApproved():
                message='Response Text: ', payment.response.ResponseText
                user=db.auth_user(auth.user.id)
                user.update_record(payment_datetime=request.now,
                                   paid=True,
                                   payment_invoice=invoice)
                auth.user.update(dict(payment_datetime=request.now,
                                      paid=True,
                                      payment_invoice=invoice))
                for user in users:
                    user.update_record(paid=True,
                                       payment_datetime=request.now)
                redirect(URL('payment_processed',
                             vars=dict(invoice=invoice,items=items.xml(),
                                       balance=balance)))
            elif payment.isDeclined():
                message='Your credit card was declined by your bank'
            elif payment.isError():
                message='Internal error'
        except AIM.AIMError, e:
            message="System Error"
            form.errors.card_number="Not accepted"
    return dict(form=form,balance=balance,message=message,users=users)

@auth.requires_login()
def payment_processed():
    return dict(request.vars)

def list_papers():
    papers=db(db.paper.status=='Accepted').select(orderby=db.paper.section|db.paper.authors)
    return dict(papers=papers)

def show_paper():
    paper=get(db.paper)
    return dict(papers=papers)

@auth.requires_login()
def manage_papers():
    db.paper.authors.default = '%(first_name)s %(last_name)s' % auth.user
    form=crud.create(db.paper,next='manage_paper/[id]')
    papers_all = db(db.paper.created_by!=auth.user_id).select() if editor else []
    papers_mine = db(db.paper.created_by==auth.user_id).select()
    papers_to_review =db(db.paper.id.belongs(db(db.assignment.reviewer==auth.user_id)._select(db.assignment.id))).select()
    return dict(papers_all=papers_all,papers_mine=papers_mine,papers_to_review=papers_to_review, form=form)

@auth.requires_login()
def manage_paper():
    paper = get(db.paper)
    author = paper.created_by==auth.user_id
    edit_form=crud.update(db.paper,paper,next=URL(r=request,args=paper.id)) if author else None
    reviewer = db(db.assignment.paper==paper.id)(db.assignment.reviewer==auth.user_id).count()
    add_reviewer_form,reviewers=None, None
    if author:
        types=AUTHOR_MESSAGE_TYPE
    elif editor:
        db.assignment.paper.default=paper.id
        add_reviewer_form=crud.create(db.assignment)
        reviewers=db(db.auth_user.id.belongs(db(db.assignment.paper==paper.id)\
                                                 ._select(db.assignment.reviewer))).select()
        types=EDITOR_MESSAGE_TYPE
        for reviewer in reviewers:
            types.append((reviewer.id+1000,'Primate Editor to reviewer %s' % reviewer.id))
    elif reviewer:
        types=REVIEWER_MESSAGE_TYPE
    else:
        redirect(URL('manage_papers'))        
    db.message.message_type.requires=IS_IN_SET(types,zero=None)
    def email_users(form):
        k = int(form.vars.message_type)
        if k==11:
            paper.update_record(file=form.vars.file,status=paper.status+' S:')
        elif k==23:
            paper.update_record(status='Accepted')
        elif k==24:
            paper.update_record(status='Conditionally Accepted')
        elif k==25:
            paper.update_record(status='Rejected')
        elif k == 32:
            paper.update_record(status=paper.status+'A')
        elif k == 33:
            paper.update_record(status=paper.status+'C')
        elif k == 34:
            paper.update_record(status=paper.status+'R')
        message=form.vars.body
        subject=MESSAGE_TYPES.get(k,'Private Communication')
        if k in AUTHOR_MESSAGE_POLICY:
            to=paper.created_by.email
        elif k in EDITOR_MESSAGE_POLICY:
            to=[x.email for x in db(db.auth_user.editor==True).select(db.auth_user.email)]
        elif k in REVIEWER_MESSAGE_POLICY:
            to=[x.email for x in db(db.auth_user.id.belongs(db(db.assignment.paper==paper.id)\
              ._select(db.assignment.reviewer))).select(db.auth_user.email)]            
        elif k>1000:
            to=db(db.auth_user.id==k-1000).select().first().email
        else:
            return
        mail.send(to=to,message=message,subject=subject)
    db.message.paper.default=paper.id
    form=crud.create(db.message,onaccept=email_users)
    messages=db(db.message.paper==paper.id).select(orderby=db.message.created_on)
    return dict(paper=paper,author=author,reviewer=reviewer,form=form,
                messages=messages,edit_form=edit_form,add_reviewer_form=add_reviewer_form,reviewers=reviewers)

def directions(): return dict()

@auth.requires(auth.user and auth.user.manager)
def slideshow():
    db.slideshow.id.represent=lambda id: A('[edit]',_href=URL(args=id))
    db.slideshow.image.represent=lambda x: IMG(_src=URL('download',args=x),_width="100px")
    form=crud.update(db.slideshow,request.args(0))
    images=SQLTABLE(db(db.slideshow.id>0).select(),headers='fieldname:capitalize')
    return dict(form=form,images=images)

@auth.requires(auth.user and auth.user.manager)
def manage_users():
    db.auth_user.registered_by.default=auth.user.id
    record=db.auth_user(request.args(0) or 0)
    form=crud.update(db.auth_user,
                     record,
                     message='User registered')
    users=plugin_wiki.widget('jqgrid',table='auth_user')
    return dict(form=form,users=users)    

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='profile' and auth.user and auth.user.paid:
        db.auth_user.rate.writable=False
        db.auth_user.tutorials.writable=False
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


