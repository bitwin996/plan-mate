from google.appengine.ext import ndb
from planmate.models.plan import PlanAttendant
from planmate.lib.helpers import AuthenticationHelper
from planmate.views.api.crud import _create
from planmate.views.api.plans import plans_show_response

def create(context, request):
  _create(context, request)
  plan_key = context.__parent__.get_key()
  return plans_show_response(plan_key)


def destroy(context, request):
  print 'PLAN_ATTENDANT DESTROY', context

  key = context.get_key()
  entity = key.get()

  if hasattr(entity, 'user_key') and entity.user_key != AuthenticationHelper.instance().get_user_key():
    raise HTTPUnauthorized("You do not have a permission to do the action.")

  plan_key = key.parent()

  key.delete()

  return plans_show_response(plan_key)

  """
  plan = plan_key.parent().get()
  plan_json = entity.to_json()

  plan_key.delete()

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
