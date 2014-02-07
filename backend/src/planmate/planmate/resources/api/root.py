from planmate.resources import api
from planmate.resources.api.users import UserModelResource
from planmate.resources.api.plans import PlanModelResource
from planmate.resources.api.me import MyEntityResource
from planmate.resources.api.auth import AuthenticationResource
from planmate.lib.helpers import AuthenticationHelper


class RootResource(api.BaseResource):
  __parent__ = None
  __name__ = ''

  _item_map = {
    'me': MyEntityResource,
    'plans': PlanModelResource,
    'users': UserModelResource,
    'auth': AuthenticationResource
    }

  def __init__(self, *args, **options):
    super(RootResource, self).__init__(*args, **options)

    # session
    auth = AuthenticationHelper.instance()
    if not auth.has_session():
      auth.set_session(self.request.session)

    #TODO delete
    auth.debug_login()

  def __getitem__(self, name):
    cls = self.__class__._item_map[name]
    if not cls: raise KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource

