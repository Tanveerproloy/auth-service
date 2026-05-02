from config import Config
from app import create_app

# Validate env variables on startup
Config.validate()

print("SECRET_KEY loaded:", bool(Config.SECRET_KEY))
print("JWT_SECRET loaded:", bool(Config.JWT_SECRET))
print("DATABASE_URL loaded:", bool(Config.DATABASE_URL))
print("REDIS_URL loaded:", bool(Config.REDIS_URL))
print("PORT:", Config.PORT)
print("DEBUG:", Config.DEBUG)
print("")
print("All environment variables loaded successfully")

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",    # accept connections from any IP
        port=Config.PORT,  # reads from .env (5000)
        debug=Config.DEBUG # reads from .env (True in development)
    )