from google.appengine.ext import ndb
from planmate.views.api.crud import create as crud_create


def index(context, request):
  print('INDEX', context)

  query = context.get_query()
  plan_attendants = query.fetch()

  user_keys = [plan_attendant.user_key for plan_attendant in plan_attendants]
  users = ndb.get_multi(user_keys)

  plan_attendants_json = [plan_attendant.to_json() for plan_attendant in plan_attendants]
  users_json = [user.to_json() for user in users]
  return {'plan_attendants': plan_attendants_json, 'users': users_json}


def create(context, request):
  print('CREATE PLAN_ATTENDANTS', context)

  crud_create(context, request)
  response = index(context, request)

  return response
