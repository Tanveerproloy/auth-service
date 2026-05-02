from flask import Flask 
from config import Config

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["DEBUG"] = Config.DEBUG
    app.config["DATABASE_URL"] = Config.DATABASE_URL
    app.config["REDIS_URL"] = Config.REDIS_URL
    
    #Shows error if anything missing
    Config.validate()
    
    #test database connection
    from app.services.db import test_connection
    test_connection()
    
    #test Redis connection
    from app.services.cache import test_connection as test_redis
    test_redis()
    
    #register blueprints
    _register_blueprints(app)
    
    return app
    
def _register_blueprints(app):
    # Import here, not top level, to avoid circular imports
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")