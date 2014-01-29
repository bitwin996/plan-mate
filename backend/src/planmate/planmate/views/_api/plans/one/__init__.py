"""
from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.events import subscriber,NewRequest,ContextFound,BeforeRender
from pyramid.httpexceptions import HTTPNotFound

from planmate.models.plan import Plan,PlanSchedule
from planmate.lib.helpers import *


@view_config(route_name='api.plans.one.attend-options', renderer='string')
def attend_options(request): return

@view_config(route_name='api.plans.one.attend', renderer='json')
def attend(request):
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan = plan_key.get()

  user_key = AuthenticationHelper.instance().get_user_key()
  plan.attendant_keys.append(user_key)
  plan.put()

  return to_dict_with_key(plan)


@view_config(route_name='api.plans.one.options', renderer='string')
def options(request): return

@view_config(route_name='api.plans.one.get', renderer='json')
def get(request):
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan = plan_key.get()
  return to_dict_with_key(plan)


@view_config(route_name='api.plans.one.schedules.options', renderer='string')
def schedules_options(request): return

@view_config(route_name='api.plans.one.schedules.get', renderer='json')
def schedules_get(request):
  #plan_key_string = request.matchdict.get('plan_key')
  #plan_key = ndb.Key(urlsafe = plan_key_string)
  #if not plan_key: raise HTTPNotFound()

  plan_key = request.plan_key
  print('PLAN_KEY', plan_key)

  plan_schedules = PlanSchedule.query(PlanSchedule.plan_key == plan_key).fetch()
  return list_to_dict_with_key(plan_schedules)
"""
