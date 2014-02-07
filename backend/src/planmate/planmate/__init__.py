import os
__here__ = os.path.dirname(os.path.abspath(__file__))


from pyramid.config import Configurator
import ConfigParser
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings
from planmate.lib.exceptions import status_map


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
  config.add_route('api_options', '/api/*traverse', request_method='OPTIONS', factory='planmate.resources.api.OptionsResource')
  config.add_view('planmate.views.api.options', route_name='api_options', request_method='OPTIONS', renderer='string')


  # API routes and views
  config.add_route('api', '/api/*traverse', factory='planmate.resources.api.root.RootResource')

  # root view
  config.add_view(
    'planmate.views.api.crud.root',
    context='planmate.resources.api.root.RootResource',
    route_name='api', renderer='json',
    request_method='GET', name='')

  # auth
  config.add_view(
    'planmate.views.auth.status',
    context='planmate.resources.api.auth.AuthenticationResource',
    route_name='api', renderer='json',
    request_method='GET', name='status')

  model_resources = [
    'users.UserModelResource',
    'plans.PlanModelResource',
    'plans.attendants.PlanAttendantModelResource',
    'plans.comments.PlanCommentModelResource',
    'plans.schedules.PlanScheduleModelResource',
    'plans.schedules.attendants.PlanScheduleAttendantModelResource',
    'me.plans.MyPlanModelResource'
    ]
  for resource in model_resources:
    context = 'planmate.resources.api.' + resource

    # list view
    config.add_view('planmate.views.api.crud.index',
      context=context, route_name='api', renderer='json',
      request_method='GET', name='')

    # create view
    config.add_view('planmate.views.api.crud.create',
      context=context, route_name='api', renderer='json',
      request_method='POST', name='')


  entity_resources = [
    'users.UserEntityResource',
    'plans.PlanEntityResource',
    'plans.attendants.PlanAttendantEntityResource',
    'plans.comments.PlanCommentEntityResource',
    'plans.schedules.PlanScheduleEntityResource',
    'plans.schedules.attendants.PlanScheduleAttendantEntityResource',
    'me.MyEntityResource',
    'me.plans.MyPlanEntityResource'
    ]
  for resource in entity_resources:
    context = 'planmate.resources.api.' + resource

    # show view
    config.add_view('planmate.views.api.crud.show',
      context=context, route_name='api', renderer='json',
      request_method='GET', name='')

    # update view
    config.add_view('planmate.views.api.crud.update',
      context=context, route_name='api', renderer='json',
      request_method='PUT', name='')

    # delete view
    config.add_view('planmate.views.api.crud.destroy',
      context=context, route_name='api', renderer='json',
      request_method='DELETE', name='')

  # auth
  config.add_route('debug_login', '/debug/login/{offset}')

  config.add_route('auth_login', '/auth/login/{provider_type}')
  config.add_view('planmate.views.auth.login', route_name='auth_login')

  config.add_view('planmate.views.auth.complete', context='velruse.AuthenticationComplete')
  config.add_view('planmate.views.auth.denied', context='velruse.AuthenticationDenied')

  #config.add_route('api.auth.status.get', '/api/auth/status', request_method='GET')

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
