from planmate.resources import api
from planmate.resources.api.me.plans import MyPlanModelResource
from planmate.lib.helpers import AuthenticationHelper
from planmate.lib.exceptions import AppNotLoginError


class MyEntityResource(api.BaseResource):
  _item_map = {
    'plans': MyPlanModelResource
    }

  def __init__(self, *args, **options):
    super(MyEntityResource, self).__init__(*args, **options)

    if not AuthenticationHelper.instance().is_logged_in():
      raise AppNotLoginError()

    self.key = self.get_key()

  def __getitem__(self, name):
    cls = self.__class__._item_map[name]
    if not cls: raise KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource

  def get_key(self):
    user_key = AuthenticationHelper.instance().get_user_key()
    return user_key
