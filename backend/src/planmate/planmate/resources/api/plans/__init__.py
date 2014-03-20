from planmate.resources import api
from planmate.resources.api.plans.attendants import PlanAttendantModelResource
from planmate.resources.api.plans.comments import PlanCommentModelResource
from planmate.resources.api.plans.schedules import PlanScheduleModelResource
from planmate.models.plan import Plan


class PlanEntityResource(api.EntityResource):
  _item_map = {
    'attendants': PlanAttendantModelResource,
    'comments': PlanCommentModelResource,
    'schedules': PlanScheduleModelResource
    }
  
  def __getitem__(self, name):
    cls = self.__class__._item_map[name]
    if not cls: raise KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource


class PlanModelResource(api.ModelResource):
  model = Plan

  def __getitem__(self, unicode_id):
    key = self.generate_key(unicode_id)
    return PlanEntityResource(self.request, key=key, parent=self)

  def get_new_entity(self):
    return self._get_new_entity(add_parent=False, current_user_key='user_key')

