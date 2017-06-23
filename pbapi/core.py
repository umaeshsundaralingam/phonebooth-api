import bcrypt
from eve import Eve
from eve.auth import BasicAuth
from eve.auth import requires_auth
from pbapi import config
from pbapi import tasker
from flask import jsonify
from flask import url_for
import requests

ctm_url = config.settings['CTM_URL']
ctm_auth = (config.settings['CTM_USER'], config.settings['CTM_PASS'])


class RolesAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        users = app.data.driver.db['users']
        lookup = {'email': username }
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        user = users.find_one(lookup)
        return user and \
            bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8')


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
    auth=RolesAuth
)
app.on_pre_POST_calls += reference_call_to_account_callback
celery = tasker.make_celery(app)


@celery.task(bind=True)
def retrieve_new_accounts(self):
    """Check CTM's accounts and compare the list to existing accounts in PhoneBooth's
    datastore."""

    # Make a query to CTM so we know how many pages we are dealing with
    r = requests.get(ctm_url + '/accounts.json', params={'page': 1}, auth=ctm_auth)

    # Get all of of CTM's accounts in an empty list
    ctm_accounts = []
    for page in range(1, r.json()['total_pages'] + 1):
        ctm_accounts.extend(requests.get(ctm_url + '/accounts.json', params={'page': page}, auth=ctm_auth).json()['accounts'])
        del page

    # Grab only the account ids in an empty list
    ctm_account_ids = []
    for account in ctm_accounts:
        ctm_account_ids.append(account['id'])
        del account

    # Retrieve all existing call tracking accounts in PhoneBooth's datastore for
    # comparison before import
    existing_account_ids = []
    accounts = app.data.driver.db['accounts']
    for account in accounts.find():
        existing_account_ids.append(account['ctm_id'])

    # Compare the lists via list comprehension
    filtered = [id for id in ctm_account_ids if id not in existing_account_ids]

    return filtered


@app.route('/tasks/new_accounts', methods=['GET'])
@requires_auth('RolesAuth')
def retrieve_new_accounts_trigger():
    task = retrieve_new_accounts.apply_async()
    return jsonify({'task_id': task.id})


@app.route('/tasks/new_accounts/<task_id>')
@requires_auth('RolesAuth')
def retrieve_new_accounts_status(task_id):
    task = retrieve_new_accounts.AsyncResult(task_id)
    response = {
        'state': task.state,
        'info': str(task.info)
    }
    return jsonify(response)


@celery.task(bind=True)
def import_new_accounts(self):
    pass


@app.route('/tasks/new_accounts', methods=['POST'])
@requires_auth('RolesAuth')
def import_new_accounts_trigger():
    task = import_new_accounts.apply_async()
    return jsonify({'task_id': task.id})
