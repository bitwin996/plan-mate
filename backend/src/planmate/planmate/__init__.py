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

  # other special views
  config.add_view(
    'planmate.views.api.plans.attendants.index',
    context='planmate.resources.api.plans.attendants.PlanAttendantModelResource',
    route_name='api', renderer='json',
    request_method='GET', name='')

  config.add_view(
    'planmate.views.api.plans.attendants.create',
    context='planmate.resources.api.plans.attendants.PlanAttendantModelResource',
    route_name='api', renderer='json',
    request_method='POST', name='')


  model_resources = {
    'users.UserModelResource': ['index', 'create'],
    'plans.PlanModelResource': ['index', 'create'],
    'plans.attendants.PlanAttendantModelResource': [],
    'plans.comments.PlanCommentModelResource': ['index', 'create'],
    'plans.schedules.PlanScheduleModelResource': ['index', 'create'],
    'plans.schedules.attendants.PlanScheduleAttendantModelResource': ['index', 'create'],
    'me.plans.MyPlanModelResource': ['index', 'create']
    }
  for resource, views in model_resources.iteritems():
    context = 'planmate.resources.api.' + resource

    # index view
    if 'index' in views:
      config.add_view('planmate.views.api.crud.index',
        context=context, route_name='api', renderer='json',
        request_method='GET', name='')

    # create view
    if 'create' in views:
      config.add_view('planmate.views.api.crud.create',
        context=context, route_name='api', renderer='json',
        request_method='POST', name='')


  entity_resources = {
    'users.UserEntityResource': ['show', 'update', 'destroy'],
    'plans.PlanEntityResource': ['show', 'update', 'destroy'],
    'plans.attendants.PlanAttendantEntityResource': ['show', 'update', 'destroy'],
    'plans.comments.PlanCommentEntityResource': ['show', 'update', 'destroy'],
    'plans.schedules.PlanScheduleEntityResource': ['show', 'update', 'destroy'],
    'plans.schedules.attendants.PlanScheduleAttendantEntityResource': ['show', 'update', 'destroy'],
    'me.MyEntityResource': ['show', 'update', 'destroy'],
    'me.plans.MyPlanEntityResource': ['show', 'update', 'destroy']
    }
  for resource, views in entity_resources.iteritems():
    context = 'planmate.resources.api.' + resource

    # show view
    if 'show' in views:
      config.add_view('planmate.views.api.crud.show',
        context=context, route_name='api', renderer='json',
        request_method='GET', name='')

    # update view
    if 'update' in views:
      config.add_view('planmate.views.api.crud.update',
        context=context, route_name='api', renderer='json',
        request_method='PUT', name='')

    # destroy view
    if 'destroy' in views:
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
