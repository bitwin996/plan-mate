from planmate.resources import api
from planmate.models.plan import Plan


class MyPlanEntityResource(api.EntityResource):
  def __getitem__(self, name):
    return KeyError


class MyPlanModelResource(api.ModelResource):
  model = Plan

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return MyPlanEntityResource(self.request, key=key, parent=self)

  def get_new_entity(self):
    return self._get_new_entity_with_current_user()

