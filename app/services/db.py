import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_connection():
    connection = psycopg2.connect(
        Config.DATABASE_URL,
        cursor_factory=RealDictCursor
    )
    return connection


def get_cursor(connection):

    return connection.cursor()


def test_connection():
    try:
        connection = get_connection()
        cursor = get_cursor(connection)

        # asks PostgreSQL for its version
        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        print("PostgreSQL connected successfully")
        print(f"{result['version']}")

        cursor.close()
        connection.close()

    except Exception as e:
        print("PostgreSQL connection failed")
        print(f"Error: {e}")
        raise SystemExit(1)  # stop the app immediately