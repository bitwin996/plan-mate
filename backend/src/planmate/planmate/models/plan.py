from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from pyramid.httpexceptions import HTTPBadRequest,HTTPConflict

from datetime import date

from planmate.lib import mydb
from planmate.models.user import User


class Plan(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  place_name = ndb.StringProperty(required=True)
  date = mydb.DateProperty()
  description = ndb.TextProperty()

  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  def _attendants_count(self):
    if self.is_saved():
      return PlanAttendant.query(ancestor=self.key).count()
    else:
      return 0

  def _comments_count(self):
    if self.is_saved():
      return PlanComment.query(ancestor=self.key).count()
    else:
      return 0

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_children_by_ancestor(key, PlanAttendant, PlanComment, PlanSchedule)


class PlanAttendant(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)

  def _pre_put_hook(self):
    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.is_saved():
      query = cls.query(
        cls.user_key == self.user_key,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count > 0:
        raise HTTPConflict('You have already joined this plan.')


class PlanComment(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)
  body = ndb.TextProperty(required=True)


class PlanSchedule(mydb.Model):
  date = mydb.DateProperty(required=True)
  attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())

  def _attendants_count(self):
    if self.is_saved():
      return PlanScheduleAttendant.query(ancestor=self.key).count()
    else:
      return 0

  def _pre_put_hook(self):
    if self.date < date.today():
      raise HTTPBadRequest('Date must be after today.')

    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.is_saved():
      query = cls.query(
        cls.date == self.date,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('Date has already registered.')

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_children_by_ancestor(key, PlanScheduleAttendant)


class PlanScheduleAttendant(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)

  def _pre_put_hook(self):
    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.is_saved():
      query = cls.query(
        cls.user_key == self.user_key,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('You have already availed this date.')

