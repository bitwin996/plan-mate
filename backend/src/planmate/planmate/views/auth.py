from pyramid.view import view_config
from planmate.models.user import User,SESSION_KEY
from pyramid.httpexceptions import HTTPFound
from pyramid.config import Configurator


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
    request.session[SESSION_KEY] = user.key

    # Redirect to main page
    base_url = request.registry.settings['frontend.base_url']
    return HTTPFound(location = base_url + '/#/')


@view_config(context='velruse.AuthenticationDenied')
def login_denied_view(request):
    base_url = request.registry.settings['frontend.base_url']
    reason = request.context.reason
    return HTTPFound(location = base_url + '/#/')


@view_config(renderer='json')
def info(request):
    is_login = not not request.session[SESSION_KEY]
    return {'is_login': is_login}

