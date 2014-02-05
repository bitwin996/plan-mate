from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import AuthenticationHelper


class PlanAttendantEntity(api.Entity):
  def __getitem__(self, name):
    return KeyError


class PlanAttendantModel(api.Model):
  model = PlanAttendant

  def get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    user_key = AuthenticationHelper.instance().get_user_key()
    if not user_key:
      raise HTTPUnauthorized('Need to log in.')

    new_entity = model(user_key=user_key, parent=parent_key)
    return new_entity

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanAttendantEntity(self.request, key=key, parent=self)
