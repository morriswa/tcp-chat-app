#!/usr/bin/env python

import logging
import signal

import dotenv

import database as db
from server import start_tcp_server, stop_tcp_server


def handle_interrupt(s, f):
    logging.info(f"received {signal.Signals(s).name}, exiting...")
    try:
        # cleanup
        stop_tcp_server()
        # terminate without errors
        exit(0)
    except Exception as exc:
        logging.error("Error occurred during cleanup", exc_info=exc)
        # terminate with errors
        exit(1)


def main():
    # register signals for safe shutdown
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    # enable logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t[%(name)s] %(message)s"
    )

    try:
        # attempt to create environment from file
        dotenv.load_dotenv('server.properties')

        # create database connection
        with db.init_db():
            # create tables, if they don't already exist
            db.create_tables()
            # start tcp server and begin listening for incoming request from client
            start_tcp_server()

    except Exception as e:
        logging.error('exiting with errors...', exc_info=e)


if __name__ == "__main__":
    main()
