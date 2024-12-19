
import base64
import json
import logging
import socket
import os
from typing import Any

import context
from exception import ServerException

BUFFER = 10_000_000
SERVER_IP = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5678'))

log = logging.getLogger(__name__)


def send_tcp_request(message: str) -> dict[str, Any]:
    """ sends a tcp request to configured server """

    # create socket and connect to requested server at correct port
    # https://docs.python.org/3/howto/sockets.html
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    # send encoded message
    client_socket.sendall(message.encode())
    # get encoded response
    response = client_socket.recv(BUFFER)
    # close client connection
    client_socket.close()
    # decode response and return dict
    return json.loads(response.decode())


def create_token(username: str, password: str) -> str:
    decoded_credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(decoded_credentials.encode())
    return f"Basic {encoded_credentials.decode()}"


def verify_credentials(username: str, password: str) -> bool:
    """ verifies provided login credentials
        :returns bool indicating if credentials were valid
    """
    # create token
    token = create_token(username, password)
    # create health request
    request = {
        "authentication": token,
        "action": "health"
    }
    # send request
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":  # if server response was ok, credentials are valid
        log.info(f"successfully logged in as {username}")
        # set token in global context
        context.set_token(token)
        return True
    else:
        # if server returns error response or other, credentials were invalid
        log.info(f"failed to login as {username}")
        return False


def create_account(username, password):
    token = create_token(username, password)
    request = {
        "action": "create_account",
        "body": {
            "username": username,
            "password": password,
        }
    }
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":
        log.info(f"successfully created account with username {username}")
        context.set_token(token)
        return True
    else:
        raise ServerException(response["msg"])


def get_online_users():
    request = {
        "authentication": context.get_token(),
        "action": "online_users",
    }
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":
        # print(response_data["body"])
        return response["body"]
    else:
        raise ServerException(response["msg"])


def get_active_chats():
    request = {
        "action": "active_chats",
        "authentication": context.get_token(),
    }
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":
        return response["body"]
    else:
        raise ServerException(response["msg"])


def view_chat(username):
    request = {
        "action": "view_chat",
        "authentication": context.get_token(),
        "body": {
            "username": username,
        }
    }
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":
        # print(response_data["body"])
        return response["body"]
    else:
        raise ServerException(response["msg"])


def send_message(recipient, message):
    request = {
        "action": "send_message",
        "authentication": context.get_token(),
        "body": {
            "username": recipient,
            "message": message,
        }
    }
    response = send_tcp_request(json.dumps(request))

    if response["status"] == "ok":
        return response["body"]
    else:
        raise ServerException(response["msg"])
