from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.resources.api.me.plans import MyPlanModel
from planmate.lib.helpers import AuthenticationHelper


class MyEntity(api.Base):
  _item_map = {
    'plans': MyPlanModel
    }

  def __init__(self, *args, **options):
    super(MyEntity, self).__init__(*args, **options)

    auth = AuthenticationHelper.instance()
    auth.set_session(self.request.session)
    #AuthenticationHelper.instance().debug_login()

    if not auth.is_logged_in():
      raise HTTPUnauthorized('Need logging in to continue.')

    self.key = auth.get_user_key()

  def __getitem__(self, name):
    name = str(name)

    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource

  def get_key(self):
    user_key = AuthenticationHelper.instance().get_user_key()
    return user_key
