from planmate.lib.helpers import AuthenticationHelper
from pyramid.httpexceptions import HTTPFound


#TODO delete
#from pyramid.url import resource_url

import requests
from requests_oauthlib import OAuth1Session,OAuth1
#from velruse.compat import parse_qsl
from urlparse import parse_qs

from inspect import getmembers
from pprint import pprint
from planmate.lib.helpers import var_dump

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
BASE_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'

#AUTH_URL = 'https://api.twitter.com/oauth/authenticate'
#DATA_URL = 'https://api.twitter.com/1.1/users/show.json?screen_name=%s'

#print 'RESOURCE_URL', context, resource_url(context, request), request.route_url('api', traverse=('auth', 'debug_callback'))

def debug(context, request):
  settings = request.registry.settings
  consumer_key = settings['velruse.twitter.consumer_key']
  consumer_secret = settings['velruse.twitter.consumer_secret']

  # OAuth1Session
  print 'OAUTH_1_SESSION', consumer_key
  oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    callback_uri=request.route_url('api', traverse=('auth', 'debug_callback'))
    )
  fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)

  resource_owner_key = fetch_response.get('oauth_token')
  resource_owner_secret = fetch_response.get('oauth_token_secret')

  session = request.session
  session['resource_owner_key'] = resource_owner_key
  session['resource_owner_secret'] = resource_owner_secret

  authorization_url = oauth.authorization_url(BASE_AUTHORIZATION_URL)
  print 'URL', authorization_url

  #TODO Redirect to authorization_url
  return HTTPFound(location=authorization_url)


def debug_callback(context, request):
  print 'DEBUG_CALLBACK', request.GET

  settings = request.registry.settings
  consumer_key = settings['velruse.twitter.consumer_key']
  consumer_secret = settings['velruse.twitter.consumer_secret']

  verifier = request.GET['oauth_verifier']

  session = request.session
  resource_owner_key = session['resource_owner_key']
  resource_owner_secret = session['resource_owner_secret']
  print 'SESSION_TOKEN', resource_owner_key, resource_owner_secret

  oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=session['resource_owner_key'],
    resource_owner_secret=session['resource_owner_secret'],
    verifier=verifier)

  oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
  resource_owner_key = oauth_tokens.get('oauth_token')
  resource_owner_secret = oauth_tokens.get('oauth_token_secret')
  print 'ACCESS_TOKEN', resource_owner_key, resource_owner_secret

  session['resource_owner_key'] = resource_owner_key
  session['resource_owner_secret'] = resource_owner_secret

  oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=session['resource_owner_key'],
    resource_owner_secret=session['resource_owner_secret'])

  url = 'https://api.twitter.com/1.1/friends/list.json'
  response = oauth.get(url)

  if response.status_code == 200:
    data = response.json()
    print 'DATA', data

    for user in data['users']:
      print user['screen_name']
      for k,v in user.iteritems():
        print(k,v)

  elif response.status_code == 401:
    del session['resource_owner_key']
    del session['resource_owner_secret']

  return {'debug': 'OK'}


def status(context, request):
  print 'AUTH STATUS', context, AuthenticationHelper.instance().get_user_id()
  is_logged_in = AuthenticationHelper.instance().is_logged_in()

  if not is_logged_in:
    return {'is_logged_in': is_logged_in}

  user = AuthenticationHelper.instance().get_user()
  user_dict = user.to_json()

  user_dict.update({
    'user_id': user.key.id(),
    'user_key': user.key.urlsafe(),
    'is_logged_in': is_logged_in
    })

  return user_dict


def logout(context, request):
  print 'LOGOUT', context

  AuthenticationHelper.instance().logout()
  return {}

