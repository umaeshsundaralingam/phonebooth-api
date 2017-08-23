from app import schemas

# Resource definitions
users = {
    # We disable endpoint caching as we don't want client apps to
    # cache user account data.
    'cache_control': '',
    'cache_expires': 0,

    # Only allow managers and admins.
    'allowed_roles': ['manager', 'admin'],

    # Finally, let's add the schema definition for this endpoint.
    'schema': schemas.user
}

accounts = {
    # Only allow human users
    'allowed_roles': ['enduser', 'manager', 'admin'],

    # Add the schema definition for this endpoint.
    'schema': schemas.account,
    'allow_unknown': True
}

calls = {
    'allowed_roles': ['api', 'enduser', 'manager', 'admin'],
    'schema': schemas.call,
    'allow_unknown': True
}
