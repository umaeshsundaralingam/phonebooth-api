from flask import Blueprint
from flask import jsonify
from flask import request
from app.tasks import accounts, emails


task = Blueprint('task', __name__)

@task.route('/accounts', methods=['GET'])
def retrieve_new_accounts_trigger():
    task = accounts.retrieve_new.apply_async()
    return jsonify({'task id': task.id})


@task.route('/accounts/<task_id>', methods=['GET'])
def retrieve_new_accounts_status(task_id):
    task = accounts.retrieve_new.AsyncResult(task_id)
    response = {
        'state': task.state,
        'info': str(task.info)
    }
    return jsonify(response)


@task.route('/emails', methods=['POST'])
def send_email_trigger():
    data = list()
    for key, value in request.get_json().items():
        data.append(value)
    task = emails.send.apply_async(args=data)
    return jsonify({'task id': task.id})


@task.route('/emails/<task_id>', methods=['GET'])
def send_email_status(task_id):
    task = emails.send.AsyncResult(task_id)
    response = {
        'state': task.state,
        'info': str(task.info)
    }
    return jsonify(response)
