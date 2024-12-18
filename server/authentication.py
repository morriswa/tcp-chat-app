
import base64


def authenticate(request):
    auth_header = request.get('authentication')
    if auth_header is None:
        raise Exception('authentication is missing')

    if not auth_header.startswith('Basic '):
        raise ValueError('Invalid Basic Authentication header')

    encoded_credentials = auth_header[6:]  # Remove 'Basic ' prefix
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

    username, password = decoded_credentials.split(':', 1)
    return username, password
