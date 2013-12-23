from pyramid.view import view_config
#from velruse import login_url,AuthenticationComplete

# store credentials, create accounts, and redirect
@view_config(
    context='velruse.AuthenticationComplete',
    renderer='mytemplate.jinja2'
)
def login_complete_view(request):
    context = request.context
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile':       context.profile,
        'credentials':   context.credentials
    }
    print(result)
    return {'project':'complete'}


@view_config(
    context='velruse.AuthenticationDenied',
    renderer='mytemplate.jinja2'
)
def login_denied_view(request):
    return {'project':'denied'}
