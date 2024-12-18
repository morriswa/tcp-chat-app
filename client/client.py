
import base64
import json
import logging
import socket

import context

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5678

log = logging.getLogger(__name__)


def send_tcp_request(message: str):
    # create socket and connect to requested server at correct port
    # https://docs.python.org/3/howto/sockets.html
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    client_socket.sendall(message.encode())

    response = client_socket.recv(1024)

    # close client connection
    client_socket.close()

    # transform response sent time back to datetime obj for calculations
    return response.decode()


def verify_credentials(username: str, password: str):
    decoded_credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(decoded_credentials.encode())
    token = f"Basic {encoded_credentials.decode()}"
    request = {
        "authentication": token,
        "action": "health"
    }
    response = send_tcp_request(json.dumps(request))
    response_data = json.loads(response)

    if response_data["status"] == "ok":
        log.info(f"successfully logged in as {username}")
        context.set_token(token)
        return True
    else:
        log.info(f"failed to login as {username}")
        return False


def create_account(username, password):
    decoded_credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(decoded_credentials.encode())
    token = f"Basic {encoded_credentials.decode()}"
    request = {
        "action": "create_account",
        "body": {
            "username": username,
            "password": password,
        }
    }
    response = send_tcp_request(json.dumps(request))
    response_data = json.loads(response)

    if response_data["status"] == "ok":
        log.info(f"successfully created account with username {username}")
        context.set_token(token)
        return True, None
    else:
        log.error(response_data['msg'])
        return False, response_data['msg']
