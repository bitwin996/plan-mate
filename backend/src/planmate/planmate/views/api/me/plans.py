from pyramid.view import view_config
from planmate.models.user import User,SESSION_KEY
from google.appengine.ext import ndb
from pyramid.httpexceptions import HTTPUnauthorized


@view_config(route_name='api_me_plans', renderer='json')
def api_me_plans(request):
    if SESSION_KEY in request.session:
        user_key = ndb.Key(urlsafe = request.session[SESSION_KEY])
        user = user_key.get()

        return {'plans': []}

    else:
        request.response.status = 401
        #return HTTPUnauthorized()
        return {'error':'Need to log in.'}
