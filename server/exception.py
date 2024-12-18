
class BadRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "status": "error",
            "msg": self.message,
        }
