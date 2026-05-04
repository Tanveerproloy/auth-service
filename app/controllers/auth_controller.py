from flask import request, jsonify
from app.services.auth_service import register_user


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