from pyramid.events import subscriber,NewRequest,BeforeRender
from pyramid.view import view_config

from pyramid.httpexceptions import *

from planmate.lib.helpers import AuthenticationHelper
from planmate.lib import mydb
from planmate.lib.resources import PrefixResource,RootResource,ModelResource
from planmate.models.user import User
from planmate.models.plan import Plan,PlanAttendant,PlanScheduleAttendant
from planmate.resources.plan import PlanScheduleAttendantModelResource


def options(context, request): return


def get(context, request):
  print('GET', context, request)

  if context.is_model():
    entities = context.query().fetch()
    return mydb.list_to_dict_with_id(entities)

  elif context.is_entity():
    entity = context.get_entity()
    return mydb.to_dict_with_id(entity)

  raise HTTPNotFound()


def post(context, request):
  print('POST', context, request)

  if context.is_model():
    if hasattr(request, 'json_body'):
      params = request.json_body
      key = context.put(attributes=params)
    else:
      key = context.put()

    return mydb.to_dict_with_id(key.get())

  else:
    raise HTTPMethodNotAllowed('You cannnot use the action at this URL.')


def delete(context, request):
  print('DELETE', context, request)

  if context.is_entity():
    if context.exists():
      context.delete()
      request.response.status = 200
      return {'message':'Success to delete the data.'}

    else:
      raise HTTPNotFound('You do not attend yet.')

  else:
    raise HTTPMethodNotAllowed('You cannnot use the action at this URL.')


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

