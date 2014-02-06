from planmate.resources import api
from planmate.resources.api.plans import PlanModelResource
from planmate.resources.api.me import MyEntityResource


class RootResource(api.BaseResource):
  __parent__ = None
  __name__ = ''

  _item_map = {
    'plans': PlanModelResource,
    'me': MyEntityResource
    }

  def __getitem__(self, name):
    name = str(name)

    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource
