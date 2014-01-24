from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPNotFound

from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import list_to_dict_with_key


@view_config(route_name='api.plans.one.attentants.options', renderer='string')
def options(request): return

@view_config(route_name='api.plans.one.attentants.get', renderer='json')
def get(request):
  plan_key_string = request.matchdict.get('plan_key_string')
  plan_key = ndb.Key(urlsafe = plan_key_string)
  plan_schedules = PlanSchedule.query(PlanSchedule.plan_key == plan_key).fetch()
  return list_to_dict_with_key(plan_schedules)


@view_config(route_name='api.plans.one.attentants.post', renderer='json')
def post(request):
  plan_key_string = request.matchdict.get('plan_key')
  plan_key = ndb.Key(urlsafe = plan_key_string)

  if not plan_key: raise HTTPNotFound()

  user = AuthenticationHelper.instance().get_user()

  PlanAttendant(
    plan_key = 
    user = user,
  plan = Plan(
    user_key = user_key,
    place_name = params.get('place_name'),
    description = params.get('description')
    )
  plan_key = plan.put()

  return to_dict_with_key(plan)

