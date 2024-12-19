
import logging

from psycopg2 import errors

import database
from exception import BadRequestException
from models import Chat

log = logging.getLogger(__name__)


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


def send_message(uname_from, uname_to, message):
    with database.cursor() as cur:
        cur.execute("""
            insert into user_chat_log (uname_from, uname_to, message)
            values (%(uname_from)s, %(uname_to)s, %(message)s)
        """, {'uname_from': uname_from, 'uname_to': uname_to, 'message': message})


def get_chat_history(uname_from, uname_to):
    with database.cursor() as cur:
        cur.execute("""
            select * from user_chat_log
            where   uname_from = %(uname_from)s
            and     uname_to = %(uname_to)s
        """, {'uname_from': uname_from, 'uname_to': uname_to})
        sent_messages = cur.fetchall()

        cur.execute("""
            select * from user_chat_log
            where   uname_to = %(uname_from)s
            and     uname_from = %(uname_to)s
        """, {'uname_from': uname_from, 'uname_to': uname_to})
        received_messages = cur.fetchall()

        message_history = sent_messages + received_messages
        message_history.sort(key=lambda x: x['sent'])
        return [Chat(**msg) for msg in message_history]


def get_active_chats(username):
    with database.cursor() as cur:
        cur.execute("""
                   select uname_to as username from user_chat_log
                   where  uname_from = %(uname_from)s
               """, {'uname_from': username})
        users_one = cur.fetchall()

        cur.execute("""
                   select uname_from as username from user_chat_log
                   where  uname_to = %(uname_to)s
               """, {'uname_to': username})
        users_two = cur.fetchall()

        user_rows = users_one + users_two
        return list({r["username"] for r in user_rows})
