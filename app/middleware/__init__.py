import jwt
from functools import wraps
from flask import request, jsonify, g
from config import Config


def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        #Read the Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "status":  "error",
                "message": "Authorization header is missing"
            }), 401

        #Extract the token

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "status":  "error",
                "message": "Authorization header must be: Bearer <token>"
            }), 401

        token = parts[1]

        #Verify the token
        try:
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            # exp timestamp has passed
            return jsonify({
                "status":  "error",
                "message": "Token has expired — please login again"
            }), 401

        except jwt.InvalidSignatureError:
            # Signature doesn't match
            return jsonify({
                "status":  "error",
                "message": "Token signature is invalid"
            }), 401

        except jwt.DecodeError:
            # Token is malformed
            return jsonify({
                "status":  "error",
                "message": "Token is malformed"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "status":  "error",
                "message": "Token is invalid"
            }), 401

        #Attach user data to Flask's g object
        g.user_id = decoded["sub"]
        g.email   = decoded["email"]

        #Call the actual route function
        return f(*args, **kwargs)

    return decorated