from pyramid.view import view_config
from google.appengine.ext import ndb

from planmate.models.plan import Plan
from planmate.lib.helpers import to_dict_with_key


@view_config(route_name='api.plans.show.options', renderer='string')
def options(request): return


@view_config(route_name='api.plans.show.get', renderer='json')
def get(request):
  key_string = request.matchdict.get('id')
  key = ndb.Key(urlsafe = key_string)
  plan = key.get()
  print('MATCH', plan)
  return to_dict_with_key(plan)
