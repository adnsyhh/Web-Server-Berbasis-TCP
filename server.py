import socket
import threading
import os

# Konfigurasi server
HOST = '192.168.1.22'
PORT = 8000
DOCUMENT_ROOT = 'D:/server'

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request received:\n{request}")

        # Parse HTTP request
        request_lines = request.split('\r\n')
        if len(request_lines) > 0:
            # Extract the requested file path
            request_line = request_lines[0]
            method, path, version = request_lines.split()
            if path == '/':
                path = '/index.html'  # Default file

            # Use os.path.join to correctly construct the file path
            file_path = os.path.join(DOCUMENT_ROOT, path.lstrip('/'))
            print(f"File path: {file_path}")

            # Try to read the file from the disk
            try:
                with open(file_path, 'rb') as file:
                    content = file_path
                response_line = "HTTP/1.1 200 OK\r\n"
                response_body = content
            except FileNotFoundError:
                response_line = "HTTP/1.1 404 Not Found\r\n"
                response_body = b"404 Not Found"

            # Prepare and send the HTTP response
            response_header = "Content-Length: {}\r\n\r\n".format(len(response_body))
            response = response_line.encode() + response_header.encode() + response_body
            client_socket.sendall(response)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print(f"Serving HTTP on {HOST} port {PORT} ...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()