import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from flask import request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from redis import StrictRedis
from app import celery
from app import config
from app.utils.tasker import make_celery
import views.account_tasks

def create_app(config=None, environment=None):

    class RolesAuth(BasicAuth):
        def check_auth(self, username, password, allowed_roles, resource, method):
            # use Eve's own db driver; no additional connections/resources are used
            users = app.data.driver.db['users']
            lookup = {'username': username }
            if allowed_roles:
                # only retrieve a user if his roles match ``allowed_roles``
                lookup['roles'] = {'$in': allowed_roles}
            user = users.find_one(lookup)
            return user and \
                bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8')


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


    def reference_call_to_account_callback(request):
        """Replace call data payload ``account_id`` with the correct ObjectId
        reference to an account in PhoneBooth's datastore. Save the original ``id``
        and ``account_id`` as ``ctm_id``, and ``ctm_account_id`` respectively,
        in case there is a need to reference it back in CTM.
        """
        payload=request.json
        accounts = app.data.driver.db['accounts']
        lookup = {'ctm_id': payload['account_id']}
        account = accounts.find_one(lookup)

        payload['ctm_id'] = payload['id']
        payload['ctm_account_id'] = payload['account_id']
        del payload['id'], payload['account_id']
        payload['account_id'] = account['_id']


    app = Eve(
        settings=config.settings,
        auth=BearerAuth
    )
    ResourceOwnerPasswordCredentials(app)
    app.on_pre_POST_calls += reference_call_to_account_callback
    make_celery(app, celery)

    app.register_blueprint(views.account_tasks.task, url_prefix='/tasks')

    return app
