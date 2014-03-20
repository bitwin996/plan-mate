from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from google.appengine.ext import ndb

from planmate.models.user import User,Friendship
from planmate.lib.helpers import AuthenticationHelper


def login(request):
  AuthenticationHelper.instance().logout()

  base_url = request.registry.settings['frontend.base_url']

  # Invoke login request
  provider_type = request.matchdict['provider_type']

  # Sub Request for internal redirect
  sub_request = Request.blank('/login/' + provider_type, base_url = request.host_url)
  response = request.invoke_subrequest(sub_request)
  return response


def complete(context, request):
  print 'LOGIN COMPLETE', context, context.credentials

  session = request.session

  provider_type = context.provider_type
  provider_userid = int(context.profile['accounts'][0]['userid'])
  profile_image_url = context.profile['photos'][0]['value']

  query = User.query(
    User.provider_type == provider_type,
    User.provider_userid == provider_userid,
    User.registered == True
    )
  user = query.get()
  print 'USER', user

  if not user:
    # Create user account
    user = User(
      provider_type = provider_type,
      provider_userid = provider_userid,
      name = context.profile['displayName'],
      profile_image_url = profile_image_url,
      registered = True
      )
    user.put()

  # Store user key to session
  AuthenticationHelper.instance().set_user_id(user.key.id())
  #print 'SESSION', AuthenticationHelper.instance().get_user_id()
  #request.session.save()

  # Store and access tokens to session for Twitter
  session['resource_owner_key'] = context.credentials['oauthAccessToken']
  session['resource_owner_secret'] = context.credentials['oauthAccessTokenSecret']

  current_user = AuthenticationHelper.instance().get_user()

  #TODO Get friend list
  if provider_type == 'twitter':
    friends_data = get_twitter_friend_list(context, request)

    if friends_data:
      new_social_user_ids = [int(data['id_str']) for data in friends_data]

      # Users already in DB
      existing_users = User.query(
        ndb.AND(User.provider_type == provider_type,
                User.provider_userid.IN(new_social_user_ids))).fetch()
      existing_social_user_ids = [user.provider_userid for user in existing_users]

      existing_friends_data = []
      not_existing_friends_data = []
      for data in friends_data:
        if int(data['id_str']) in existing_social_user_ids:
          existing_friends_data.append(data)
        else:
          not_existing_friends_data.append(data)

      updating_users = []

      for data in existing_friends_data:
        # Update existing user
        user = [user for user in existing_users if user.provider_userid == int(data['id_str'])].pop()

        user.name = data['screen_name']
        user.profile_image_url = data['profile_image_url']
        updating_users.append(user)

      for data in not_existing_friends_data:
        # Create new user as temporary
        user = User(
          provider_type = provider_type,
          provider_userid = int(data['id_str']),
          name = data['screen_name'],
          profile_image_url = data['profile_image_url'],
          registered = False)
        updating_users.append(user)

      user_keys = ndb.put_multi(updating_users)

      # Update Friendships
      new_friendships = []
      existing_friendships = Friendship.query(ancestor=current_user.key)
      for user_key in user_keys:
        _friendships = [f for f in existing_friendships if f.user_key == user_key]
        if len(_friendships) == 0:
          # Create new Friendship
          friendship = Friendship(
            user_key = user_key,
            parent = current_user.key)
          new_friendships.append(friendship)

        elif len(_friendships) == 1:
          # Do nothing
          friendship = _friendships.pop()

        #elif len(_friendships) > 1:
        else:
          raise UserWarning(str(current_user_key) + " has duplicated Friendships to " + str(user_key))

      ndb.put_multi(new_friendships)

  # Redirect to main page
  base_url = request.registry.settings['frontend.base_url']
  return HTTPFound(location = base_url + '/#/auth/login-complete')


#@view_config(context='velruse.AuthenticationDenied')
def denied(context, request):
  base_url = request.registry.settings['frontend.base_url']
  reason = request.context.reason
  return HTTPFound(location = base_url + '/#/')


def get_twitter_friend_list(context, request):
  import requests
  from requests_oauthlib import OAuth1Session

  url = 'https://api.twitter.com/1.1/friends/list.json'

  session = request.session

  settings = request.registry.settings
  consumer_key = settings['velruse.twitter.consumer_key']
  consumer_secret = settings['velruse.twitter.consumer_secret']

  oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=session['resource_owner_key'],
    resource_owner_secret=session['resource_owner_secret'])

  response = oauth.get(url)

  if response.status_code == 200:
    data = response.json()
    return data['users']

  elif response.status_code == 401:
    del session['resource_owner_key']
    del session['resource_owner_secret']

