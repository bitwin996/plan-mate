from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request

from planmate.models.user import User
from planmate.lib.helpers import AuthenticationHelper


def login(request):
  AuthenticationHelper.instance().logout()

  base_url = request.registry.settings['frontend.base_url']

  # Invoke login request
  provider_type = request.matchdict['provider_type']

  # sub request
  sub_request = Request.blank('/login/' + provider_type, base_url = request.host_url)
  response = request.invoke_subrequest(sub_request)
  return response


def complete(context, request):
  print 'LOGIN COMPLETE', context

  provider_type = context.provider_type
  provider_userid = int(context.profile['accounts'][0]['userid'])
  profile_image_url = context.profile['photos'][0]['value']

  query = User.query(
    User.provider_type == provider_type,
    User.provider_userid == provider_userid
    )
  user = query.get()
  print 'USER', user

  if not user:
    # Create user account
    user = User(
      provider_type = provider_type,
      provider_userid = provider_userid,
      name = context.profile['displayName'],
      profile_image_url = profile_image_url
      )
    user.put()

  # Store user key to session
  AuthenticationHelper.instance().set_user_id(user.key.id())
  #print 'SESSION', AuthenticationHelper.instance().get_user_id()
  #request.session.save()

  # Redirect to main page
  base_url = request.registry.settings['frontend.base_url']
  return HTTPFound(location = base_url + '/#/auth/login-complete')


#@view_config(context='velruse.AuthenticationDenied')
def denied(context, request):
  base_url = request.registry.settings['frontend.base_url']
  reason = request.context.reason
  return HTTPFound(location = base_url + '/#/')

