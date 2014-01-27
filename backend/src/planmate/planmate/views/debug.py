from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from planmate.lib import mydb
from planmate.lib.helpers import *
from planmate.lib.resources import *
from planmate.models.user import User

from planmate.lib.helpers import var_dump


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


def options(context, request): return


def get(context, request):
  print('GET', context, request)

  if context.is_model():
    entities = context.query().fetch()
    return mydb.list_to_dict_with_id(entities)

  elif context.is_entity():
    entity = context.key.get()
    return mydb.to_dict_with_id(entity)

  else:
    NotImplemented


def post(context, request):
  print('POST', var_dump(context))
  if isinstance(context, ModelResource):
    key = context.put()
    return mydb.to_dict_with_id(key.get())

  else:
    NotImplemented


from planmate.models.plan import Plan
from planmate.lib.resources import PrefixResource,ModelResource


class ApiRoot(PrefixResource):
  __prefix__ = 'spi'

  def init_child_resources(self, child):
    plans = ModelResource(self.request, name='plans', model=Plan)
    child.add_model_resource(plans)


@view_config(context='planmate:views.debug.ApiRoot', name='', renderer='string')
@view_config(context='planmate:views.debug.PrefixResource', name='', renderer='string')
@view_config(context='planmate:resources.ModelResource', name='', renderer='string')
def root(context, request):
  return 'root'

@view_config(context='planmate:views.debug.ApiRoot', name='add', renderer='string')
@view_config(context='planmate:resources.ModelResource', name='add', renderer='string')
@view_config(context='planmate:resources.EntityResource', name='add', renderer='string')
def add(context, request):
  return 'add'

@view_config(context='planmate:resources.EntityResource', name='', renderer='string')
def show(context, request):
  return 'show'
