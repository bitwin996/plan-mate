from pyramid.view import view_config
from google.appengine.ext import ndb

from planmate.models.plan import Plan
from planmate.lib.helpers import to_dict_with_key,AuthenticationHelper


@view_config(route_name='api.plans.one.options', renderer='string')
def options(request): return

@view_config(route_name='api.plans.one.get', renderer='json')
def get(request):
  key_string = request.matchdict.get('id')
  key = ndb.Key(urlsafe = key_string)
  plan = key.get()
  return to_dict_with_key(plan)


"""
@view_config(route_name='api.plans.one.post', renderer='json')
def post(request):
  params = request.json_body
  print('PARAMS', params)
"""


@view_config(route_name='api.plans.one.attend-options', renderer='string')
def attend_options(request): return

@view_config(route_name='api.plans.one.attend', renderer='json')
def attend(request):
  key_string = request.matchdict.get('id')
  key = ndb.Key(urlsafe = key_string)
  plan = key.get()

  user_key = AuthenticationHelper.instance().get_user_key()
  plan.attendant_keys.append(user_key)
  plan.put()

  return to_dict_with_key(plan)

