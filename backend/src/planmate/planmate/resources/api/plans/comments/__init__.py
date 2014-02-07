from pyramid.httpexceptions import HTTPUnauthorized

from planmate.resources import api
from planmate.models.plan import PlanComment
from planmate.lib.helpers import AuthenticationHelper


class PlanCommentEntityResource(api.EntityResource):
  def __getitem__(self, name):
    raise KeyError


class PlanCommentModelResource(api.ModelResource):
  model = PlanComment

  def get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    user_key = AuthenticationHelper.instance().get_user_key()
    if not user_key:
      raise HTTPUnauthorized('Need to log in.')

    new_entity = model(user_key=user_key, parent=parent_key)
    return new_entity

  def __getitem__(self, unicode_id):
    key = self.create_key(self.get_model(), unicode_id, self.get_parent_key())
    return PlanCommentEntityResource(self.request, key=key, parent=self)

