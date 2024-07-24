# Uncomment this to pass the first stage
import socket
import threading
import sys
import os


OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
CREATED_RESPONSE = "HTTP/1.1 201 Created\r\n\r\n".encode()


def handle_client(client_socket, addr):
    print(f"\nHandling new connection from {addr}")
    message = client_socket.recv(1024).decode()
    response = OK_RESPONSE

    if message:
        request_body = message.split("\r\n")
        method_body = request_body[0].split()
        method = method_body[0]
        endpoint_body = method_body[1].split("/")
        print(request_body)
        print(method_body)
        print(endpoint_body)
        if 'Accept-Encoding' in request_body:
            print("da")

        if method == 'GET':
            if endpoint_body[1] == 'echo':
                endpoint_string = endpoint_body[2]
                length = len(endpoint_string)
                response = f"HTTP/1.1 200 OK\r\n" \
                           f"Content-Type: text/plain\r\n" \
                           f"Content-Length: {length}\r\n\r\n" \
                           f"{endpoint_string}".encode()
            elif endpoint_body[1] == 'user-agent':
                user_agent_body = request_body[2].split()
                user_agent_string = user_agent_body[1]
                length = len(user_agent_string)
                response = f"HTTP/1.1 200 OK\r\n" \
                           f"Content-Type: text/plain\r\n" \
                           f"Content-Length: {length}\r\n\r\n" \
                           f"{user_agent_string}".encode()
            elif endpoint_body[1] == 'files':
                endpoint_string = endpoint_body[2]
                path_file = sys.argv[2] + endpoint_string

                try:
                    with open(path_file, 'r') as file:
                        content = file.read()
                    length = os.path.getsize(path_file)
                    response = f"HTTP/1.1 200 OK\r\n" \
                               f"Content-Type: application/octet-stream\r\n" \
                               f"Content-Length: {length}\r\n\r\n" \
                               f"{content}".encode()
                except FileNotFoundError:
                    response = NOTFOUND_RESPONSE
            elif endpoint_body[1] == '':
                response = OK_RESPONSE
            else:
                response = NOTFOUND_RESPONSE
        elif method == "POST":

            if endpoint_body[1] == 'files':
                endpoint_string = endpoint_body[2]
                path_file = sys.argv[2] + endpoint_string
                content = request_body[5]

                with open(path_file, 'w') as file:
                    file.write(content)

                response = CREATED_RESPONSE

    client_socket.send(response)
    client_socket.close()


def main():

    print("Sad")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"\nActive connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
