from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import AuthenticationHelper


class PlanAttendantEntityResource(api.EntityResource):
  def __getitem__(self, name):
    raise KeyError


class PlanAttendantModelResource(api.ModelResource):
  model = PlanAttendant

  def get_new_entity(self):
    return self._get_new_entity_with_current_user_key()

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanAttendantEntityResource(self.request, key=key, parent=self)

