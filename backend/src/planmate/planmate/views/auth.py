from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.config import Configurator
from pyramid.request import Request

from pyramid.view import render_view
from pyramid.renderers import render_to_response

from pyramid.config.routes import RoutesConfiguratorMixin as Router

from planmate.models.user import User
import planmate.lib.helpers


@view_config(route_name='auth_login')
def auth_login(request):
  if SESSION_KEY in request.session:
    del request.session[SESSION_KEY]
  base_url = request.registry.settings['frontend.base_url']

  #print(dict(request.session))
  if SESSION_KEY in request.session:
    return HTTPFound(location = base_url + '/#/')
  else:
    # Invoke login request
    provider_type = request.matchdict['provider_type']

    # sub request
    sub_request = Request.blank('/login/' + provider_type, base_url = request.host_url)
    response = request.invoke_subrequest(sub_request)
    return response


@view_config(context='velruse.AuthenticationComplete')
def login_complete_view(request):
  context = request.context
  provider_type = context.provider_type
  provider_userid = int(context.profile['accounts'][0]['userid'])
  profile_image_url = context.profile['photos'][0]['value']

  query = User.query(
    User.provider_type == provider_type,
    User.provider_userid == provider_userid
    )
  count = query.count()

  if count is 0:
    # Create user account
    user = User(
      provider_type = provider_type,
      provider_userid = provider_userid,
      name = context.profile['displayName'],
      profile_image_url = profile_image_url
      )
    user.put()

  elif count is 1:
    user = query.get()

  else:
    raise

  # Store user key to session
  key_string = user.key.urlsafe()
  AuthenticationHelper.instance().set_key_string(key_string)

  # Redirect to main page
  base_url = request.registry.settings['frontend.base_url']
  return HTTPFound(location = base_url + '/#/')


@view_config(context='velruse.AuthenticationDenied')
def login_denied_view(request):
  base_url = request.registry.settings['frontend.base_url']
  reason = request.context.reason
  return HTTPFound(location = base_url + '/#/')

