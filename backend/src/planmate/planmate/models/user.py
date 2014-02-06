from google.appengine.ext import ndb
from planmate.lib import mydb


class User(mydb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()

  def _pre_put_hook(self):
    cls = self.__class__

    # Unique constraint in creating a new entity
    if not self.key.id():
      query = cls.query(
        cls.provider_type == self.provider_type,
        cls.provider_userid == self.provider_userid
        )
      count = query.count()

      if count != 0:
        raise HTTPConflict('You have already attended this date.')

  #TODO
  #@classmethod
  #def _pre_delete_hook(self, key):
  #  self._delete_child_models(key)
