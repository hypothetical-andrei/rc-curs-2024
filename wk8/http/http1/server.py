import socket

def simple_http_server(host='127.0.0.1', port=8080):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Serving HTTP on {host}:{port} ...")

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()

        print("--- Request Start ---")
        print(request.strip())
        print("--- Request End ---")

        # Basic HTTP 1.1 response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            "<html><body><h1>Hello, HTTP1.1!</h1></body></html>"
        )

        client_connection.sendall(response.encode())
        client_connection.close()

if __name__ == "__main__":
    simple_http_server()
