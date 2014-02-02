from google.appengine.ext import ndb
from planmate.lib import mydb


class User(mydb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()

  @classmethod
  def _pre_delete_hook(self, key):
    self._delete_child_models(key)
