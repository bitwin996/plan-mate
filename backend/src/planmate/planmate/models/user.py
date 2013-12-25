from google.appengine.ext import ndb
from pyramid.config import Configurator

SESSION_KEY = 'user.key'

class User(ndb.Model):
    provider_type = ndb.StringProperty()
    provider_userid = ndb.IntegerProperty()
    name = ndb.StringProperty()

