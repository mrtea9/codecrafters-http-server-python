# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Sad")

    # Uncomment this to pass the first stage

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    request = server_socket.accept()[0]
    request_body = request.recv(2028).decode().split("\r\n")
    get_body = request_body[0].split()
    endpoint_body = get_body[1].split("/")
    endpoint_string = endpoint_body[2]
    length = len(endpoint_string)
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n{endpoint_string}".encode()
    request.sendall(response)


if __name__ == "__main__":
    main()
