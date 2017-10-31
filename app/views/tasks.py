from flask import Blueprint
from flask import jsonify
from flask_sentinel import oauth
from app.tasks.accounts import retrieve_new_accounts

task = Blueprint('task', __name__)

@task.route('/accounts', methods=['GET'])
@oauth.require_oauth()
def retrieve_new_accounts_trigger():
    task = retrieve_new_accounts.apply_async()
    return jsonify({'task_id': task.id})


@task.route('/accounts/<task_id>', methods=['GET'])
@oauth.require_oauth()
def retrieve_new_accounts_status(task_id):
    task = retrieve_new_accounts.AsyncResult(task_id)
    response = {
        'state': task.state,
        'info': str(task.info)
    }
    return jsonify(response)

