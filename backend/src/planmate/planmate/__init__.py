import os
__here__ = os.path.dirname(os.path.abspath(__file__))


from pyramid.config import Configurator
import ConfigParser
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

def make_app():
  """ This function returns a Pyramid WSGI application.
  """
  #config = Configurator(root_factory='planmate.views.debug.ApiRoot')
  config = Configurator()

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

  # scan first for initialize session
  #config.scan()

  # route
  # API
  config.add_route('api_options', '/api/*traverse', request_method='OPTIONS', factory='planmate.lib.resources.OptionsRoot')
  config.add_view('planmate.views.api.options', route_name='api_options', request_method='OPTIONS', renderer='string')

  config.add_route('api', '/api/*traverse', factory='planmate.resources.ApiRoot')
  config.add_view('planmate.views.api.get', route_name='api', name='', request_method='GET', renderer='json')
  config.add_view('planmate.views.api.add', route_name='api', name='add', request_method='GET', renderer='json')
  config.add_view('planmate.views.api.show', route_name='api', name='show', request_method='GET', renderer='json')

  # auth
  config.add_route('debug_login', '/debug/login/{offset}')
  config.add_route('auth_login', '/auth/login/{provider_type}')

  config.add_route('api.auth.status.get', '/api/auth/status', request_method='GET')
  #config.add_route('api.auth.status.options', '/api/auth/status', request_method='OPTIONS')

  """
  config.add_route('spi_options', '/bpi/*traverse', request_method='OPTIONS', factory='planmate.lib.resources.OptionsRoot')
  config.add_view('planmate.views.debug.options', route_name='spi_options', renderer='string')
  """


  #config.add_route('spi_get', '/bpi/*traverse', request_method="GET", factory='planmate.resources.AppRoot')
  #config.add_view('planmate.views.debug.get', route_name='spi_get', renderer='json')

  #config.add_route('spi_post', '/bpi/*traverse', request_method="POST", factory='planmate.resources.AppRoot')
  #config.add_view('planmate.views.debug.post', route_name='spi_post', renderer='json')


  """
  config.add_route('api.plans.one.options', pattern='/api/plans/{plan_key}', request_method='OPTIONS')
  config.add_route('api.plans.one.get', pattern='/api/plans/{plan_key}', request_method='GET')
  config.add_route('api.plans.one.post', pattern='/api/plans/{plan_key}', request_method='POST')

  config.add_route('api.plans.one.attend-options', pattern='/api/plans/{plan_key}/attend', request_method='OPTIONS')
  config.add_route('api.plans.one.attend', pattern='/api/plans/{plan_key}/attend', request_method='POST')

  config.add_route('api.plans.one.schedules.options', pattern='/api/plans/{plan_key}/schedules', request_method='OPTIONS')
  config.add_route('api.plans.one.schedules.get', pattern='/api/plans/{plan_key}/schedules', request_method='GET')
  config.add_route('api.plans.one.attendants.options', pattern='/api/plans/{plan_key}/attendants', request_method='OPTIONS')
  config.add_route('api.plans.one.attendants.get', pattern='/api/plans/{plan_key}/attendants', request_method='GET')
  config.add_route('api.plans.one.attendants.post', pattern='/api/plans/{plan_key}/attendants', request_method='POST')

  config.add_route('api.me.plans.get', pattern='/api/me/plans', request_method='GET')
  config.add_route('api.me.plans.options', pattern='/api/me/plans', request_method='OPTIONS')
  config.add_route('api.me.plans.post', pattern='/api/me/plans', request_method='POST')
  """

  return config.make_wsgi_app()

application = make_app()
