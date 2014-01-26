from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from planmate.models.user import User,MyResource
from planmate.lib.helpers import *
from planmate.lib import mydb


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
  #print('GET', context, request)

  if context.is_model():
    entities = context.model.query().fetch()
    return mydb.list_to_dict_with_id(entities)

  elif context.is_entity():
    entity = context.key.get()
    return mydb.to_dict_with_id(entity)

  else:
    NotImplemented


def post(context, request):
  #print('POST', context, request)
  if isinstance(context, ModelResource):
    key = context.put()
    return mydb.to_dict_with_id(key.get())

  else:
    NotImplemented

