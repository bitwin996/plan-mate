from pyramid.config import Configurator
from resources import Root
import views
import views.auth
import pyramid_jinja2
import os

import ConfigParser

from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings


__here__ = os.path.dirname(os.path.abspath(__file__))


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

  # oauth
  config.include('velruse.providers.facebook')
  config.add_facebook_login_from_settings(prefix='velruse.facebook.')
  config.include('velruse.providers.twitter')
  config.add_twitter_login_from_settings(prefix='velruse.twitter.')

  # session
  config.include('pyramid_beaker')

  # route
  config.add_route('auth_login', '/auth/login/{provider_type}')

  config.add_route('api.auth.status.get', '/api/auth/status', request_method='GET')
  config.add_route('api.auth.status.options', '/api/auth/status', request_method='OPTIONS')

  config.add_route('api.plans.show.options', pattern='/api/plans/{id}', request_method='OPTIONS')
  config.add_route('api.plans.show.get', pattern='/api/plans/{id}', request_method='GET')

  config.add_route('api.me.plans.get', pattern='/api/me/plans', request_method='GET')
  config.add_route('api.me.plans.options', pattern='/api/me/plans', request_method='OPTIONS')
  config.add_route('api.me.plans.post', pattern='/api/me/plans', request_method='POST')

  # debug
  config.add_route('debug_login', '/debug/login/{offset}')

  config.scan()

  return config.make_wsgi_app()

application = make_app()
