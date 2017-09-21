import bcrypt
from eve.auth import BasicAuth
from flask import current_app


class RolesAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        users = current_app.data.driver.db['users']
        lookup = {'username': username }
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        user = users.find_one(lookup)
        return user and \
            bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8')

