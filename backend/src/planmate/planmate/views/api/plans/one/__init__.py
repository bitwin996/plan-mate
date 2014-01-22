from pyramid.view import view_config
from google.appengine.ext import ndb

from planmate.models.plan import Plan
from planmate.lib.helpers import to_dict_with_key,AuthenticationHelper


@view_config(route_name='api.plans.one.options', renderer='string')
def options(request): return

@view_config(route_name='api.plans.one.get', renderer='json')
def get(request):
  print('PLANS-ONE', request.matchdict)
  plan_key_string = request.matchdict.get('plan_key_string')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan = plan_key.get()
  return to_dict_with_key(plan)

@view_config(route_name='api.plans.one.attend-options', renderer='string')
def attend_options(request): return

@view_config(route_name='api.plans.one.attend', renderer='json')
def attend(request):
  plan_key_string = request.matchdict.get('plan_key_string')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan = plan_key.get()

  user_key = AuthenticationHelper.instance().get_user_key()
  plan.attendant_keys.append(user_key)
  plan.put()

  return to_dict_with_key(plan)
