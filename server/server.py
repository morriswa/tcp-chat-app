
import socket
import logging
import json

import context
import authentication
import views
from exception import BadRequestException, ServerException

PORT = 5678

log = logging.getLogger(__name__)


def process_request(request):
    try:
        match request.get("action"):
            case "health":
                auth = authentication.authenticate(request)
                return views.hello_world(request.get("body"), auth)
            case "create_account":
                return views.create_account(request.get("body"))
            case "retrieve_chats":
                pass
            case "view_chat":
                pass
            case "send_message":
                pass
            case "online_users":
                auth = authentication.authenticate(request)
                return views.online_users(request.get("body"), auth)
            case _:
                raise BadRequestException("Invalid request action")
    except ServerException as e:
        return e.response()


def stop_tcp_server():
    soc = context.get_socket()
    if soc is not None:
        soc.close()
    context.set_socket(None)
    log.debug("tcp server closed successfully")


def start_tcp_server():

    # create socket and bind to requested port
    # https://docs.python.org/3/howto/sockets.html
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # https://stackoverflow.com/questions/5875177/how-to-close-a-socket-left-open-by-a-killed-program
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('0.0.0.0', PORT))

    context.set_socket(server_socket)

    # start listening for incoming requests
    server_socket.listen()
    log.info(f'started tcp server on local machine port {PORT}')

    # continue monitoring requests until user quits application
    while True:
        # accept incoming tcp requests
        client_socket, client_address = server_socket.accept()
        log.info(f'opened connection to {client_address[0]}:{client_address[1]}')

        data = client_socket.recv(1024)  # Adjust buffer size as needed

        decoded_data = json.loads(data.decode("utf-8"))
        response_data = process_request(decoded_data)
        response = json.dumps(response_data)

        client_socket.sendall(response.encode())
        client_socket.close()
        log.info(f'closed connection to {client_address[0]}:{client_address[1]}\n')
