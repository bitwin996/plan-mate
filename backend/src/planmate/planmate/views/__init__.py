from pyramid.events import subscriber,NewResponse,NewRequest
from planmate.lib.helpers import AuthenticationHelper

# default view
def my_view(request):
  return {'project':'planmate'}


@subscriber(NewRequest)
def initialize_authentication(event):
  AuthenticationHelper.instance().set_session(event.request.session)
