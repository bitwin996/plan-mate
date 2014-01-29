from planmate.lib.resources import ModelResource,EntityResource,CurrentUserEntityResource
from planmate.models.user import User
from planmate.lib.helpers import AuthenticationHelper


class UserEntityResource(EntityResource): pass


class UserModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': User,
      'name': 'users',
      'entity_resource': UserEntityResource
      }
    _kwds.update(kwds)
    super(UserModelResource, self).__init__(*args, **_kwds)


class MyResource(CurrentUserEntityResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'name': 'me'
      }
    _kwds.update(kwds)
    super(MyResource, self).__init__(*args, **_kwds)
