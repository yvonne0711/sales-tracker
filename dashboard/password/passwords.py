"""Script to encrypt passwords and verify users."""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from psycopg2.extensions import connection


def insert_user(conn: connection, user_name: str, user_email: str, password: str) -> None:
    """This function hashes the password and adds user details to the database."""
    password_hasher = PasswordHasher()
    hashed = password_hasher.hash(password)
    query = """
            INSERT INTO users 
                (user_name,user_email, password_hash) 
            VALUES 
                (%s,%s,%s)
            """
    with conn.cursor() as cur:
        cur.execute(query, (user_name, user_email, hashed))
        conn.commit()


def verify_user(conn: connection, user_email: str) -> bool:
    """Function to verify user."""
    query = """
            SELECT * 
            FROM users 
            WHERE user_email = %s"""
    with conn.cursor() as cur:
        cur.execute(query, (user_email,))
        hashed = cur.fetchone()
        if hashed is None:
            return False
        return True


def verify_user_password(conn: connection, user_email: str, user_password: str) -> bool:
    """Function to verify user password."""
    password_hasher = PasswordHasher()
    query = """
            SELECT password_hash 
            FROM users 
            WHERE user_email = %s"""
    with conn.cursor() as cur:
        cur.execute(query, (user_email,))
        hashed = cur.fetchone()
        if hashed is None:
            return False
        try:
            return password_hasher.verify(hashed["password_hash"], user_password)
        except VerifyMismatchError:
            return False
