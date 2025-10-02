from argon2 import PasswordHasher
import argon2
from os import environ
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


def get_db_connection() -> connection:
    """Returns a live connection to the database."""
    return connect(user=environ["DB_USERNAME"],
                   password=environ["DB_PASSWORD"],
                   host=environ["DB_HOST"],
                   port=environ["DB_PORT"],
                   database=environ["DB_NAME"],
                   cursor_factory=RealDictCursor)


def insert_user(conn: connection, user_name: str, user_email: str, password: str):
    ph = PasswordHasher()
    hash = ph.hash(password)
    query = '''insert into users (user_name,user_email, password_hash) values (%s,%s,%s)'''
    with conn.cursor() as cur:
        cur.execute(query, (user_name, user_email, hash))
        conn.commit()


def verify_user(conn: connection, user_name: str, user_password: str):
    ph = PasswordHasher()
    query = '''select password_hash from users where user_name = %s'''
    with conn.cursor() as cur:
        cur.execute(query, (user_name,))
        hash = cur.fetchone()['password_hash']
        try:
            return ph.verify(hash, user_password)
        except argon2.exceptions.VerifyMismatchError:
            return False


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()
    # insert_user(conn, 'test_user_for_password',
    #             'b_yacquub@hotmail.co.uk', 'password')
    print(verify_user(conn, 'test_user_for_password', 'password'))
