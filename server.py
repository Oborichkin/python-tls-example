import socket
import ssl

from certificate import create_self_signed_cert

HOST = "127.0.0.1"
PORT = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

keyfile, certfile = create_self_signed_cert(name="server")
server = ssl.wrap_socket(server, server_side=True, keyfile=keyfile, certfile=certfile)

if __name__ == "__main__":
    server.bind((HOST, PORT))
    server.listen(0)

    while True:
        print("Waiting for connection")

        connection, client_address = server.accept()
        ip, port = client_address
        print(f"Accepted connection from {ip}:{port}")

        while True:
            data = connection.recv(1024)
            if not data:
                print(f"Connection closed")
                break
            print(f"Received {data.decode('utf-8')}")
