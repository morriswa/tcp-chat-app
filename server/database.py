
import os
import logging
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

import context

log = logging.getLogger(__name__)


class init_db:
    def __enter__(self):
        """ initializes application db context """
        conn = context.get_db_connection()
        if conn is not None:
            raise RuntimeError("database connection ALREADY been initialized")
        context.set_db_connection(psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        ))
        log.debug('opened connection to db')
        return context.get_db_connection()

    def __exit__(self, exc_type, exc_value, traceback):
        """ destroys application db context """
        conn = context.get_db_connection()
        if conn is not None:
            conn.close()
        context.set_db_connection(None)

        if exc_type is not None and not isinstance(exc_value, SystemExit):
            log.debug('closed connection to db with errors')
        else:
            log.debug('closed connection to db')


class cursor:

    def __init__(self):
        self.__cursor: Any = None

    def __enter__(self):
        """ MUST be run within database context """
        conn = context.get_db_connection()
        if conn is None:
            raise RuntimeError("database connection has not been initialized")
        self.__cursor = conn.cursor(cursor_factory=RealDictCursor)
        log.debug('begin transaction')
        return self.__cursor

    def __exit__(self, exc_type, exc_value, traceback):
        conn = context.get_db_connection()
        if conn is None:
            raise RuntimeError("database connection has not been initialized")

        if exc_type is not None:
            log.error('encountered error while committing transaction, attempting rollback')
            conn.rollback()
            log.debug('transaction rollback complete')
            self.__cursor = None
            return False
        else:
            conn.commit()
            log.debug('transaction committed')
            self.__cursor = None
            return True


def create_tables():
    with cursor() as cur:
        cur.execute("""
            create table if not exists user_info (
                username varchar(256) primary key,
                password varchar(256) not null,
                last_login timestamp not null default current_timestamp
            );
            
            create table if not exists user_chat_logs (
                chat_id bigint primary key,
                user_one varchar(256) not null,
                user_two varchar(256) not null,
                chat_log varchar(100000)
            );
        """)
