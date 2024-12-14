#!/usr/bin/env python

import logging

import dotenv

import database as db


def main():

    with db.cursor() as cur:
        cur.execute("insert into username_password(username, password) values ('username50000', 'password')")
        cur.execute("insert into username_password(username, password) values ('username5', 'password')")


def init():
    logging.basicConfig(level=logging.DEBUG)
    try:
        dotenv.load_dotenv('server.properties')

        with db.init_db():
            main()

    except Exception as e:
        logging.debug('exiting with errors...', exc_info=e)


if __name__ == "__main__":
    init()
