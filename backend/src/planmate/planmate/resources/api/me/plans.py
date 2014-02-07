from planmate.resources import api
from planmate.models.plan import Plan
from planmate.lib.helpers import AuthenticationHelper


class MyPlanEntityResource(api.EntityResource):
  def __getitem__(self, name):
    raise KeyError


class MyPlanModelResource(api.ModelResource):
  model = Plan

  def __getitem__(self, unicode_id):
    key = self.generate_key(unicode_id, parent=None)
    return MyPlanEntityResource(self.request, key=key, parent=self)

  def get_query(self, *args, **options):
    user_key = AuthenticationHelper.instance().get_user_key()
    list_args = list(args)
    list_args.append(Plan.user_key == user_key)
    return self._get_query(*list_args, **options)

  def get_new_entity(self):
    return self._get_new_entity(add_parent=False, current_user_key='user_key')

