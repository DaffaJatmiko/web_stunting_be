from pyramid.config import Configurator
import logging
from pyramid.renderers import JSON
# from pyramid.authorization import ACLAuthorizationPolicy
# from pyramid.authentication import AuthTktAuthenticationPolicy
log = logging.getLogger(__name__)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        log.info("Configuring the application")

        # Add JSON renderer
        json_renderer = JSON()
        config.add_renderer(None, json_renderer)
        config.add_renderer('json', json_renderer)

        config.include('.models')
        config.include('.routes')

        
        config.scan()
        log.debug("Registered routes:")
        for route in config.get_routes_mapper().get_routes():
            log.debug(f"  {route.name}: {route.pattern}")

    return config.make_wsgi_app()