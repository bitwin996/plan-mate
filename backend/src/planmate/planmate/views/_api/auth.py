"""
from pyramid.view import view_config

from planmate.models.user import User
from planmate.lib.helpers import AuthenticationHelper


@view_config(route_name='api.auth.status.options', request_method='OPTIONS', renderer='string')
def options(request): return


@view_config(route_name='api.auth.status.get', request_method='GET', renderer='json')
def get(request):
  is_logged_in = AuthenticationHelper.instance().is_logged_in()
  return {'is_logged_in': is_logged_in}
"""
