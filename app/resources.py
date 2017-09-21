from app import schemas
from app.utils.auth import RolesAuth

# Resource definitions
users = {
    # We disable endpoint caching as we don't want client apps to
    # cache user account data.
    'cache_control': '',
    'cache_expires': 0,

    # Only allow managers and admins to access/administer users
    'allowed_roles': ['manager', 'admin'],

    # Add the schema definition for this endpoint.
    'schema': schemas.user
}

accounts = {
    'allowed_roles': ['enduser', 'manager', 'admin'],
    'schema': schemas.account
}

calls = {
    'allowed_roles': ['api', 'enduser', 'manager', 'admin'],
    'schema': schemas.call,
    'allow_unknown': True
}

ctm_calls = {
    'allowed_roles': ['api'],
    'authentication': RolesAuth,
    'resource_methods': ['POST'],
    'item_methods': [],
    'datasource': {
        'source': 'calls'
    },
    'schema': schemas.call,
    'allow_unknown': True
}
