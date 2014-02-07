from pyramid.httpexceptions import HTTPNotFound
from planmate.lib import mydb


def root(context, request):
  print('ROOT', context)
  return {'message':'root'}


def index(context, request):
  print('INDEX', context)

  query = context.get_query()
  entities = query.fetch()

  json_body = [entity.to_json() for entity in entities]
  return json_body


def show(context, request):
  print('SHOW', context.get_key())
  key = context.get_key()
  entity = key.get()

  json_body = entity.to_json()
  #print('JSON', json_body)
  return json_body


def create(context, request):
  print('CREATE', context)

  new_entity = context.get_new_entity()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  print 'PARAMS', post_params
  new_entity.set_prop_values(**post_params)
  new_entity.put()

  json_body = new_entity.to_json()
  return json_body


def update(context, request):
  print('UPDATE', context, hasattr(request, 'json_body'))

  key = context.get_key()
  entity = key.get()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  entity.set_prop_values(**post_params)
  entity.put()

  json_body = entity.to_json()
  return json_body


def destroy(context, request):
  print('DESTROY', context)

  key = context.get_key()
  entity = key.get()

  if not entity:
    raise HTTPNotFound()

  key.delete()

  return {}

