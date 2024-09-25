# src/auth/auth0.py

from functools import wraps
from flask import request, jsonify
from jose import jwt
import urllib.request
import json

# Configuration de Auth0
# AUTH0_DOMAIN = 
# API_IDENTIFIER = 
# ALGORITHMS = 
# SECRET_KEY = 

def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Exception("Authorization header is expected")

    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Exception("Token not found")
    elif len(parts) > 2:
        raise Exception("Authorization header must be Bearer token")

    token = parts[1]
    return token

# Middleware pour décoder le JWT et vérifier l'autorisation
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urllib.request.urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        if 'kid' not in unverified_header:
            return jsonify({"message": "Authorization malformed."}), 401

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer=f"https://{AUTH0_DOMAIN}/"
                )
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expired."}), 401
            except jwt.JWTClaimsError:
                print("Token:", token)
                print("Unverified Header:", unverified_header)
                print("RSA Key:", rsa_key)
                return jsonify({"message": "Incorrect claims."}), 401
            except Exception:
                return jsonify({"message": "Unable to parse authentication token."}), 400

            return f(payload, *args, **kwargs)
        return jsonify({"message": "Unable to find appropriate key."}), 400

    return decorated


