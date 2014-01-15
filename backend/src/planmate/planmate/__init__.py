from pyramid.config import Configurator
from resources import Root
import views
import views.auth
import pyramid_jinja2
import os

import ConfigParser

from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from pyramid.request import Request
from pyramid.request import Response

from pyramid.events import subscriber, NewResponse


__here__ = os.path.dirname(os.path.abspath(__file__))


#@subscriber(NewResponse)
#def add_access_list(event):
#  event.response.headerlist.append(
#    ('Access-Control-Allow-Origin', 'http://localhost:9000')
#    )

def make_app():
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root)
    config.add_renderer('.jinja2', pyramid_jinja2.Jinja2Renderer)
    config.add_view(views.my_view,
                    context=Root,
                    renderer='mytemplate.jinja2')
    config.add_static_view(name='static',
                           path=os.path.join(__here__, 'static'))

    # config
    conf = ConfigParser.SafeConfigParser()
    conf.read(os.path.join(__here__, '..', 'development.ini'))

    settings = dict(conf.items('app:main'))
    config.add_settings(settings)

    # CORS
    #def request_factory(environ):
    #    request = Request(environ)
    #    #if request.is_xhr:
    #    request.response = Response()
    #    request.response.headerlist = []
    #    request.response.headerlist.extend(
    #            (
    #                #('Access-Control-Allow-Origin', '*'),
    #                ('Access-Control-Allow-Origin', 'http://localhost:9000')
    #                #('Content-Type', 'application/json')
    #            )
    #    )
    #    return request
    #config.set_request_factory(request_factory)
    #config.add_subscriber(add_access_list)

    # oauth
    config.include('velruse.providers.facebook')
    config.add_facebook_login_from_settings(prefix='velruse.facebook.')
    config.include('velruse.providers.twitter')
    config.add_twitter_login_from_settings(prefix='velruse.twitter.')

    # session
    config.include('pyramid_beaker')

    # route
    config.add_route('auth_login', '/auth/login/{provider_type}')
    config.add_route('api_auth_status', '/api/auth/status')
    config.add_route('api_me_plans', '/api/me/plans')

    config.scan()

    return config.make_wsgi_app()

application = make_app()
