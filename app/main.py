# Uncomment this to pass the first stage
import socket
from _thread import *
import threading


OK_RESPONSE = "HTTP/1.1 200 OK\r\n\r\n".encode()
NOTFOUND_RESPONSE = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

print_lock = threading.Lock()


def threaded(c):
    print("Da")
    while True:

        data = c.recv(1024)
        if not data:
            print("Bye")
            print_lock.release()
            break

        print(data)

    c.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Sad")

    # Uncomment this to pass the first stage

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    request = server_socket.accept()[0]
    print_lock.acquire()
    start_new_thread(threaded, (request,))
    request_body = request.recv(2028).decode().split("\r\n")
    get_body = request_body[0].split()
    endpoint_body = get_body[1].split("/")
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
    elif endpoint_body[1] == '':
        response = OK_RESPONSE
    else:
        response = NOTFOUND_RESPONSE
    request.sendall(response)


if __name__ == "__main__":
    main()
