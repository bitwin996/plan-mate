from pyramid.events import subscriber,BeforeRender
from planmate.models.user import User
from google.appengine.ext import ndb

from planmate.lib.helpers import AuthenticationHelper


@subscriber(BeforeRender)
def check_login(event):
  if not AuthenticationHelper.instance().is_logged_in():
    #TODO return 'not logged in' response
    return {'login': 'Not logged in'}


