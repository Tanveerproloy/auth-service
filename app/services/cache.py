import redis
from config import Config

redis_client = redis.from_url(
    Config.REDIS_URL,
    decode_responses=True
)

def test_connection():
    #shows error if redis is not reachable
    try:
        response = redis_client.ping()

        if response:
            print("Redis connected successfully")
        else:
            raise Exception("Connection error")

    except Exception as e:
        print("Redis connection failed")
        print(f"Error: {e}")
        raise SystemExit(1)
    
def set_value(key, value, ttl_seconds=None):

    if ttl_seconds:
        redis_client.setex(key, ttl_seconds, value)
    else:
        redis_client.set(key, value)


def get_value(key):
    
    return redis_client.get(key)


def delete_value(key):
 
    redis_client.delete(key)


def key_exists(key):

    return redis_client.exists(key) == 1

# Refresh Token Helpers

REFRESH_TOKEN_TTL = 7 * 24 * 60 * 60  # 7 days in seconds


def store_refresh_token(user_id: str, token: str):

    redis_client.setex(f"refresh:user:{user_id}", REFRESH_TOKEN_TTL, token)
    redis_client.setex(f"refresh:token:{token}",  REFRESH_TOKEN_TTL, user_id)


def get_user_id_from_refresh_token(token: str):
    return redis_client.get(f"refresh:token:{token}")

def get_refresh_token_for_user(user_id: str):
    return redis_client.get(f"refresh:user:{user_id}")

def get_refresh_token(user_id: str):

    key = f"refresh:{user_id}"
    return get_value(key)


def delete_refresh_token(user_id: str):

    redis_client.delete(f"refresh:user:{user_id}")
    redis_client.delete(f"refresh:token:{token}")

def refresh_token_exists(user_id: str) -> bool:

    return redis_client.exists(f"refresh:token:{token}") == 1