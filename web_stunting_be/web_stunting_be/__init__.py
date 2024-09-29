from pyramid.config import Configurator
from pyramid.renderers import JSON
# from pyramid.authorization import ACLAuthorizationPolicy
# from pyramid.authentication import AuthTktAuthenticationPolicy

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('.routes')
        config.include('.middleware')

        config.add_renderer(None, 'json')


        # # Security policies
        # authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
        # authz_policy = ACLAuthorizationPolicy()
        # config.set_authentication_policy(authn_policy)
        # config.set_authorization_policy(authz_policy)
        
        config.scan()
    return config.make_wsgi_app()