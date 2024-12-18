
import socket
import logging
import json

import context
import authentication
import views

PORT = 5678

log = logging.getLogger(__name__)


def process_request(request):
    try:
        match request.get("action"):
            case "health":
                auth = authentication.authenticate(request)
                return views.hello_world(request.get("body"), auth)
            case "create_account":
                return views.create_account(request)
            case _:
                raise Exception("Invalid request action")
    except Exception as e:
        return views.error(e)


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
    # try:
    server_socket.bind(('0.0.0.0', PORT))
    # except OSError as exc:
    #     if exc.errno == 48:
    #         server_socket.close()

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

        response = json.dumps(process_request(decoded_data))

        # encode time string, send response, and close connection
        client_socket.sendall(response.encode())
        client_socket.close()
        log.info(f'closed connection to {client_address[0]}:{client_address[1]}\n')
