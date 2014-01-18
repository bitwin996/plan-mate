from google.appengine.ext import ndb
from planmate.lib import mydb

class PlanComment(ndb.Model):
    user_key = mydb.SafeKeyProperty(kind='User', required=True)
    body = ndb.StringProperty(required=True)

