from planmate.resources import api
from planmate.models.plan import PlanComment
from planmate.lib.helpers import AuthenticationHelper
from planmate.lib.exceptions import AppNotLoginError


class PlanCommentEntityResource(api.EntityResource):
  def __getitem__(self, name):
    raise KeyError


class PlanCommentModelResource(api.ModelResource):
  model = PlanComment

  def __getitem__(self, unicode_id):
    key = self.generate_key(unicode_id, parent=self.get_parent_key())
    return PlanCommentEntityResource(self.request, key=key, parent=self)

  def get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    user_key = AuthenticationHelper.instance().get_user_key()
    if not user_key:
      raise AppNotLoginError()

    new_entity = model(user_key=user_key, parent=parent_key)
    return new_entity

  def get_query(self, *args, **options):
    query = self._get_query_with_ancestor(*args, **options)
    return query.order(-self.get_model().created)
