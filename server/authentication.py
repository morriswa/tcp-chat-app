
""" contains backend authentication logic """

import base64

import daos
from exception import BadRequestException


def authenticate(request):
    """ authenticates a tcp request obj via authentication field """
    auth = request.get('authentication')
    if auth is None:
        raise BadRequestException('authentication field is missing')

    if not auth.startswith('Basic '):
        raise BadRequestException('invalid authentication field')

    encoded_credentials = auth[6:]  # remove prefix from authentication field
    # decode base64 creds
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    # and retrieve username and password
    username, provided_password = decoded_credentials.split(':', 1)

    # attempt database authentication
    daos.login(username, provided_password)

    # return verified username
    return username
