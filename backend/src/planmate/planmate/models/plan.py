from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from planmate.lib import mydb
from planmate.models.user import User


class Plan(ndb.Model):
  user_key = mydb.SafeKeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()
  parent_key = user_key

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  def _attendants_count(self):
    return PlanAttendant.query(PlanAttendant.plan_key == self.key).count()

  def _comments_count(self):
    return PlanComment.query(PlanComment.plan_key == self.key).count()


class PlanAttendant(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  user = ndb.StructuredProperty(User, required=True)
  parent_key = plan_key

class PlanSchedule(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  date = ndb.DateProperty(required=True)
  attendants = ndb.StructuredProperty(User, repeated=True)
  parent_key = plan_key

class PlanComment(ndb.Model):
  plan_key = mydb.SafeKeyProperty(kind='Plan', required=True)
  user = ndb.StructuredProperty(User, required=True)
  body = ndb.TextProperty(required=True)
  parent_key = plan_key

