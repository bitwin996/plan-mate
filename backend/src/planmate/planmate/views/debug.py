from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from planmate.models.user import User,MyResource
from planmate.lib.helpers import *


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


def traversal(context, request):
  print('TRAVERSAL', context, request)

  if isinstance(context, ModelResource):
    entities = context.model.query().fetch()
    return list_to_dict_with_key(entities)

  elif isinstance(context, EntityResource) or isinstance(context, MyResource):
    entity = context.key.get()
    return to_dict_with_key(entity)

  else:
    NotImplemented


def options(context, request): return

