#!/usr/bin/env python
import base64
import json
import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5678


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
    print('got ', response.decode())


if __name__ == "__main__":

    username = "william"
    password = "passphrase"

    decoded_credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(decoded_credentials.encode())

    request = {
        "authentication": f"Basic {encoded_credentials.decode()}",
        "action": "health",
    }
    request = {
        "authentication": f"Basic {encoded_credentials.decode()}",
        "action": "online_users",
    }
    # request = {
    #     "action": "create_account",
    #     "body": {
    #         "username": username,
    #         "password": password
    #     }
    # }
    send_tcp_request(json.dumps(request))
