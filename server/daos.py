
from psycopg2 import errors

import database
from exception import BadRequestException


def create_account(username, password):
    with database.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO user_info (username, password)
                VALUES (%(username)s, %(password)s)
            """, {'username': username, 'password': password})
        except errors.UniqueViolation as exc:
            if 'user_info_pkey' in str(exc):
                raise BadRequestException("There is already an account with that username")


def login(username, provided_password):
    with database.cursor() as cur:
        cur.execute("""
            SELECT password FROM user_info WHERE username = %(username)s
        """, {'username': username,})
        res = cur.fetchone()
        if res is not None:
            actual_password = res['password']
            if actual_password != provided_password:
                raise BadRequestException('Bad password')

            cur.execute("""
                UPDATE user_info SET last_login = current_timestamp WHERE username = %(username)s
            """, {'username': username, })
        else:
            raise BadRequestException('No user found')


def get_online_users():
    with database.cursor() as cur:
        cur.execute("""
            SELECT username FROM user_info 
            WHERE last_login > current_timestamp - INTERVAL '5 minutes'
        """)
        return [r["username"] for r in cur.fetchall()]
