from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPUnauthorized
import json

from planmate.models.user import User
from planmate.models.plan import Plan
from planmate.lib.helpers import AuthenticationHelper,to_dict_with_key


@view_config(route_name='api.me.plans.get', renderer='json')
def get(request):
  if AuthenticationHelper.instance().is_logged_in():
    query = Plan.query(
      Plan.user_key == AuthenticationHelper.instance().get_user_key()
      )
    plans = query.fetch()

    entities = []
    for plan in plans:
      entities.append(to_dict_with_key(plan))
    return entities

  else:
    raise HTTPUnauthorized()


@view_config(route_name='api.me.plans.options', renderer='string')
def options(request): return


@view_config(route_name='api.me.plans.post', renderer='json')
def post(request):
  params = request.json_body

  plan = Plan(
    user_key = AuthenticationHelper.instance().get_user_key(),
    place_name = params.get('place_name'),
    description = params.get('description')
    )
  plan_key = plan.put()

  return to_dict_with_key(plan)

