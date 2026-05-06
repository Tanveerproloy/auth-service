from flask import request, jsonify
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access_token,
    logout_user
)


def validate_registration_input(data: dict) -> list:

    errors = []

    if not data.get("email"):
        errors.append("Email is required")
    elif "@" not in data["email"] or "." not in data["email"]:
        errors.append("Email format is invalid")

    if not data.get("password"):
        errors.append("Password is required")
    elif len(data["password"]) < 8:
        errors.append("Password must be at least 8 characters")

    return errors

def validate_login_input(data: dict) -> list:

    errors = []

    if not data.get("email"):
        errors.append("Email is required")

    if not data.get("password"):
        errors.append("Password is required")

    return errors


class AuthController:

    @staticmethod
    def register():
        #Parse JSON body
        data = request.get_json()

        if not data:
            return jsonify({
                "status":  "error",
                "message": "Request body must be JSON"
            }), 400

        #Validate input
        errors = validate_registration_input(data)

        if errors:
            return jsonify({
                "status":  "error",
                "message": "Validation failed",
                "errors":  errors
            }), 422

        #Call the service
        try:
            result = register_user(
                email    = data["email"].lower().strip(),
                password = data["password"]
            )
            return jsonify({
                "status":  "success",
                "message": "Registration successful",
                "data":    result
            }), 201

        except ValueError as e:
            # Expected errors (email taken etc.)
            return jsonify({
                "status":  "error",
                "message": str(e)
            }), 409

        except Exception as e:
            # Unexpected errors
            return jsonify({
                "status":  "error",
                "message": "Internal server error"
            }), 500
            
    @staticmethod
    def login():
        #Parse JSON body
        data = request.get_json()

        if not data:
            return jsonify({
                "status":  "error",
                "message": "Request body must be JSON"
            }), 400

        #Validate input
        errors = validate_login_input(data)

        if errors:
            return jsonify({
                "status":  "error",
                "message": "Validation failed",
                "errors":  errors
            }), 422

        #Call the service
        try:
            result = login_user(
                email    = data["email"].lower().strip(),
                password = data["password"]
            )
            return jsonify({
                "status":  "success",
                "message": "Login successful",
                "data":    result
            }), 200

        except ValueError as e:
            # Wrong email or password
            return jsonify({
                "status":  "error",
                "message": str(e)
            }), 401

        except Exception:
            return jsonify({
                "status":  "error",
                "message": "Internal server error"
            }), 500
            
    @staticmethod
    def refresh():

        data = request.get_json()

        if not data or not data.get("refresh_token"):
            return jsonify({
                "status":  "error",
                "message": "refresh_token is required"
            }), 400

        try:
            result = refresh_access_token(data["refresh_token"])
            return jsonify({
                "status":  "success",
                "message": "Token refreshed successfully",
                "data":    result
            }), 200

        except ValueError as e:
            return jsonify({
                "status":  "error",
                "message": str(e)
            }), 401

        except Exception:
            return jsonify({
                "status":  "error",
                "message": "Internal server error"
            }), 500

    @staticmethod
    def logout():
        try:
            logout_user(g.user_id)
            return jsonify({
                "status":  "success",
                "message": "Logged out successfully"
            }), 200

        except Exception:
            return jsonify({
                "status":  "error",
                "message": "Internal server error"
            }), 500