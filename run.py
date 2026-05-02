from config import Config

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