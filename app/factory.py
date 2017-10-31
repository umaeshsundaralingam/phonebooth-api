from eve import Eve
from eve.auth import BasicAuth
from flask import request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from redis import StrictRedis
from app import celery
from app import config
from app.utils.tasker import init_celery
from app.utils.events import prepare_documents_for_import_callback
from app.views.tasks import task

def create_app(config=None, environment=None):
    class BearerAuth(BasicAuth):
        """ Overrides Eve's built-in basic authorization scheme and uses Redis to
        validate bearer token
        """
        def __init__(self):
            super(BearerAuth, self).__init__()
            self.redis = StrictRedis.from_url(config.settings['SENTINEL_REDIS_URL'])

        def check_auth(self, token, allowed_roles, resource, method):
            """ Check if API request is authorized.
            Examines token in header and checks Redis cache to see if token is
            valid. If so, request is allowed.
            :param token: OAuth 2.0 access token submitted.
            :param allowed_roles: Allowed user roles.
            :param resource: Resource being requested.
            :param method: HTTP method being executed (POST, GET, etc.)
            """
            return token and self.redis.get(token)

        def authorized(self, allowed_roles, resource, method):
            """ Validates the the current request is allowed to pass through.
            :param allowed_roles: allowed roles for the current request, can be a
                                  string or a list of roles.
            :param resource: resource being requested.
            """
            try:
                token = request.headers.get('Authorization').split(' ')[1]
            except:
                token = None
            return self.check_auth(token, allowed_roles, resource, method)

    app = Eve(
        settings=config.settings,
        auth=BearerAuth
    )

    ResourceOwnerPasswordCredentials(app)
    app.on_pre_POST += prepare_documents_for_import_callback
    
    app.config.update(config.extra_settings)
    init_celery(app, celery)

    app.register_blueprint(task, url_prefix='/tasks')

    return app

