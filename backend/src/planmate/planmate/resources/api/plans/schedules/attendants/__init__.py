from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.models.plan import PlanScheduleAttendant
from planmate.lib.helpers import AuthenticationHelper


class PlanScheduleAttendantEntity(api.Entity):
  def __getitem__(self, name):
    return KeyError


class PlanScheduleAttendantModel(api.Model):
  model = PlanScheduleAttendant

  def get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    user_key = AuthenticationHelper.instance().get_user_key()
    if not user_key:
      raise HTTPUnauthorized('Need to log in.')

    new_entity = model(parent=parent_key, user_key=user_key)
    return new_entity

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanScheduleAttendantEntity(self.request, key=key, parent=self)
