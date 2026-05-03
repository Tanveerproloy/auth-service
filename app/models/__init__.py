from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:

    #Mirrors the users table in PostgreSQL.

    id:            str
    email:         str
    password_hash: str
    is_verified:   bool
    created_at:    datetime
    updated_at:    datetime

    @staticmethod
    def from_row(row: dict) -> "User":

        #Converts a database row (dict) into a User object.
        return User(
            id            = str(row["id"]),
            email         = row["email"],
            password_hash = row["password_hash"],
            is_verified   = row["is_verified"],
            created_at    = row["created_at"],
            updated_at    = row["updated_at"]
        )

    def to_dict(self) -> dict:
        #Converts User to a dict safe to return in API responses.

        return {
            "id":          self.id,
            "email":       self.email,
            "is_verified": self.is_verified,
            "created_at":  self.created_at.isoformat(),
            "updated_at":  self.updated_at.isoformat()
        }