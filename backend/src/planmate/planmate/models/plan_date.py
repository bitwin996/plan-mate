from google.appengine.ext import ndb
from planmate.lib import mydb

class PlanDate(ndb.Model):
    date = ndb.DateProperty(required=True)
    available_user_keys = mydb.SafeKeyProperty(kind='User', repeated=True)
    unavailable_user_keys = mydb.SafeKeyProperty(kind='User', repeated=True)

