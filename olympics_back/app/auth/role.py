# src/auth/role.py

from functools import wraps
from flask import jsonify
from .auth0 import requires_auth  # Import the authentication decorator


def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            payload = requires_auth()(f)(*args, **kwargs)  # Call the requires_auth decorator
            if 'roles' in payload and role in payload['roles']:
                return f(*args, **kwargs)  # Proceed if the user has the required role
            return jsonify({"message": "Unauthorized"}), 403
        return decorated
    return decorator

