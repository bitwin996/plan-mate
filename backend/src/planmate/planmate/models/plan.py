from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from pyramid.httpexceptions import HTTPBadRequest,HTTPConflict

from datetime import date

from planmate.lib import mydb
from planmate.models.user import User


class Plan(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  _parent_key = 'user_key'
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

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_child_entities(key)


class PlanAttendant(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  _parent_key = 'plan_key'
  _current_user_key = 'user_key'

  @classmethod
  def get_parent_key_property(self):
    return self.plan_key

  def _pre_put_hook(self):
    cls = self.__class__

    count = cls.query(
      cls.plan_key == self.plan_key,
      cls.user_key == self.user_key).count()

    if count != 0:
      raise HTTPConflict('You have already attended this date.')


class PlanComment(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)
  body = ndb.TextProperty(required=True)

  _parent_key = 'plan_key'
  _current_user_key = 'user_key'

  #@classmethod
  #def get_parent_key_property(self):
  #  return self.plan_key


class PlanSchedule(mydb.Model):
  plan_key = ndb.KeyProperty(kind='Plan', required=True)
  date = mydb.DateProperty(required=True)

  _parent_key = 'plan_key'

  #@classmethod
  #def get_parent_key_property(self):
  #  return self.plan_key

  def _pre_put_hook(self):
    print('DATETIME', self.date, date.today())
    if self.date < date.today():
      raise HTTPBadRequest('Date must be after today.')

    cls = self.__class__

    count = cls.query(
      cls.plan_key == self.plan_key,
      cls.date == self.date).count()

    if count != 0:
      raise HTTPConflict('Date has already registered.')

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_child_models(key)


class PlanScheduleAttendant(mydb.Model):
  plan_schedule_key = ndb.KeyProperty(kind='PlanSchedule', required=True)
  user_key = ndb.KeyProperty(kind='User', required=True)

  _parent_key = 'plan_schedule_key'
  _current_user_key = 'user_key'

  #@classmethod
  #def get_parent_key_property(self):
  #  return self.plan_schedule_key

  def _pre_put_hook(self):
    cls = self.__class__

    count = cls.query(
      cls.plan_schedule_key == self.plan_schedule_key,
      cls.user_key == self.user_key).count()

    if count != 0:
      raise HTTPConflict('You have already attended this date.')


User_child_models = [Plan]
Plan._child_models = [PlanAttendant, PlanSchedule, PlanComment]
PlanSchedule._child_models = [PlanScheduleAttendant]

