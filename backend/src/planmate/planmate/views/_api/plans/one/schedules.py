"""
from pyramid.view import view_config
from google.appengine.ext import ndb

from planmate.models.plan import PlanSchedule
from planmate.lib.helpers import list_to_dict_with_key


@view_config(route_name='api.plans.one.schedules.options', renderer='string')
def options(request): return

@view_config(route_name='api.plans.one.schedules.get', renderer='json')
def get(request):
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan_schedules = PlanSchedule.query(PlanSchedule.plan_key == plan_key).fetch()
  return list_to_dict_with_key(plan_schedules)
"""
