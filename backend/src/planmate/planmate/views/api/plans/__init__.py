from google.appengine.ext import ndb
from planmate.models.plan import PlanAttendant
#from copy import copy

def show(context, request):
  print 'PLAN SHOW', context, request
  plan_key = context.get_key()
  return plans_show_response(plan_key)

  """
  plan = plan_key.get()
  plan_json = plan.to_json()

  attendants = PlanAttendant.query(ancestor=plan_key).fetch()
  attendants_json = [attendant.to_json() for attendant in attendants]

  user_keys = [attendant.user_key for attendant in attendants]
  users = ndb.get_multi(user_keys)
  users_json = [user.to_json() for user in users]

  response = {
    'plan': plan_json,
    'plan_attendants': attendants_json,
    'users': users_json
    }
  return response
  """


def plans_show_response(plan_key):
  plan = plan_key.get()
  plan_json = plan.to_json()

  attendants = PlanAttendant.query(ancestor=plan_key).fetch()
  attendants_json = [attendant.to_json() for attendant in attendants]

  user_keys = [attendant.user_key for attendant in attendants]
  users = ndb.get_multi(user_keys)
  users_json = [user.to_json() for user in users]

  response = {
    'plan': plan_json,
    'plan_attendants': attendants_json,
    'users': users_json
    }

  return response
