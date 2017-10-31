from app import celery
from flask import current_app
from eve.methods.post import post_internal
import requests

@celery.task(bind=True)
def retrieve_new_accounts(self):
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
    missing_ctm_accounts = []

    try:
        for id in filtered_ids:
            r = requests.get(ctm_url + '/accounts/' + str(id) + '.json', auth=ctm_auth)
            with current_app.test_request_context():
                post_internal('accounts', r.json())
            missing_ctm_accounts.append(id)
            del id, r
    except:
        raise

    if len(missing_ctm_accounts):
        n = len(missing_ctm_accounts)
        a = str(missing_ctm_accounts)
        return "{} accounts imported. {}".format(n, a)
    else:
        return "No new accounts to import."

