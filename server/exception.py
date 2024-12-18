
class BadRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "msg": self.message,
        }
