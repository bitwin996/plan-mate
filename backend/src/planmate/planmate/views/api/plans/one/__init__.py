from pyramid.view import view_config
from google.appengine.ext import ndb

from planmate.models.plan import Plan,PlanSchedule
from planmate.lib.helpers import to_dict_with_key,list_to_dict_with_key,AuthenticationHelper


#from pyramid.events import subscriber,NewRequest
#@subscriber(NewRequest)
#def initialize(event):
#  print('ONE_DICT', event.request.matchdict)


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
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan_schedules = PlanSchedule.query(PlanSchedule.plan_key == plan_key).fetch()
  return list_to_dict_with_key(plan_schedules)


@view_config(route_name='api.plans.one.attendants.options', renderer='string')
def attendants_options(request): return

@view_config(route_name='api.plans.one.attendants.get', renderer='json')
def attendants_get(request):
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan_schedules = PlanSchedule.query(PlanSchedule.plan_key == plan_key).fetch()

  attendant_keys = []
  attendants = []
  for plan_schedule in plan_schedules:
    #print('KEYS', plan_schedule.attendant_keys)
    attendant_keys += plan_schedule.attendant_keys
    attendants = User.query(key in attendant_keys).fetch()

  return list_to_dict_with_key(attendants)

