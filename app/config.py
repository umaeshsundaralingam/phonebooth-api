import os
from app import resources

# Heroku sets a PORT evironment variable that we can look for.
# This way, we know if we are on a Heroku ``production`` or ``staging``
# environment, and let it use the set environment variables
try:
    if os.environ['PORT']:
        pass
except KeyError:
    # or if we are developing locally and using foreman instead of heroku local,
    # then load the .env
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv('.env'))

# Grab global variables and add them to a ``settings`` dictionary to pass on
# to eve; only grab variables pre-pended with "EVE_" or "APP_".
settings = dict()
extra_settings = dict()

for key, value in os.environ.items():
    if key[:4] == 'EVE_':
        settings[key[4:]] = value
    elif key[:4] == 'APP_':
        extra_settings[key[4:]] = value

# Eve takes a list of domains for Cross-Origin Resource Sharing.
# We convert the variable value to a list for good measure, in case we need more
# than one domain added
try:
    if settings['X_DOMAINS']:
        settings['X_DOMAINS'] = settings['X_DOMAINS'].split(', ')
except KeyError:
    pass


try:
    if settings['X_EXPOSE_HEADERS']:
        settings['X_EXPOSE_HEADERS'] = settings['X_EXPOSE_HEADERS'].split(', ')
except KeyError:
    pass

# Flask-Sentinel uses seconds as timedelta for the expiration time of tokens.
# We need to convert the environment variable to an integer.
try:
    if settings['OAUTH2_PROVIDER_TOKEN_EXPIRES_IN']:
        settings['OAUTH2_PROVIDER_TOKEN_EXPIRES_IN'] = int(settings['OAUTH2_PROVIDER_TOKEN_EXPIRES_IN'])
except KeyError:
    pass

# Resource availability
settings['DOMAIN'] = {
    'users': resources.users,
    'accounts': resources.accounts,
    'calls': resources.calls,
    'ctm_calls': resources.ctm_calls
}

# Enable reads, inserts, and deletions of resources/collections
settings['RESOURCE_METHODS'] = ['GET', 'POST', 'DELETE']

# Enable reads, edits, and deletetions of individual items
settings['ITEM_METHODS'] = ['GET', 'PATCH', 'DELETE']

