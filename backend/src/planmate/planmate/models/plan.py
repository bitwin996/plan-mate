from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from planmate.models.user import User


class Plan(ndb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()
  _parent_key_name = 'user_key'

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  def _attendants_count(self):
    return PlanAttendant.query(PlanAttendant.plan_key == self.key).count()

  def _comments_count(self):
    return PlanComment.query(PlanComment.plan_key == self.key).count()


class PlanAttendant(ndb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)
  _parent_key_name = 'plan_key'

class PlanComment(ndb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.StructuredProperty(User, required=True)
  body = ndb.TextProperty(required=True)
  _parent_key_name = 'plan_key'

class PlanSchedule(ndb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  date = ndb.DateProperty(required=True)
  #attendants = ndb.StructuredProperty(User, repeated=True)
  _parent_key_name = 'plan_key'

class PlanScheduleAttendant(ndb.Model):
  plan_schedule_key = ndb.KeyProperty(kind='PlanSchedule', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)
  _parent_key_name = 'plan_schedule_key'
