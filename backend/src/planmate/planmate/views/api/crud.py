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
  response = {context.__name__: json_body}
  return response


def show(context, request):
  print('SHOW', context, request)
  key = context.get_key()
  entity = key.get()
  name = mydb.underscorize(key.kind())

  json_body = entity.to_json()
  response = {name: json_body}
  return response


def create(context, request):
  print('CREATE', context)

  new_entity = context.get_new_entity()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  new_entity.set_prop_values(**post_params)
  new_entity.put()

  json_body = new_entity.to_json()
  response = {context.__name__: json_body}
  return response


def update(context, request):
  print('UPDATE', context, hasattr(request, 'json_body'))

  key = context.get_key()
  entity = key.get()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  entity.set_prop_values(**post_params)
  entity.put()

  json_body = entity.to_json()
  response = {context.__name__: json_body}
  return response


def destroy(context, request):
  print('DESTROY', context)

  key = context.get_key()
  entity = key.get()

  if not entity:
    raise HTTPNotFound()

  key.delete()

  return {}

