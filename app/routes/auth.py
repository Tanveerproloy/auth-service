from flask import Blueprint, jsonify

# Create the blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    return jsonify({
        "message": "register route works",
        "status": "ok"
    }), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({
        "message": "login route works",
        "status": "ok"
    }), 200


@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "auth-service"
    }), 200