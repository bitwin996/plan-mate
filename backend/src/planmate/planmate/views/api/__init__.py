from google.appengine.ext import ndb

from pyramid.events import subscriber,NewRequest,BeforeRender
from pyramid.view import view_config

from pyramid.httpexceptions import *

from planmate.lib.helpers import AuthenticationHelper
from planmate.lib import mydb
from planmate.models.user import User
from planmate.models.plan import Plan,PlanAttendant,PlanScheduleAttendant


def options(context, request):
  pass


# auth debug
#@view_config(route_name='debug_login')
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


# api/auth
#@view_config(route_name='api.auth.status.options', request_method='OPTIONS', renderer='string')
#def options(request): return

#@view_config(route_name='api.auth.status.get', request_method='GET', renderer='json')
def auth_status(request):
  is_logged_in = AuthenticationHelper.instance().is_logged_in()
  return {'is_logged_in': is_logged_in}


# api/me/__init__
@subscriber(BeforeRender)
def check_login(event):
  request_method = event['request'].method
  if request_method != 'OPTIONS' and not AuthenticationHelper.instance().is_logged_in():
    raise HTTPUnauthorized()

