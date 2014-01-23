from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from planmate.lib import mydb
from planmate.models.user import User


class Plan(ndb.Model):
  user_key = mydb.SafeKeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()
  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())

  def _attendants_count(self):
    return PlanAttendant.query(PlanAttendant.plan_key == self.key).count()

  #attendant_keys = mydb.SafeKeyProperty(kind='User', repeated=True)
  #comment_keys = mydb.SafeKeyProperty(kind='PlanComment', repeated=True)
  #date_keys = mydb.SafeKeyProperty(kind='PlanDate', repeated=True)

  #TODO move to lib.helpers
  #def _pre_put_hook(self):
  #  list_properties = ['attendant_keys', 'comment_keys', 'date_keys']
  #  for prop in list_properties:
  #    values = getattr(self, prop)
  #    if len(set(values)) is not len(values):
  #      raise InvalidPropertyError(prop + ' property contains duplicated values.')

class PlanAttendant(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  user = ndb.StructuredProperty(User, required=True)

class PlanSchedule(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  date = ndb.DateProperty(required=True)
  attendants = ndb.StructuredProperty(User, repeated=True)

class PlanComment(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  user = ndb.StructuredProperty(User, required=True)
  body = ndb.TextProperty(required=True)

