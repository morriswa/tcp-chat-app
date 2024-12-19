
""" contains data access functions that interact with the database """

import logging

from psycopg2 import errors

import database
from exception import BadRequestException
from models import Chat


log = logging.getLogger(__name__)


def create_account(username, password) -> None:
    """ creates a new account in the database
        :raises BadRequestException: if the username already exists
    """
    with database.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO user_info (username, password)
                VALUES (%(username)s, %(password)s)
            """, {'username': username, 'password': password})
        # thrown if username is already in database
        except errors.UniqueViolation as exc:
            # check that error is user_info_pkey
            if 'user_info_pkey' in str(exc):
                # user friendly error message
                raise BadRequestException("There is already an account with that username")


def login(username, provided_password) -> None:
    """ attempts to verify a users login
        :raises BadRequestException: if the username/password combination doesn't match
    """
    with database.cursor() as cur:
        cur.execute("""
            SELECT password FROM user_info WHERE username = %(username)s
        """, {'username': username})
        res = cur.fetchone()
        if res is not None:
            actual_password = res['password']

            # compare database password to user provided password
            if actual_password != provided_password:
                # throw user-friendly error if passwords dont match
                raise BadRequestException('Bad password')

            # if user authenticated successfully, update last-login
            cur.execute("""
                UPDATE user_info SET last_login = current_timestamp WHERE username = %(username)s
            """, {'username': username, })
        else:
            # throw user-friendly error if username was not found in the database
            raise BadRequestException('No user found')


def get_online_users() -> list[str]:
    """ retrieve all users that were online in the last 5 minutes """
    with database.cursor() as cur:
        cur.execute("""
            SELECT username FROM user_info 
            WHERE last_login > current_timestamp - INTERVAL '5 minutes'
        """)
        return [r["username"] for r in cur.fetchall()]


def send_message(uname_from, uname_to, message) -> None:
    """ adds database entry for new message """
    with database.cursor() as cur:
        cur.execute("""
            insert into user_chat_log (uname_from, uname_to, message)
            values (%(uname_from)s, %(uname_to)s, %(message)s)
        """, {'uname_from': uname_from, 'uname_to': uname_to, 'message': message})


def get_chat_history(uname_from, uname_to) -> list[Chat]:
    """ retrieves full chat log """
    with database.cursor() as cur:
        # retrieve all messages sent by the user to the recipient
        cur.execute("""
            select * from user_chat_log
            where   uname_from = %(uname_from)s
            and     uname_to = %(uname_to)s
        """, {'uname_from': uname_from, 'uname_to': uname_to})
        sent_messages = cur.fetchall()

        # retrieve all messages sent by the recipient to the user
        cur.execute("""
            select * from user_chat_log
            where   uname_to = %(uname_from)s
            and     uname_from = %(uname_to)s
        """, {'uname_from': uname_from, 'uname_to': uname_to})
        received_messages = cur.fetchall()

        # create list of all messages
        message_history = sent_messages + received_messages
        # sort in ascending order by time sent
        message_history.sort(key=lambda x: x['sent'])
        # convert database rows to Chat datamodels
        return [Chat(**msg) for msg in message_history]


def get_active_chats(username) -> list[str]:
    """ retrieve current users chats """
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
