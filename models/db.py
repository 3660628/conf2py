# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)              # authentication/authorization
crud=Crud(globals(),db)              # for CRUD helpers using auth
service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc

COUNTRIES=['United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', "C&ocirc;te d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea','Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']


def Hidden(*a,**b):
    b['writable']=b['readable']=False
    return Field(*a,**b)

fields=[
    Hidden('manager','boolean',default=False),
    Hidden('editor','boolean',default=False),
    Hidden('registered','boolean',default=False),
    Hidden('paid','boolean',default=False),
    Hidden('payment_amount','double',default=0.0),
    Hidden('payment_datetime','datetime',default=request.now),
    Hidden('payment_invoice',default=''),
    Field('first_name', length=512,default='',comment='*'),
    Field('last_name', length=512,default='',comment='*'),
    Field('email', length=512,default='',comment='*',
          requires=(IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email'))),
    Field('password', 'password', readable=False, label='Password',
          requires=[CRYPT(auth.settings.hmac_key)]),
    Field('rate','string',comment='*',
          requires=IS_IN_SET([x[0:2] for x in settings.rates if x[2]<=request.now<=x[3]])),
    Field('category',requires=IS_IN_SET(settings.categories),comment='*'),
    Field('web_page',requires=IS_EMPTY_OR(IS_URL())),
    Field('mobile_number',default=''),
    Field('institution_name',default=''),
    Field('institution_address',default=''),
    Field('institution_city',default=''),
    Field('institution_country',requires=IS_IN_SET(COUNTRIES),comment='*'),
    Field('plan_to_attend_workshop','boolean',default=True),
    Field('plan_to_submit_paper','boolean',default=True),
    Field('dietary_preferences',
          requires=IS_IN_SET(('None','Vegetarian','Vegan','Kosher'),zero=None)),    
    Field('tutorials','list:string',
          requires=IS_IN_SET(settings.tutorials,multiple=True)),
    Field('short_profile','text',default=''),
    Field('profile_picture','upload'),
    Field('make_profile_public','boolean',default=True),
    Field('arrival_date_time','datetime',default=settings.start_date),
    Field('departure_date_time','datetime',default=settings.end_date),
    Field('need_accommodation','boolean',default=True),
    Field('relative_traveling_with_you','integer',
          requires=IS_IN_SET(range(5),zero=None)),
    Field('subscribe_mailing_list','boolean',default=True,
          readable=settings.mailing_list ,writable=settings.mailing_list),
    Hidden('latitude','double',requires=IS_FLOAT_IN_RANGE(-90,90)),
    Hidden('longitude','double', requires=IS_FLOAT_IN_RANGE(-180,180)),
    Field('discout_coupon','string'),
    Hidden('registered_by','integer',default=0), #nobody
    Hidden('registration_id', length=512,default=''),
    Hidden('registration_key', length=512,default=''),
    Hidden('reset_password_key', length=512,default='',
          label=auth.messages.label_reset_password_key),
    ]

db.define_table('auth_user',
                format='%(first_name)s %(last_name)s',
                *fields
                )

db.auth_user.manager.default = db(db.auth_user.id>0).count()==0
db.auth_user.id.represent=lambda id: A(id,_href=URL('default','manage_users',args=id))

def lola(form):
    form.vars.registered=True
    if settings.mailing_list and form.vars.subscribe_mailing_list:
        sender=mail.settings.sender
        mail.settings.sender=form.vars.email
        mail.send(to=settings.mailing_list,message='subscribe')
        mail.settings.sender=sender
    if form.vars.institution_country:
        form.vars.longitude, form.vars.latitude = geocode("%s %s" % (form.vars.institution_city, form.vars.institution_country))
    if not form.record or (form.record and not form.record.paid):
        amount=settings.pricing_policy(form.vars.rate,form.vars.tutorials)
        if form.vars.dicount_coupon:
            coupon=db.coupon(code=form.vars.dicount_coupon,used=False)
            if coupon and (coupon.used==False or coupon.used_by==form.vars.id):
                amount=min(amount-coupon.amount,0)
                coupon.update_record(used=True,
                                     used_by=form.vars.id,
                                     used_in=request.now)
            else:
                form.errors.discount_coupon='Invalid coupon code'
        form.vars.payment_amount=amount

auth.settings.register_onvalidation=lola
auth.settings.profile_onvalidation=lola
crud.settings.create_onvalidation.auth_user.append(lola)
crud.settings.update_onvalidation.auth_user.append(lola)


manager = auth.user and auth.user.manager or auth.user_id==1
editor = True # auth.user and auth.user.editor or auth.user_id==1

mail=Mail()
mail.settings.server=settings.email_server if settings.production else 'logging'
mail.settings.sender=settings.email_sender
#mail.settings.login=settings.email_login

auth.settings.hmac_key='<your secret key>'
auth.define_tables()                 
auth.settings.mailer=mail         
auth.settings.registration_requires_verification = settings.production
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

if settings.rpx_domain:
    from gluon.contrib.login_methods.rpx_account import RPXAccount
    auth.settings.actions_disabled=['register','change_password',
                                    'request_reset_password']
    auth.settings.login_form = RPXAccount(request, 
                                          api_key=settings.rpx_apikey,
                                          domain=settings.rpx_domain,
                                          url = settings.home_url+"/user/login")
    if request.function=='user' and request.args(0)=='register':
        if not auth.user_id: redirect(URL('user',args='login'))
        else: redirect(URL('user',args='profile'))
    if auth.user and not auth.user.registered:
        if not (request.function=='user' and request.args(0)=='profile'):
            redirect(URL('user',args='profile'))

