from app import celery
from app.utils.events import prepare_documents_for_import_callback
from flask import request, current_app
from eve.methods.post import post_internal
from eve.render import send_response
import requests, json


@celery.task(bind=True)
def retrieve_new(self):
    """Check CTM's accounts and compare the list to existing accounts in PhoneBooth's
    datastore."""

    ctm_url = current_app.config['CTM_URL']
    ctm_auth = (current_app.config['CTM_USER'], current_app.config['CTM_PASS'])

    # Query CTM and find out how many pages we are dealing with
    r = requests.get(ctm_url + '/accounts.json', params={'page': 1}, auth=ctm_auth)

    # Get a list of all CTM's accounts
    ctm_accounts = []
    for page in range(1, r.json()['total_pages'] + 1):
        ctm_accounts.extend(requests.get(ctm_url + '/accounts.json', params={'page': page}, auth=ctm_auth).json()['accounts'])
        del page

    # Grab only the account ids, as we will have to request each account's full
    # profile information
    ctm_account_ids = []
    for account in ctm_accounts:
        ctm_account_ids.append(account['id'])
        del account

    # Retrieve all existing call tracking accounts in PhoneBooth's datastore for
    # comparison before import
    existing_account_ids = []
    accounts = current_app.data.driver.db['accounts']
    for account in accounts.find():
        existing_account_ids.append(account['ctm_id'])

    # Compare the lists via list comprehension
    filtered_ids = [id for id in ctm_account_ids if id not in existing_account_ids]

    # Query CTM for every missing account's profile and import them
    imported_ctm_accounts = []

    for id in filtered_ids:
        r = requests.get(ctm_url + '/accounts/' + str(id) + '.json', auth=ctm_auth, timeout=3)
        payload = json.dumps(r.json())
        with current_app.test_request_context(path='/accounts', method='POST', content_type='application/json', data=payload):
            try:
                prepare_documents_for_import_callback('accounts', request)
                post_internal('accounts')
                imported_ctm_accounts.append(id)
            except:
                raise

    if len(imported_ctm_accounts):
        n = len(imported_ctm_accounts)
        a = str(imported_ctm_accounts)
        return "{} accounts imported. {}".format(n, a)
    else:
        return "No new accounts to import."

