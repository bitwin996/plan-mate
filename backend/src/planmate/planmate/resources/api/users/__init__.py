from planmate.resources import api
from planmate.resources.api.users.plans import PlanModelResource
from planmate.models.user import User


class UserEntityResource(api.EntityResource):
  _item_map = {
    'plans': PlanModelResource,
    }
  
  def __getitem__(self, name):
    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource


class UserModelResource(api.ModelResource):
  model = User

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id) #, self.get_parent_key())
    return UserEntityResource(self.request, key=key, parent=self)

