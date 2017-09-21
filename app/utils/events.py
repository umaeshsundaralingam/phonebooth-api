import dateutil.parser
from flask import request, current_app

def prepare_documents_for_import_callback(resource, request):
    payload = request.get_json()
    documents = [[payload], payload][type(payload) == list]
    for document in documents.copy():
        date_fields = ['created', 'called_at', 'billed_at', 'call_path']
        for key in date_fields:
            if key in document:
                if key == 'created':
                    document['ctm_created'] = dateutil.parser.parse(document['created'])
                    del document['created']
                elif key == 'call_path':
                    for path in document['call_path']:
                        if 'started_at' in path:
                            path['started_at'] = dateutil.parser.parse(path['started_at'])
                else:
                    document[key] = dateutil.parser.parse(document[key])

        if 'account_id' in document:
            accounts = current_app.data.driver.db['accounts']
            lookup = {'ctm_id': document['account_id']}
            account = accounts.find_one(lookup)
            document['ctm_account_id'] = document['account_id']
            document['account_id'] = account['_id']

        if 'id' in document:
            document['ctm_id'] = document['id']
            del document['id']

        for key in document.copy():
            if "url" in key:
                del document[key]

