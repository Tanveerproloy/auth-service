from flask import Blueprint, jsonify
from app.services.db import get_connection, get_cursor
from app.services.cache import redis_client
from app.controllers.auth_controller import AuthController
from app.middleware import authenticate

# Create the blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health", methods=["GET"])
def health():
    health_status = {
        "status": "ok",
        "db":     "disconnected",
        "redis":  "disconnected"
    }
    http_code = 200

    try:
        connection = get_connection()
        cursor     = get_cursor(connection)
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        health_status["db"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["db"]     = f"error: {str(e)}"
        http_code = 503

    try:
        response = redis_client.ping()
        if response:
            health_status["redis"] = "connected"
        else:
            raise Exception("Ping returned False")
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["redis"]  = f"error: {str(e)}"
        http_code = 503

    return jsonify(health_status), http_code


@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthController.register()


@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()

@auth_bp.route("/profile", methods=["GET"])
@authenticate
def profile():
    return jsonify({
        "status":  "success",
        "message": "Token is valid",
        "data": {
            "user_id": g.user_id,
            "email":   g.email
        }
    }), 200