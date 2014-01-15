from pyramid.events import subscriber, BeforeRender
from planmate.models.user import User,SESSION_KEY
from google.appengine.ext import ndb

@subscriber(BeforeRender)
def check_login(event):
    if SESSION_KEY in event['request'].session:
        user_key = ndb.Key(urlsafe = event['request'].session[SESSION_KEY])
        user = user_key.get()

    else:
        #event.response.status = 401
        #return HTTPUnauthorized()
        #return {'error':'Need to log in.'}
        print('#### NOT LOGGED IN')


