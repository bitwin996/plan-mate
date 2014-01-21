from pyramid.view import view_config
from pyramid.events import subscriber,NewRequest

from pyramid.httpexceptions import HTTPUnauthorized
from google.appengine.ext.ndb.model import InvalidPropertyError

from planmate.lib.helpers import AuthenticationHelper


# default view
def my_view(request):
  return {'project':'planmate'}


@subscriber(NewRequest)
def initialize_authentication(event):
  AuthenticationHelper.instance().set_session(event.request.session)


@view_config(context=HTTPUnauthorized, renderer='json')
def http_unauthorized(exception, request):
  request.response.status = 401
  return {'message':'Please log in to continue.'}


@view_config(context=InvalidPropertyError, renderer='json')
def invalid_property_error(exception, request):
  request.response.status = 500
  message = exception.args[0] if exception.args else 'Some invalid parameters are posted.'
  return {'message':message}


