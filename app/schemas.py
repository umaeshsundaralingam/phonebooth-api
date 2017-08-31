# Cerberus schemas for database modeling
user = {
    'username': {
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
    'roles': {
        'type': 'list',
        'required': True,
        'allowed': ['api', 'enduser', 'manager', 'admin']
    },
    # We have to keep the password field as well as the RolesAuth class for clients
    # which only support basic authentication (a.k.a. CTM)
    'password': {
        'type': 'string',
        'required': False
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
        'type': 'string',
        'required': True
    },
    'id': {
        'type': 'integer',
        'required': True,
        'unique': True
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
