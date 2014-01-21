from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError
from planmate.lib import mydb

class Plan(ndb.Model):
  user_key = mydb.SafeKeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()

  attendant_keys = mydb.SafeKeyProperty(kind='User', repeated=True)
  comment_keys = mydb.SafeKeyProperty(kind='PlanComment', repeated=True)
  date_keys = mydb.SafeKeyProperty(kind='PlanDate', repeated=True)

  def _pre_put_hook(self):
    list_properties = ['attendant_keys', 'comment_keys', 'date_keys']
    for prop in list_properties:
      values = getattr(self, prop)
      if len(set(values)) is not len(values):
        raise InvalidPropertyError(prop + ' property contains duplicated values.')
