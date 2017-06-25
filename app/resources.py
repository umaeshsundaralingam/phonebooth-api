from app import schemas

# Resource definitions
users = {
    # We disable endpoint caching as we don't want client apps to
    # cache user account data.
    'cache_control': '',
    'cache_expires': 0,

    # Only allow superusers and admins.
    'allowed_roles': ['admin', 'superuser'],

    # Finally, let's add the schema definition for this endpoint.
    'schema': schemas.user
}

accounts = {
    # Only allow superusers and admins.
    'allowed_roles': ['enduser', 'admin', 'superuser'],

    # Add the schema definition for this endpoint.
    'schema': schemas.account,
    'allow_unknown': True
}

calls = {
    'allowed_roles': ['external_api', 'enduser', 'admin', 'superuser'],
    'schema': schemas.call,
    'allow_unknown': True
}

