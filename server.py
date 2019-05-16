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
    from time import sleep
    import select

    print(f"Serving server on {HOST}:{PORT}")
    server.bind((HOST, PORT))
    server.listen(1)

    while True:
        print("Waiting for connections")
        connection, client_address = server.accept()

        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        while True:
            r, w, x = select.select([connection], [connection], [connection])
            if r:
                data = r[0].recv(1024)
                if not data:
                    break
                print(f"Received {data.decode('utf-8')}")
