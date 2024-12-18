
from typing import Any

__socket: Any = None
__db_connection: Any = None


def get_socket():
    global __socket
    return __socket


def set_socket(conn):
    global __socket
    __socket = conn


def get_db_connection():
    global __db_connection
    return __db_connection


def set_db_connection(conn):
    global __db_connection
    __db_connection = conn
