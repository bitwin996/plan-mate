from planmate.resources import api
from planmate.models.plan import Plan


class MyPlanEntity(api.Entity):
  def __getitem__(self, name):
    return KeyError


class MyPlanModel(api.Model):
  model = Plan

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return MyPlanEntity(self.request, key=key, parent=self)

