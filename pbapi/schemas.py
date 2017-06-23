# Schemas
user = {
    'email': {
        'type': 'string',
        'regex': "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        'required': True,
        'unique': True
    },
    'firstname' : {
        'type': 'string',
        'required': True
    },
    'lastname': {
        'type': 'string',
        'required': True
    },
    'password': {
        'type': 'string'
    },
    'roles': {
        'type': 'list',
        'required': True,
        'allowed': ['api', 'enduser', 'admin', 'superuser']
    }
}

account = {
    'agency_id': {
        'type': 'integer',
        'required': True
    },
    'balance': {
        'type': 'dict'
    },
    'created': {
        'type': 'date',
        'required': True
    },
    'ctm_id': {
        'type': 'integer',
        'required': True
    },
    'invoiced': {
        'type': 'boolean'
    },
    'name': {
        'type': 'string',
        'required': True
    },
    'shared_billing': {
        'type': 'boolean',
        'required': True
    },
    'stats': {
        'type': 'dict'
    },
    'status': {
        'type': 'string',
        'required': True
    },
    'timezone': {
        'type': 'string',
        'required': True
    },
    'user_role': {
        'type': 'string',
        'allowed': ['agency_admin', 'admin', 'report_manager', 'call_manager', 'agent']
    },
    'website': {
        'type': 'string'
    }
}

call = {
    'ctm_id': {
        'type': 'integer'
    },
    'ctm_account_id': {
        'type': 'integer'
    },
    'account_id': {
        'type': 'objectid',
        'required': True
    }
}

