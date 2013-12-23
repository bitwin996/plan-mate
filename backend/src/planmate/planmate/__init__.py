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
    conf.read(os.path.join(__here__, 'development.ini'))

    settings = dict(conf.items('app:main'))
    config.add_settings(settings)

    # oauth
    config.include('velruse.providers.facebook')
    config.add_facebook_login_from_settings(prefix='velruse.facebook.')

    # session
    config.include('pyramid_beaker')

    config.scan()

    return config.make_wsgi_app()

application = make_app()
