from google.appengine.ext import ndb
from planmate.lib import mydb


class User(mydb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()
  registered = ndb.BooleanProperty(default=False)

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


class Friendship(mydb.Model):
  user_key = ndb.KeyProperty(kind='User', required=True)

  @classmethod
  def get_friends(self, user_key):
    referers = self.__class__.query(parent=user_key).fetch()
    referees = self.__class__.query(self.user_key == user_key).fetch()

    referer_keys = [referer.user_key for referer in referers]
    referee_keys = [referee.key.parent for referee in referees]

    user_keys = list(set(referer_keys + referee_keys))
    users = ndb.get_multi(user_keys)

    return users


"""
# No. 1
class User:
  friend_keys = ndb.KeyProperty(repeat=True)


# No. 2
class User:

class Friendship:
  # parent = User
  # or
  #owner_key = ndb.KeyProperty(kind='User', required=True)
  referer_key = ndb.KeyProperty(kind='User', required=True)
  referee_key = ndb.KeyProperty(kind='User', required=True)


# No. 3
class User:
"""
