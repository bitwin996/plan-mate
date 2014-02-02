from google.appengine.ext import ndb
from planmate.lib import mydb

from planmate.models.plan import Plan,PlanAttendant,PlanScheduleAttendant
from planmate.resources.plan import PlanAttendantModelResource


# plan_attendants
def get_attendants(context, request):
  print('GET_ATTENDANTS', context, request)

  if not isinstance(context, PlanAttendantModelResource):
    raise HTTPBadRequest()

  query = PlanAttendant.query(
    PlanAttendant.plan_key == context.get_parent_key())
  entities = query.fetch( projection = [PlanAttendant.user_key] )

  keys = []
  for entity in entities:
    keys.append(entity.user_key)

  attendants = ndb.get_multi(keys)

  return mydb.list_to_dict_with_id(attendants)
