from planmate.models.plan import Plan

from pyramid.httpexceptions import HTTPUnauthorized
from google.appengine.ext.ndb.model import InvalidPropertyError
from pyramid.events import subscriber,NewRequest,BeforeRender

from planmate.lib.helpers import AuthenticationHelper
from planmate.lib import mydb
from planmate.lib.resources import PrefixResource,RootResource,ModelResource
from pyramid.view import view_config
from planmate.models.user import User


"""
class ApiRoot(PrefixResource):
  __prefix__ = 'api'

  def init_child_resources(self, child):
    plans = ModelResource(self.request, name='plans', model=Plan)
    child.add_model_resource(plans)

  def __init__(self, *args, **kwds):
    super(ApiRoot, self).__init__(args, kwds)

    #self.request.response.headers.update({
    #  'Access-Control-Allow-Origin': 'http://localhost:9000',
    #  'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type, X-HTTP-Method-Override',
    #  'Access-Control-Allow-Credentials': 'true',
    #  'Access-Control-Allow-Methods': '*',
    #  'Content-Type': 'application/json; charset=UTF-8'
    #  })
"""


"""
class ApiRoot(RootResource):
  def init_resources(self):
    plans = ModelResource(self.request, name='plans', model=Plan)
    self.add_model_resource(plans)
"""


@view_config(context=HTTPUnauthorized, renderer='json')
def http_unauthorized(exception, request):
  request.response.status = 401
  return {'message':'Please log in to continue.'}


@view_config(context=InvalidPropertyError, renderer='json')
def invalid_property_error(exception, request):
  #TODO
  request.response.status = 409
  message = exception.args[0] if exception.args else 'Some invalid parameters are posted.'
  return {'message':message}


def options(context, request): return


def root(context, request):
  return 'root'

def add(context, request):
  return 'add'

def show(context, request):
  return 'show'



def get(context, request):
  print('GET', context, request)

  if context.is_model():
    entities = context.query().fetch()
    return mydb.list_to_dict_with_id(entities)

  elif context.is_entity():
    entity = context.get_entity()
    return mydb.to_dict_with_id(entity)

  else:
    NotImplemented



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

