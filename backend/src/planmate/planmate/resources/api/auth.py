from planmate.resources import api


class AuthenticationResource(api.BaseResource):
  def __getitem__(self, name):
    raise KeyError
