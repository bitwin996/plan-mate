from google.appengine.ext import ndb
from planmate.lib.helpers import underscorize
from planmate.views.api.crud import index_with_users, create as crud_create


def create_with_users_reponse(context, request):
  print('CREATE PLAN_ATTENDANTS', context)

  crud_create(context, request)
  response = index_with_users(context, request)

  return response
