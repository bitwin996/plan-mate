from pyramid.view import view_config
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPUnauthorized
import json

import planmate.lib.helpers
from planmate.models.user import User #,SESSION_KEY
from planmate.models.plan import Plan


#def current_user_key(session):
#    key_string = session[SESSION_KEY]
#    user_key = ndb.Key(urlsafe = key_string)
#    return user_key

def to_dict_urlsafe_key(entity):
  d0 = entity.to_dict()
  d1 = {}

  for k in d0:
    v = d0[k]

    if isinstance(v, ndb.Key):
      d1[k] = v.urlsafe()
    else:
      d1[k] = v

  d1.update({'key':entity.key.urlsafe()})
  return d1


def _to_dict_urlsafe_key(entity, nest_level=0):
  d0 = entity.to_dict()
  d1 = {}
  for k in d0:
    v = d0[k]
    if isinstance(v, ndb.Key):
      if nest_level > 0:
        d1[k] = to_dict_urlsafe_key(v.get(), nest_level-1)
      else:
        d1[k] = v.urlsafe()

    elif isinstance(v, list):
      if nest_level > 0:
        d1[k] = ndb.get_multi(v)
      else:
        d1[k] = v

    else:
      d1[k] = v

  return d1


@view_config(route_name='api.me.plans.get', renderer='json')
def get(request):
  if SESSION_KEY in request.session:
    user_key = ndb.Key(urlsafe = request.session[SESSION_KEY])
    user = user_key.get()

    #TODO User's plans

    return []

  else:
    request.response.status = 401
    #return HTTPUnauthorized()
    return {'error':'Need to log in.'}


@view_config(route_name='api.me.plans.options', renderer='string')
def options(request): return


@view_config(route_name='api.me.plans.post', renderer='json')
def post(request):
  params = request.json_body

  plan = Plan(
    user_key = User.current_user_key(request.session),
    place_name = params.get('place_name'),
    description = params.get('description')
    )
  key = plan.put()

  _dict = to_dict_urlsafe_key(plan)
  #_dict.update({'key':key.urlsafe()})
  return _dict

