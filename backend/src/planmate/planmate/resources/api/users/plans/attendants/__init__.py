from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import AuthenticationHelper


class PlanAttendantEntityResource(api.EntityResource):
  def __getitem__(self, name):
    return KeyError


class PlanAttendantModelResource(api.ModelResource):
  model = PlanAttendant

  def get_new_entity(self):
    return self._get_new_entity_with_current_user_key()
    """
    new_entity = super(PlanAttendantModelResource, self).get_new_entity()

    model = self.get_model()
    parent_key = self.get_parent_key()

    current_user = AuthenticationHelper.instance().get_user()
    if not user_key:
      raise HTTPUnauthorized('Need to log in.')

    #new_entity = model(user_key=user_key, parent=parent_key)

    new_entity.user = current_user
    return new_entity
    """

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanAttendantEntityResource(self.request, key=key, parent=self)

