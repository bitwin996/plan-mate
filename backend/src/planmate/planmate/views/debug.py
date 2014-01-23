from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from planmate.models.user import User
from planmate.lib.helpers import AuthenticationHelper


@view_config(route_name='debug_login')
def debug_login(request):
  if request.matchdict.has_key('offset'):
    offset = int(request.matchdict['offset'])
  else:
    offset = 0

  user = User.query().get(offset=offset)
  if not user:
    return HTTPNotFound()

  user_key_string = user.key.urlsafe()
  AuthenticationHelper.instance().set_user_key_string(user_key_string)

  base_url = request.registry.settings['frontend.base_url']
  return HTTPFound(location = base_url)
