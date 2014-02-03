from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.resources.api.plans.schedules.attendants import PlanScheduleAttendantModel
from planmate.models.plan import PlanSchedule
from planmate.lib.helpers import AuthenticationHelper


class PlanScheduleEntity(api.Entity):
  _item_map = {
    'attendants': PlanScheduleAttendantModel
    }

  def __getitem__(self, name):
    name = str(name)

    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource


class PlanScheduleModel(api.Model):
  model = PlanSchedule

  def get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    new_entity = model(parent=parent_key)
    return new_entity

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanScheduleEntity(self.request, key=key, parent=self)

