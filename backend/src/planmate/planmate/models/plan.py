from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from pyramid.httpexceptions import HTTPConflict

from planmate.lib import mydb
from planmate.models.user import User


class Plan(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  _current_user_key = 'user_key'

  @classmethod
  def get_parent_key_property(self):
    return self.user_key

  def get_current_user_key(self):
    return not not self.user_key

  def _attendants_count(self):
    return PlanAttendant.query(PlanAttendant.plan_key == self.key).count()

  def _comments_count(self):
    return PlanComment.query(PlanComment.plan_key == self.key).count()


class PlanAttendant(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  _current_user_key = 'user_key'

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanComment(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)
  body = ndb.TextProperty(required=True)

  _current_user_key = 'user_key'

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanSchedule(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  date = mydb.DateProperty(required=True)

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key


class PlanScheduleAttendant(mydb.Model):
  plan_schedule_key = ndb.KeyProperty(kind='PlanSchedule', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  _current_user_key = 'user_key'

  @classmethod
  def get_parent_key_property(self):
    return self.plan_schedule_key

  def _pre_put_hook(self):
    cls = self.__class__

    count = cls.query(
      cls.plan_schedule_key == self.plan_schedule_key,
      cls.user_key == self.user_key).count()

    if count != 0:
      raise HTTPConflict('You have already attended this date.')

