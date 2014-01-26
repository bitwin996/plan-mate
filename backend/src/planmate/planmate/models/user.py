from google.appengine.ext import ndb

from planmate.lib.helpers import EntityResource,BaseEntityResource,AuthenticationHelper


class User(ndb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()


class MyResource(BaseEntityResource):
  def __init__(self, *args, **kwds):
    super(MyResource, self).__init__(args, kwds)
    self.__name__ = kwds.get('name')

    AuthenticationHelper.instance().set_session(self.request.session)
    key = AuthenticationHelper.instance().get_user_key()
    self.key = key

  def __getitem__(self, name):
    model_resource = self.get_model_resource(name)
    if not model_resource: raise KeyError
    return model_resource
