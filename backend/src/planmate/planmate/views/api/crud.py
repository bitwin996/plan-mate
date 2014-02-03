from pyramid.httpexceptions import HTTPNotFound
from planmate.lib import mydb


def root(context, request):
  print('ROOT', context)
  return {'message':'root'}


def index(context, request):
  print('INDEX', context)
  query = context.get_model().query(ancestor=context.get_parent_key())
  entities = query.fetch(5)
  return mydb.list_to_dict_with_id(entities)


def show(context, request):
  print('SHOW', context.get_key())
  entity = context.get_key().get()
  return mydb.to_dict_with_id(entity)


def create(context, request):
  print('CREATE', context)

  from planmate.lib.helpers import AuthenticationHelper
  AuthenticationHelper.instance().debug_login()

  request_params = request.json_body if hasattr(request, 'json_body') else {}

  new_entity = context.get_new_entity()
  new_entity.populate(**request_params)
  new_entity.put()

  return mydb.to_dict_with_id(new_entity)


def update(context, request):
  print('UPDATE', context, hasattr(request, 'json_body'))
  request_params = request.json_body if hasattr(request, 'json_body') else {}

  key = context.get_key()
  entity = key.get()

  entity.populate(**request_params)
  entity.put()

  return mydb.to_dict_with_id(entity)


def destroy(context, request):
  print('DESTROY', context)

  key = context.get_key()
  entity = key.get()

  if not entity:
    raise HTTPNotFound()

  key.delete()

  return {}

