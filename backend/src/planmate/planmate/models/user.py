from google.appengine.ext import ndb

class User(ndb.Model):
  provider_type = ndb.StringProperty()
  provider_userid = ndb.IntegerProperty()
  name = ndb.StringProperty()
  profile_image_url = ndb.StringProperty()
