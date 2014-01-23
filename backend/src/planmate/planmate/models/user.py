from google.appengine.ext import ndb
#from planmate.lib import mydb


class User(ndb.Model):
    provider_type = ndb.StringProperty()
    provider_userid = ndb.IntegerProperty()
    name = ndb.StringProperty()
    profile_image_url = ndb.StringProperty()

    #plan_keys = mydb.SafeKeyProperty(kind='Plan', repeated=True)
