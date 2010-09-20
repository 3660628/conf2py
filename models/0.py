response.title='Cooking Conference'
response.subtitle=SPAN('Bologna, Italy from 1 Aug 2021 until 7 Aug 2021')
from gluon.storage import Storage
from datetime import datetime

settings=Storage()
settings.production=False
settings.home_url='http://127.0.0.1:8000/%s/default' % request.application
settings.start_date=datetime(2010,12,8,12,00)
settings.end_date=datetime(2010,12,12,12,00)
settings.email_server='logging'
settings.email_sender='example@example.com'
settings.email_login=None
settings.mailing_list=None
try:
    settings.rpx_apikey=open('/Users/mdipierro/janrain_api_key.txt','r').read().strip()
    settings.rpx_domain='web2py'
except: pass

settings.authorize_net=('cnpdev4289', 'SR2P8g4jdEn7vFLQ', True) # sandbox
settings.googlemap_key='ABQIAAAAT5em2PdsvF3z5onQpCqv0RTpH3CbXHjuCVmaTc5MkkU4wO1RRhQHEAKj2S9L72lEMpvNxzLVfJt6cg' # 127.0.0.1
settings.calendar_url="http://www.google.com/calendar/embed?src=aDg4cDN0bDJmY285MjFkcGhiYnZjcDBrdGtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ"

settings.sections=('2010','2009','2008','2007')
settings.bibtex="""@InProceedings{hevw%(id)s,
     author    = {%(authors)s}
     title     = {%(title)s}
s     booktitle = {6th High End Visualization Workshop}
     year      = {%(section)s},
     publisher = {Unkown},
     url       = {http://example.com/%(file)s}}
"""

settings.categories=[
    ('MORE6','Ph.D. with >= 6 years of experience'),
    ('LESS6','Ph.D. with < 6 years of experiance'),
    ('GRAD','Graduate Students'),
    ('UGRD','Underaduate Students'),
    ('SENIOR','Senior Scientist'),
    ]


settings.rates = [
    ('001','Amateur ($200)', datetime(2008,1,1),datetime(2009,1,1),200),
    ('002','Amateur ($220)', datetime(2009,1,1),datetime(2010,1,1),220),
    ('003','Amateur ($240)', datetime(2010,1,1),datetime(2011,1,1),240),
    ('004','Chef ($300)', datetime(2008,1,1),datetime(2009,1,1),300),
    ('005','Chef ($330)', datetime(2009,1,1),datetime(2010,1,1),330),
    ('006','Chef ($360)', datetime(2010,1,1),datetime(2011,1,1),360),
    ]

### ('name','key') tutorials with same key overlap in time
settings.tutorials = [
    ('001','Pasta'),
    ('002','Pizza'),
    ('003','Meatballs'),
    ('004','Tiramisu'),
    ('005','Profiteroles'),
    ]

settings.pricing_policy=lambda rate, tutorials: 80*len(tutorials) + [x[4] for x in settings.rates if x[0]==rate][0]

settings.footer="powered by [[web2py http://web2py.com]]"

