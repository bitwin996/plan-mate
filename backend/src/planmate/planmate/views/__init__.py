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
