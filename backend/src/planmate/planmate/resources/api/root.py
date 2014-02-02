from planmate.resources import api
from planmate.resources.api.plans import PlanModel
from planmate.resources.api.me import MyEntity


class Root(api.Base):
  __parent__ = None
  __name__ = ''

  _item_map = {
    'plans': PlanModel,
    'me': MyEntity
    }

  def __getitem__(self, name):
    name = str(name)

    cls = self.__class__._item_map[name]
    if not cls: return KeyError

    resource = cls(self.request, name=name, parent=self)
    return resource
