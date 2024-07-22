# Uncomment this to pass the first stage
import socket
from _thread import *
import threading


OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()


def threaded(c, addr):
    print(f"Handling new connection from {addr}")
    while True:
        print("Da")
        print(c)
        print("Da2")
        data = c.recv(1024).decode()
        print(data)
        print("Da3")
        c.close()


def main():

    print("Sad")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)

    while True:
        c, addr = server_socket.accept()
        print(c)
        print('Connected to :', addr[0], ':', addr[1])
        thread = threading.Thread(target=threaded, args=(c, addr))
        thread.start()
        print(threading.active_count() - 1)

        request_body = c.recv(1024).decode().split("\r\n")
        get_body = request_body[0].split()
        endpoint_body = get_body[1].split("/")
        print(request_body)

        # if endpoint_body[1] == 'echo':
        #     endpoint_string = endpoint_body[2]
        #     length = len(endpoint_string)
        #     response = f"HTTP/1.1 200 OK\r\n" \
        #                f"Content-Type: text/plain\r\n" \
        #                f"Content-Length: {length}\r\n\r\n" \
        #                f"{endpoint_string}".encode()
        # elif endpoint_body[1] == 'user-agent':
        #     user_agent_body = request_body[2].split()
        #     user_agent_string = user_agent_body[1]
        #     length = len(user_agent_string)
        #     response = f"HTTP/1.1 200 OK\r\n" \
        #                f"Content-Type: text/plain\r\n" \
        #                f"Content-Length: {length}\r\n\r\n" \
        #                f"{user_agent_string}".encode()
        # elif endpoint_body[1] == '':
        #     response = OK_RESPONSE
        # else:
        #     response = NOTFOUND_RESPONSE
        #
        # request.sendall(response)


if __name__ == "__main__":
    main()
