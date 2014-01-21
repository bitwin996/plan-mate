from pyramid.events import subscriber,NewResponse
from planmate.lib.helpers import AuthenticationHelper


@subscriber(NewResponse)
def add_cors_header(event):
  event.response.headers.update({
    'Access-Control-Allow-Origin': 'http://localhost:9000',
    'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type, X-HTTP-Method-Override',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': '*',
    'Content-Type': 'application/json; charset=UTF-8'
    })
