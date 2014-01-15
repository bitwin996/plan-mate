from pyramid.view import view_config
from planmate.models.user import User,SESSION_KEY

@view_config(route_name='api_auth_status', renderer='json')
def api_auth_status(request):
    #request.response.headers['Access-Control-Allow-Origin'] = '*'
    login = SESSION_KEY in request.session
    return {'login': login}



