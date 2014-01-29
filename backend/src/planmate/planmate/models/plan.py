from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from planmate.lib import mydb
from planmate.models.user import User


class Plan(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  @classmethod
  def get_parent_key_property(self):
    return self.user_key

  def _attendants_count(self):
    return PlanAttendant.query(PlanAttendant.plan_key == self.key).count()

  def _comments_count(self):
    return PlanComment.query(PlanComment.plan_key == self.key).count()


class PlanAttendant(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanComment(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)
  body = ndb.TextProperty(required=True)

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanSchedule(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  date = ndb.DateProperty(required=True)

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanScheduleAttendant(mydb.Model):
  plan_schedule_key = ndb.KeyProperty(kind='PlanSchedule', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  @classmethod
  def get_parent_key_property(self):
    return self.plan_schedule_key

