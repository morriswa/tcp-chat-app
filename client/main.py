#!/usr/bin/env python

import logging

import window


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s\t[%(name)s] %(message)s"
    )

    window.initialize()


if __name__ == "__main__":
    main()
