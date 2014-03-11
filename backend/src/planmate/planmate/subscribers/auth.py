from planmate.lib.helpers import AuthenticationHelper

def set_session(event):
  AuthenticationHelper.instance().set_session(event.request.session)
