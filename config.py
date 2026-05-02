import os
from dotenv import load_dotenv

#load all variables from.env into script
load_dotenv()
class Config:
    #Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    
    #Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")
    
    ## Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL")
    
    # Server
    PORT = int(os.getenv("PORT", 5000))
    
    @staticmethod
    def validate():
        """Call this on startup — crashes early if anything critical is missing"""
        required = ["SECRET_KEY", "JWT_SECRET", "DATABASE_URL", "REDIS_URL"]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise EnvironmentError(f"Missing required env variables: {missing}")