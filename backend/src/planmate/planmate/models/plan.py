from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import InvalidPropertyError

from pyramid.httpexceptions import HTTPBadRequest,HTTPConflict

from datetime import date

from planmate.lib import mydb
from planmate.models.user import User


class Plan(mydb.Model):
  #user_key = ndb.KeyProperty(kind='User', required=True)
  user = ndb.StructuredProperty(User, required=True)
  place_name = ndb.StringProperty(required=True)
  description = ndb.TextProperty()

  attendants = ndb.StructuredProperty(User, repeated=True)

  #attendants_count = ndb.ComputedProperty(lambda self: self._attendants_count())
  comments_count = ndb.ComputedProperty(lambda self: self._comments_count())

  #def _attendants_count(self):
  #  if self.key.id():
  #    return PlanAttendant.query(ancestor=self.key).count()
  #  else:
  #    return 0

  def _comments_count(self):
    if self.key.id():
      return PlanComment.query(ancestor=self.key).count()
    else:
      return 0

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_child_entities(key)


class PlanAttendant(mydb.Model):
  #user_key = ndb.KeyProperty(kind='User', required=True)
  user = ndb.StructuredProperty(User, required=True)

  #_current_user_key = 'user_key'

  def _pre_put_hook(self):
    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.key.id():
      query = cls.query(
        cls.user_key == self.user_key,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('You have already attended this plan.')


class PlanComment(mydb.Model):
  #user_key = ndb.KeyProperty(kind='User', required=True)
  user = ndb.StructuredProperty(User, required=True)
  body = ndb.TextProperty(required=True)

  #_current_user_key = 'user_key'


class PlanSchedule(mydb.Model):
  date = mydb.DateProperty(required=True)
  attendants = ndb.StructuredProperty(User, repeated=True)

  def _pre_put_hook(self):
    if self.date < date.today():
      raise HTTPBadRequest('Date must be after today.')

    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.key.id():
      query = cls.query(
        cls.date == self.date,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('Date has already registered.')

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_child_models(key)


class PlanScheduleAttendant(mydb.Model):
  #user_key = ndb.KeyProperty(kind='User', required=True)
  user = ndb.LocalStructuredProperty(User, required=True)

  #_current_user_key = 'user_key'

  def _pre_put_hook(self):
    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.key.id():
      query = cls.query(
        cls.user_key == self.user_key,
        ancestor = self.key.parent()
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('You have already attended this date.')

