import os
__here__ = os.path.dirname(os.path.abspath(__file__))


from pyramid.config import Configurator
import ConfigParser
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings
from planmate.views.api.exceptions import status_map


def make_app():
  """ This function returns a Pyramid WSGI application.
  """
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

  # route
  #config.scan()

  # API
  config.add_route('api_options', '/api/*traverse', request_method='OPTIONS', factory='planmate.lib.resources.OptionsRoot')
  config.add_view('planmate.views.api.options', route_name='api_options', request_method='OPTIONS', renderer='string')

  config.add_route('api', '/api/*traverse', factory='planmate.resources.ApiRoot')

  # specific views
  config.add_view('planmate.views.api.plans.get_attendants',
    context='planmate.resources.plan.PlanAttendantModelResource',
    route_name='api', name='', request_method='GET', renderer='json')

  # base views
  config.add_view('planmate.views.api.get', route_name='api', name='', request_method='GET', renderer='json')
  config.add_view('planmate.views.api.post', route_name='api', name='', request_method='POST', renderer='json')
  #TODO PUT
  config.add_view('planmate.views.api.delete', route_name='api', name='', request_method='DELETE', renderer='json')

  # auth
  config.add_route('debug_login', '/debug/login/{offset}')
  config.add_route('auth_login', '/auth/login/{provider_type}')

  config.add_route('api.auth.status.get', '/api/auth/status', request_method='GET')
  #config.add_route('api.auth.status.options', '/api/auth/status', request_method='OPTIONS')

  # exceptions
  for code in status_map:
    cls = status_map[code]
    config.add_view('planmate.views.api.exceptions.view', context='pyramid.httpexceptions.' + cls.__name__)

  db_exceptions = [
    'google.appengine.ext.ndb.model.InvalidPropertyError',
    'google.appengine.api.datastore_errors.BadValueError'
    ]
  for exception in db_exceptions:
    config.add_view('planmate.views.api.exceptions.view', context=exception)

  # subscribers
  config.add_subscriber('planmate.subscribers.cors.update_headers', 'pyramid.events.NewResponse')

  return config.make_wsgi_app()


application = make_app()
