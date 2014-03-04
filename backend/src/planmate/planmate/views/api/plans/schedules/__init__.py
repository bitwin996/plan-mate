from google.appengine.ext import ndb
from planmate.models.plan import PlanScheduleAttendant


def show(context, request):
  print 'PLAN_SCHEDULE SHOW', context
  key = context.get_key()
  plan_schedule = key.get()
  plan_schedule_json = plan_schedule.to_json()

  attendants = PlanScheduleAttendant.query(ancestor=key).fetch()

  attendants_json = []
  user_keys = []
  for attendant in attendants:
    attendants_json.append(attendant.to_json())
    user_keys.append(attendant.user_key)

  users = ndb.get_multi(user_keys)
  users_json = [user.to_json() for user in users]

  return {
    'plan_schedule': plan_schedule_json,
    'plan_schedule_attendants': attendants_json,
    'users': users_json
    }

