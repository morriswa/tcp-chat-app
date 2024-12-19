
""" contains exceptions thrown within this application """


class ServerException(Exception):
    """ exception for errors that should be reported to the user in friendly format"""
    def __init__(self, message):
        self.message = message
