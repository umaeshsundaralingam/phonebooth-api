import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from flask import request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from redis import StrictRedis
from app import celery
from app import config
from app.utils.tasker import init_celery
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


    def prepare_documents_for_import_callback(resource, request):
        payload = request.get_json()
        documents = [[payload], payload][type(payload) == list]
        for document in documents.copy():
            try:
                if document['created']:
                    from dateutil.parser import parse
                    document['ctm_created'] = parse(document['created'])
                    del document['created']

                if document['account_id']:
                    accounts = app.data.driver.db['accounts']
                    lookup = {'ctm_id': document['account_id']}
                    account = accounts.find_one(lookup)
                    document['ctm_account_id'] = document['account_id']
                    document['account_id'] = account['_id']
            except KeyError:
                pass
            finally:
                document['ctm_id'] = document['id']
                del document['id']

                for key in document.copy():
                    if "url" in key:
                        del document[key]


    app = Eve(
        settings=config.settings,
        auth=BearerAuth
    )
    
    ResourceOwnerPasswordCredentials(app)
    app.on_pre_POST += prepare_documents_for_import_callback
    
    app.config.update(config.extra_settings)
    init_celery(app, celery)

    app.register_blueprint(views.account_tasks.task, url_prefix='/tasks')

    return app

