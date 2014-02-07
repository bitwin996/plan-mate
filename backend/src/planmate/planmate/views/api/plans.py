from google.appengine.ext import ndb
from planmate.views.api.crud import create


def index_plan_attendants(context, request):
  print('INDEX', context)

  query = context.get_query()
  plan_attendants = query.fetch()

  user_keys = [plan_attendant.user_key for plan_attendant in plan_attendants]
  users = ndb.get_multi(user_keys)

  json_body = []
  for plan_attendant in plan_attendants:
    for user in users:
      if plan_attendant.user_key == user.key:
        break

    pa = plan_attendant.to_json()
    u = user.to_json()
    pa['user'] = u
    json_body.append(pa)

  #json_body = [entity.to_json() for entity in entities]
  return json_body


def create_plan_attendants(context, request):
  print('CREATE PLAN_ATTENDANTS', context)

  create(context, request)
  json_body = index(context, request)

  return json_body
