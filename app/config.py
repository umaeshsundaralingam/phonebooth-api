import os
from app import resources

try:
    # Heroku sets a PORT evironment variable that we can look for.
    # This way, we know if we are on a Heroku ``production`` or ``staging``
    # environment, and let it use the set environment variables
    if os.environ['PORT']:
        pass
except KeyError:
    # or if we are developing locally, then load the .env
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv('.env'))

# Grab global variables and add them to a ``settings`` dictionary to pass on
# to eve; only grabs pre-pended variables starting with "APP_"
settings = dict()

for key, value in os.environ.items():
    if key[:4] == 'APP_':
        settings[key[4:]] = value

# Eve takes a list of domains for Cross-Origin Resource Sharing.
# We convert the variable value to a list for good measure, in case we need more
# than one domain added
try:
    if settings['X_DOMAINS']:
        settings['X_DOMAINS'] = settings['X_DOMAINS'].split(', ')
except KeyError:
    pass

# Resource availability
settings['DOMAIN'] = {
    'users': resources.users,
    'accounts': resources.accounts,
    'calls': resources.calls
}

# Enable reads, inserts, and deletions of resources/collections
settings['RESOURCE_METHODS'] = ['GET', 'POST', 'DELETE']

# Enable reads, edits, and deletetions of individual items
settings['ITEM_METHODS'] = ['GET', 'PATCH', 'DELETE']

