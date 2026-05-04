import bcrypt
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from app.services.db import get_connection, get_cursor
from app.services.cache import store_refresh_token
from app.models import User
from config import Config


# ── Password Helpers ───────────────────────────────────────────


def hash_password(plain_text: str) -> str:
#password hashing
    salt           = bcrypt.gensalt(rounds=12)
    hashed         = bcrypt.hashpw(plain_text.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_text: str, hashed: str) -> bool:

    #Checks if a plain text password matches a stored hash.
    return bcrypt.checkpw(
        plain_text.encode("utf-8"),
        hashed.encode("utf-8")
    )


# ── Token Helpers ──────────────────────────────────────────────


def generate_access_token(user_id: str, email: str) -> str:

    #Generates a short-lived JWT access token (15 minutes).
    payload = {
        "sub":   user_id,
        "email": email,
        "iat":   datetime.now(timezone.utc),
        "exp":   datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    token = jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm="HS256"
    )
    return token


def generate_refresh_token() -> str:

    #Generates a refresh token
    return str(uuid.uuid4())


#Registration


def register_user(email: str, password: str) -> dict:

    connection = get_connection()
    cursor     = get_cursor(connection)

    try:
        #Check if email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )
        existing = cursor.fetchone()

        if existing:
            raise ValueError("Email is already registered")

        #Hash the password
        password_hash = hash_password(password)

        #Insert new user
        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id, email, is_verified, created_at, updated_at
            """,
            (email, password_hash)
        )
        row  = cursor.fetchone()
        user = User.from_row({
            **row,
            "password_hash": password_hash
        })

        #Commit the insert
        connection.commit()

        #Generate tokens
        access_token  = generate_access_token(user.id, user.email)
        refresh_token = generate_refresh_token()

        # ── Step 6: Store refresh token in Redis ──────────────
        store_refresh_token(user.id, refresh_token)

        # ── Step 7: Return response data ──────────────────────
        return {
            "user":          user.to_dict(),
            "access_token":  access_token,
            "refresh_token": refresh_token
        }

    except Exception:
        # If anything fails, roll back the DB insert
        connection.rollback()
        raise

    finally:
        # Always close cursor and connection
        cursor.close()
        connection.close()