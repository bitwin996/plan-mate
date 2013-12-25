from pyramid.view import view_config
#from models.user import User,SESSION_KEY
from planmate.models.user import User,SESSION_KEY

# store credentials, create accounts, and redirect
@view_config(
    context='velruse.AuthenticationComplete',
    renderer='mytemplate.jinja2'
)
def login_complete_view(request):
    context = request.context
    """
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile':       context.profile,
        'credentials':   context.credentials
    }
    print(result)
    """
    provider_type = context.provider_type
    provider_userid = int(context.profile['accounts'][0]['userid'])
    print(provider_userid)

    query = User.query(
        User.provider_type == provider_type,
        User.provider_userid == provider_userid
        )
    count = query.count()

    if count is 0:
        user = User(
            provider_type = provider_type,
            provider_userid = provider_userid,
            name = context.profile['displayName']
            )
        user.put()
    elif count is 1:
        user = query.get()
    else:
        raise

    print(user)
    request.session[SESSION_KEY] = user.key

    return {'project':'complete'}


@view_config(
    context='velruse.AuthenticationDenied',
    renderer='mytemplate.jinja2'
)
def login_denied_view(request):
    return {'project':'denied'}
