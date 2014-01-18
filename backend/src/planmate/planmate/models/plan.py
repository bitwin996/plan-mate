from google.appengine.ext import ndb
from planmate.lib import mydb

class Plan(ndb.Model):
    user_key = mydb.SafeKeyProperty(kind='User', required=True)
    place_name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()

    attendant_keys = mydb.SafeKeyProperty(kind='User', repeated=True)
    comment_keys = mydb.SafeKeyProperty(kind='PlanComment', repeated=True)
    date_keys = mydb.SafeKeyProperty(kind='PlanDate', repeated=True)
