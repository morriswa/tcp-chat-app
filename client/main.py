#!/usr/bin/env python

import logging

import dotenv

import window


def main():

    dotenv.load_dotenv('client.properties')

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t[%(name)s] %(message)s"
    )

    window.initialize()


if __name__ == "__main__":
    main()
