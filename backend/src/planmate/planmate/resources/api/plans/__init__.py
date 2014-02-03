from planmate.resources import api
from planmate.resources.api.plans.attendants import PlanAttendantModel
from planmate.resources.api.plans.comments import PlanCommentModel
from planmate.resources.api.plans.schedules import PlanScheduleModel
from planmate.models.plan import Plan


class PlanEntity(api.Entity):
  _item_map = {
    'attendants': PlanAttendantModel,
    'comments': PlanCommentModel,
    'schedules': PlanScheduleModel
    }

  def __getitem__(self, name):
    name = str(name)

    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource


class PlanModel(api.Model):
  model = Plan

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanEntity(self.request, key=key, parent=self)

