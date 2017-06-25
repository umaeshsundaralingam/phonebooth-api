from app import celery
from app import config
from flask import current_app
import requests

ctm_url = config.settings['CTM_URL']
ctm_auth = (config.settings['CTM_USER'], config.settings['CTM_PASS'])


@celery.task(bind=True)
def retrieve_new_accounts(self):
    """Check CTM's accounts and compare the list to existing accounts in PhoneBooth's
    datastore."""

    # Query CTM and find out how many pages we are dealing with
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
    accounts = current_app.data.driver.db['accounts']
    for account in accounts.find():
        existing_account_ids.append(account['ctm_id'])

    # Compare the lists via list comprehension
    filtered = [id for id in ctm_account_ids if id not in existing_account_ids]

    return filtered

