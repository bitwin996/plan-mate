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
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanEntityResource(self.request, key=key, parent=self)

