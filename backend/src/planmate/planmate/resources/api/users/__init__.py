from planmate.resources import api
#from planmate.resources.api.plans import PlanModelResource
from planmate.models.user import User


class UserEntityResource(api.EntityResource):
  #_item_map = {
  #  'plans': PlanModelResource,
  #  }
  
  def __getitem__(self, name):
    raise KeyError

    #cls = self.__class__._item_map[name]
    #if not cls: return KeyError

    #resource = cls(self.request, name=name, parent=self)
    #return resource


class UserModelResource(api.ModelResource):
  model = User

  def __getitem__(self, unicode_id):
    key = self.generate_key(unicode_id, parent=None)
    return UserEntityResource(self.request, key=key, parent=self)

