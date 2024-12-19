
""" contains datamodels used through the application """


class Chat:
    def __init__(self, **kwargs):
        self.uname_from = kwargs.get('uname_from')
        self.uname_to = kwargs.get('uname_to')
        self.sent = kwargs.get('sent')
        self.message = kwargs.get('message')

    def json(self):
        return {
            **vars(self),
            'sent': str(self.sent),
        }
