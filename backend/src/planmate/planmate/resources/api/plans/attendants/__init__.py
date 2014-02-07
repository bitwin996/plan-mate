from planmate.resources import api
from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import AuthenticationHelper


class PlanAttendantEntityResource(api.EntityResource):
  def __getitem__(self, name):
    raise KeyError


class PlanAttendantModelResource(api.ModelResource):
  model = PlanAttendant

  def __getitem__(self, unicode_id):
    key = self.generate_key(unicode_id, parent=self.get_parent_key())
    return PlanAttendantEntityResource(self.request, key=key, parent=self)

  def get_new_entity(self):
    return self._get_new_entity(add_parent=True, current_user_key='user_key')

