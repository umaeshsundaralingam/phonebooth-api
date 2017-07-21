import os
from app import resources

try:
    # Heroku sets a PORT evironment variable that we can look for.
    # This way, we know if we are on a Heroku ``production`` or ``staging``
    # environment, and let it use the variables in the .env file
    if os.environ['PORT']:
        pass
except KeyError:
    # or if we are developing locally and need the debugger, then load the .env manually
    # in case we are using foreman directly (as oppossed to heroku)
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv('.env'))


settings = {
    # Global variables
    'X_DOMAINS': os.environ.get('X_DOMAINS').split(','),

    'MONGO_HOST': os.environ.get('MONGO_HOST'),
    'MONGO_PORT': os.environ.get('MONGO_PORT'),
    'MONGO_USERNAME': os.environ.get('MONGO_USER'),
    'MONGO_PASSWORD': os.environ.get('MONGO_PASS'),
    'MONGO_DBNAME': os.environ.get('MONGO_DBNM'),

    'CELERY_BROKER_URL': os.environ.get('CELERY_BROKER_URL'),
    'CELERY_RESULT_BACKEND': os.environ.get('CELERY_RESULT_BACKEND'),

    'CTM_USER': os.environ.get('CTM_USER'),
    'CTM_PASS': os.environ.get('CTM_PASS'),
    'CTM_URL': os.environ.get('CTM_URL'),

    # Global method definitons
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PATCH', 'PUT', 'DELETE'],

    # Resource availability
    'DOMAIN': {
        'users': resources.users,
        'accounts': resources.accounts,
        'calls': resources.calls
    }
}

