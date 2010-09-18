response.title='6th High End Visualization Workshop'
response.subtitle=SPAN('8-12 Dec 2010 ',A('Obergurgl, Austria',_href='http://www.uibk.ac.at/obergurgl/'),' ')
from gluon.storage import Storage
from datetime import datetime
settings=Storage()
settings.production=True
settings.start_date=datetime(2010,12,8,12,00)
settings.end_date=datetime(2010,12,12,12,00)
settings.googlemap_key='ABQIAAAAT5em2PdsvF3z5onQpCqv0RTpH3CbXHjuCVmaTc5MkkU4wO1RRhQHEAKj2S9L72lEMpvNxzLVfJt6cg' # 127.0.0.1
settings.googlemap_key='ABQIAAAAT5em2PdsvF3z5onQpCqv0RQKjFa1yJagLmzGcZ4UA6Ce9BDiWhSxvi4hSIQsWixy4LcFJtTrQTFuhg' # web2py.com
settings.googlemap_key='ABQIAAAAT5em2PdsvF3z5onQpCqv0RQPCUEzYgiop56CdyBwu8qVi8fMhxQiCxk_q8hn8KuACpXbUW0O92B1gQ' # http://vizworkshop.cct.lsu.edu
settings.sections=('2010','2009','2008','2007')
settings.bibtex="""@InProceedings{hevw%(id)s,
     author    = {%(authors)s}
     title     = {%(title)s}
     booktitle = {6th High End Visualization Workshop}
     year      = {%(section)s},
     publisher = {Unkown},
     url       = {http://example.com/%(file)s}}
"""
