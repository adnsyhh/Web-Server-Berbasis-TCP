import socket
import sys
import threading

def send_request(server_host, server_port, path):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))

        # Ensure the path starts with a "/"
        if not path.startswith("/"):
            path = "/" + path

        # Send HTTP GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())

        # Receive response from the server
        response = b""
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part

        # Print the response
        print(response.decode())

    finally:
        # Close the connection
        client_socket.close()

def send_multiple_requests(server_host, server_port, path, num_requests):
    # Create a thread for each request
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request, args=(server_host, server_port, path))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <server_host> <server_port> <path> <num_requests>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    path = sys.argv[3]
    num_requests = int(sys.argv[4])

    # Send single/multiple requests to the server
    send_multiple_requests(server_host, server_port, path, num_requests)