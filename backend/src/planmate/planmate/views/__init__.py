from pyramid.httpexceptions import HTTPUnauthorized
from planmate.lib.helpers import AuthenticationHelper


def require_login(self):
  request_method = self.request.method
  if request_method != 'OPTIONS' and not AuthenticationHelper.instance().is_logged_in():
    raise HTTPUnauthorized()


