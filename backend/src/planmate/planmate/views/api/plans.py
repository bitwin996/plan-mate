from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPBadRequest

from planmate.lib import mydb
from planmate.models.plan import Plan,PlanAttendant,PlanScheduleAttendant
from planmate.resources.key_resources import PlanAttendantModelResource


from planmate.models.plan import PlanSchedule


# plan_attendants
def get_attendants(context, request):
  print('GET_ATTENDANTS', context, request)

  """TODO delete this parent test
  key = ndb.Key('Plan', 5778586438991872, 'PlanSchedule', 5690196012040192)
  print('KEY', key.get())

  parent_key = ndb.Key('Plan', 5778586438991872)
  print('PARENT_KEY', parent_key.get())

  query = PlanSchedule.query(ancestor=parent_key)
  plan_schedules = query.fetch()
  print('PLAN_SCHEDULES', plan_schedules)
  """

  if not isinstance(context, PlanAttendantModelResource):
    raise HTTPBadRequest()

  query = PlanAttendant.query(
    ancestor = context.get_parent_key())
  plan_attendants = query.fetch( projection = [PlanAttendant.user_key] )

  keys = []
  plan_attendants_attrs = {}
  for plan_attendant in plan_attendants:
    keys.append(plan_attendant.user_key)
    plan_attendants_attrs[plan_attendant.user_key.id()] = plan_attendant

  users = ndb.get_multi(keys)

  users_attrs = mydb.list_to_dict_with_id(users)

  user_values = []
  for user_attrs in users_attrs:
    user_attrs['plan_attendant_id'] = plan_attendants_attrs[user_attrs['id']].key.id()
    print('PLAN_ATTENDANT_ID', user_attrs['plan_attendant_id'])
    user_values.append(user_attrs)

  return user_values
