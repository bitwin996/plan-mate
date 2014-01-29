"""
from pyramid.events import subscriber,BeforeRender
from pyramid.httpexceptions import HTTPUnauthorized

from planmate.lib.helpers import AuthenticationHelper


@subscriber(BeforeRender)
def check_login(event):
  request_method = event['request'].method
  if request_method != 'OPTIONS' and not AuthenticationHelper.instance().is_logged_in():
    raise HTTPUnauthorized()
"""
