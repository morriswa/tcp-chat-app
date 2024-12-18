#!/usr/bin/env python

import logging
import signal

import dotenv

import database as db
from server import start_tcp_server, stop_tcp_server
from database import init_db_tables


def handle_interrupt(s, f):
    logging.info("Received keyboard interrupts signal, exiting.")
    try:
        # cleanup
        stop_tcp_server()
        # term
        exit(0)
    except Exception as exc:
        logging.error("Error occurred during cleanup", exc_info=exc)
        exit(1)


def main():
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t[%(name)s] %(message)s"
    )
    try:
        dotenv.load_dotenv('server.properties')

        with db.init_db():
            init_db_tables()
            start_tcp_server()
    except Exception as e:
        logging.error('exiting with errors...', exc_info=e)


if __name__ == "__main__":
    main()
