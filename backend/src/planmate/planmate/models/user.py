from google.appengine.ext import ndb

from planmate.lib.helpers import EntityResource,BaseResource,AuthenticationHelper


class User(ndb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()


class MyResource(BaseResource):
  def __init__(self, *args, **kwds):
    super(MyResource, self).__init__(args, kwds)
    self.__name__ = kwds.get('name')

    AuthenticationHelper.instance().set_session(self.request.session)
    key = AuthenticationHelper.instance().get_user_key()
    self.key = key

  def __getitem__(self, name):
    for resource in self.resources:
      if resource.__name__ == name:
        return resource
    raise KeyError
