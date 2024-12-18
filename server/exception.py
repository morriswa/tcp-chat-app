
class ServerException(Exception):
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "msg": "Encountered unexpected server error, please contact your system administrator",
        }


class BadRequestException(ServerException):
    def __init__(self, message):
        super().__init__(message)

    def response(self):
        return {
            "msg": self.message,
        }
