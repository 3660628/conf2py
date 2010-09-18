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

CATEGORIES=(
    ('MORE6','Ph.D. with >= 6 years of experience'),
    ('LESS6','Ph.D. with < 6 years of experiance'),
    ('GRAD','Graduate Students'),
    ('UGRD','Underaduate Students'),
    ('SENIOR','Senior Scientist'),
    )

db.define_table('auth_user',
                Field('manager','boolean',writable=False,readable=False),
                Field('editor','boolean',writable=False,readable=False),
                Field('first_name', length=512,default=''),
                Field('last_name', length=512,default=''),
                Field('email', length=512,default='',requires=(IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email'))),
                Field('password', 'password', readable=False, label='Password', requires=[CRYPT(auth.settings.hmac_key)]),
                Field('category',requires=IS_IN_SET(CATEGORIES)),
                Field('web_page',requires=IS_EMPTY_OR(IS_URL()),comment='(optional)'),
                Field('mobile_number',default='',comment='(optional)'),
                Field('institution_name',default='',comment='(optional)'),
                Field('institution_address',default='',comment='(optional)'),
                Field('institution_city',default='',comment='(optional)'),
                Field('institution_country',requires=IS_IN_SET(COUNTRIES)),
                Field('plan_to_attend_workshop','boolean',default=True),
                Field('plan_to_submit_paper','boolean',default=True),
                Field('dietary_preferences',requires=IS_IN_SET(('None','Vegetarian','Vegan','Kosher'),zero=None)),
                Field('short_profile','text',default='',comment='(optional)'),
                Field('profile_picture','upload',comment='(optional)'),
                Field('make_profile_public','boolean',default=True),
                Field('arrival_date_time','datetime',default=settings.start_date),
                Field('departure_date_time','datetime',default=settings.end_date),
                Field('need_accommodation','boolean',default=True),
                Field('relative_traveling_with_you','integer',requires=IS_IN_SET(range(5),zero=None)),
                Field('subscribe_mailing_list','boolean',default=True),
                Field('latitude','double',readable=False,writable=False),
                Field('longitude','double',readable=False,writable=False),
                Field('registration_key', length=512,writable=False, readable=False,default=''),
                Field('reset_password_key', length=512,writable=False, readable=False, default='',
                      label=auth.messages.label_reset_password_key),
                format='%(first_name)s %(last_name)s',
                )

db.auth_user.manager.default = db(db.auth_user.id>0).count()==0

def lola(form):
    #if settings.production and form.vars.subscribe_mailing_list:
    #    sender=mail.settings.sender
    #    mail.settings.sender=form.vars.email
    #    mail.send(to='highendvizworkshop-subscribe@cct.lsu.edu',message='subscribe')
    #    mail.settings.sender=sender
    if form.vars.institution_city:
        form.vars.longitude, form.vars.latitude = geocode("%s %s" % (form.vars.institution_city, form.vars.institution_country))
auth.settings.register_onvalidation=lola
try: auth.settings.profile_onvalidation=lola
except: pass

manager = auth.user and auth.user.manager or auth.user_id==1
editor = True # auth.user and auth.user.editor or auth.user_id==1

mail=Mail()                                  # mailer
mail.settings.server='localhost:25'    # your SMTP server
mail.settings.sender='mdipierro@cs.depaul.edu'         # your email
#mail.settings.login='username:password'      # your credentials or None

auth.settings.hmac_key='<your secret key>'
auth.define_tables()                 # creates all needed tables

auth.settings.mailer=mail          # for user email verification
if settings.production:
    auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

# crud.settings.formstyle='table2cols'
