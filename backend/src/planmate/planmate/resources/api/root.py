from planmate.resources import api
from planmate.resources.api.users import UserModelResource
from planmate.resources.api.me import MyEntityResource
from planmate.lib.helpers import AuthenticationHelper


class RootResource(api.BaseResource):
  __parent__ = None
  __name__ = ''

  _item_map = {
    'users': UserModelResource,
    'me': MyEntityResource
    }

  def __init__(self, *args, **options):
    super(self.__class__, self).__init__(*args, **options)

    auth = AuthenticationHelper.instance()
    if not auth.has_session():
      auth.set_session(self.request.session)
    auth.debug_login()

  def __getitem__(self, name):
    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource
