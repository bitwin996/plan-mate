from pyramid.httpexceptions import HTTPNotFound
from google.appengine.ext import ndb
from planmate.lib import mydb
from planmate.lib.helpers import underscorize,pluralize


def root(context, request):
  print('ROOT', context)
  return {'message':'root'}


def index(context, request):
  print('INDEX', context)

  query = context.get_query()
  entities = query.fetch()

  json_body = [entity.to_json() for entity in entities]
  name = pluralize(underscorize(context.get_model().__name__))
  response = {name: json_body}
  return response


def index_with_users(context, request):
  print('INDEX WITH USERS', context)

  query = context.get_query()
  entities = query.fetch()
  entities_json = [entity.to_json() for entity in entities]

  user_keys = [entity.user_key for entity in entities]
  users = ndb.get_multi(user_keys)
  users_json = [user.to_json() for user in users]

  name = pluralize(underscorize(context.get_model().__name__))
  return {name: entities_json, 'users': users_json}


def show(context, request):
  print('SHOW', context, request)
  key = context.get_key()
  entity = key.get()

  json_body = entity.to_json()
  name = underscorize(key.kind())
  response = {name: json_body}
  return response


def _create(context, request):
  new_entity = context.get_new_entity()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  print 'POST_PARAMS', post_params

  new_entity.set_prop_values(**post_params)
  new_entity.put()

  return new_entity

def create(context, request):
  print 'CREATE', context
  new_entity = _create(context, request)

  json_body = new_entity.to_json()
  name = underscorize(context.__name__)
  response = {name: json_body}
  return response


def create_of_index_response(context, request):
  _create(context, request)
  response = index(context, request)
  return response


def create_with_users(context, request):
  print 'CREATE PLAN_ATTENDANTS', context

  _create(context, request)
  response = index_with_users(context, request)
  return response


def update(context, request):
  print('UPDATE', context, hasattr(request, 'json_body'))

  key = context.get_key()
  entity = key.get()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  print 'POST_PARAMS', post_params
  entity.set_prop_values(**post_params)
  entity.put()

  json_body = entity.to_json()
  name = underscorize(context.__name__)
  response = {name: json_body}
  return response


def destroy(context, request):
  print('DESTROY', context)

  key = context.get_key()
  entity = key.get()

  if not entity:
    raise HTTPNotFound()

  key.delete()

  return {}

