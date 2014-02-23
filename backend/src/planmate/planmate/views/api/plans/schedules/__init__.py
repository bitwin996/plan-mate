"""
from pyramid.httpexceptions import HTTPNotFound
from google.appengine.ext import ndb
from planmate.lib import mydb
from planmate.lib.helpers import underscorize,pluralize
from planmate.views.api.crud import index


def create(context, request):
  print 'PLAN_SCHEDULE CREATE', context

  new_entity = context.get_new_entity()

  post_params = request.json_body if hasattr(request, 'json_body') else {}
  print 'POST_PARAMS', post_params

  new_entity.set_prop_values(**post_params)
  new_entity.put()

  response = index(context, request)
  print response
  return response
"""
