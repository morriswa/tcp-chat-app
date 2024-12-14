
import os
import logging
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

log = logging.getLogger(__name__)

db_connection: Any = None


class init_db:
    def __enter__(self):
        """ initializes application db context """
        global db_connection
        if db_connection is not None:
            raise RuntimeError("database connection ALREADY been initialized")
        db_connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        log.debug('opened connection to db')
        return db_connection

    def __exit__(self, exc_type, exc_value, traceback):
        """ destroys application db context """
        global db_connection

        db_connection.close()
        db_connection = None

        if exc_type is not None:
            log.debug('closed connection to db with errors')
        else:
            log.debug('closed connection to db')


class cursor:

    def __init__(self):
        self.__cursor: Any = None

    def __enter__(self):
        """ MUST be run within database context """
        global db_connection
        if db_connection is None:
            raise RuntimeError("database connection has not been initialized")
        self.__cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        log.debug('begin transaction')
        return self.__cursor

    def __exit__(self, exc_type, exc_value, traceback):
        global db_connection
        if db_connection is None:
            raise RuntimeError("database connection has not been initialized")

        if exc_type is not None:
            log.error('encountered error while committing transaction', exc_info=exc_value)
            db_connection.rollback()
            log.debug('transaction rollback complete')
        else:
            db_connection.commit()
            log.debug('transaction committed')

        self.__cursor = None
        return True


def init_db_tables():
    with cursor() as cur:
        cur.execute("""
            create table if not exists username_password (
                username varchar(256) primary key,
                password varchar(256) not null
            );
        """)
