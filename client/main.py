#!/usr/bin/env python

__author__ = "William Morris [morriswa]"

import logging

import dotenv

import window


def main():
    # load client properties into environment
    dotenv.load_dotenv('client.properties')
    # initialize logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t[%(name)s] %(message)s"
    )
    # initialize gui
    window.initialize()


if __name__ == "__main__":
    main()
