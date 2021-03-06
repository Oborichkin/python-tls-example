import socket
import ssl

from server import HOST as SERVER_HOST
from server import PORT as SERVER_PORT
from certificate import create_self_signed_cert

HOST = "127.0.0.1"
PORT = 60002

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

keyfile, certfile = create_self_signed_cert()
client = ssl.wrap_socket(client, keyfile=keyfile, certfile=certfile)

if __name__ == "__main__":
    client.bind((HOST, PORT))
    client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        from time import sleep

        client.send("Hello World!".encode("utf-8"))
        sleep(1)

