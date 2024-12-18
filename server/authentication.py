
import base64

import daos
from exception import BadRequestException


def authenticate(request):
    auth = request.get('authentication')
    if auth is None:
        raise BadRequestException('authentication field is missing')

    if not auth.startswith('Basic '):
        raise BadRequestException('Invalid Basic Authentication field')

    encoded_credentials = auth[6:]  # Remove 'Basic ' prefix
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

    username, provided_password = decoded_credentials.split(':', 1)

    daos.login(username, provided_password)

    return username
