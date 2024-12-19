
""" contains exceptions thrown within this application """


class BadRequestException(Exception):
    """ exception for errors that should be reported to the user in friendly format"""
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "status": "error",
            "msg": self.message,
        }
