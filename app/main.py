# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Sad")

    # Uncomment this to pass the first stage

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    request = server_socket.accept()[0]
    request_target = request.recv(2028).split()[1]
    if request_target != b'/':
        request.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        print(request_target)
    else:
        request.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        print(request_target)


if __name__ == "__main__":
    main()
