from pyramid.config import Configurator
import ConfigParser
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings
import os

import views
import views.auth

from planmate.lib.helpers import RootResource,ModelResource
from planmate.models.user import User
from planmate.models.plan import *

from resources import Root
import pyramid_jinja2


__here__ = os.path.dirname(os.path.abspath(__file__))


class AppRoot(RootResource):
  def init_resources(self):
    users = ModelResource(self.request, name='test_users', model=User)
    plans = ModelResource(self.request, name='plans', model=Plan)
    plan_attendants = ModelResource(self.request, name='plan_attendants', model=PlanAttendant)

    plans.add_resource(plan_attendants)
    users.add_resource(plans)
    self.add_resource(users)


def make_app():
  """ This function returns a Pyramid WSGI application.
  """
  config = Configurator(root_factory=AppRoot)
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
  config.add_route('spi', '/spi/*traverse', factory='planmate.AppRoot')
  config.add_view('planmate.views.debug.traversal', route_name='spi', renderer='json')

  config.add_route('auth_login', '/auth/login/{provider_type}')

  config.add_route('api.auth.status.get', '/api/auth/status', request_method='GET')
  config.add_route('api.auth.status.options', '/api/auth/status', request_method='OPTIONS')

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

  # debug
  config.add_route('debug_login', '/debug/login/{offset}')

  config.scan()

  return config.make_wsgi_app()

application = make_app()
