from pyramid.events import subscriber,NewRequest
from planmate.lib.helpers import AuthenticationHelper

@subscriber(NewRequest)
def initialize_authentication(event):
  AuthenticationHelper.instance().set_session(event.request.session)

  event.request.response.headers.update({
    'Access-Control-Allow-Origin': 'http://localhost:9000',
    'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type, X-HTTP-Method-Override',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': '*',
    'Content-Type': 'application/json; charset=UTF-8'
    })

"""
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPUnauthorized
from google.appengine.ext.ndb.model import InvalidPropertyError



# default view
def my_view(request):
  return {'project':'planmate'}


@view_config(context=HTTPUnauthorized, renderer='json')
def http_unauthorized(exception, request):
  request.response.status = 401
  return {'message':'Please log in to continue.'}


@view_config(context=InvalidPropertyError, renderer='json')
def invalid_property_error(exception, request):
  #TODO
  request.response.status = 409
  message = exception.args[0] if exception.args else 'Some invalid parameters are posted.'
  return {'message':message}
"""
