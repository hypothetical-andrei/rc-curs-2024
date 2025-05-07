import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer

class AltSvcRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Alt-Svc', 'h3=":8443"')  # Tell browser: "HTTP/3 available!"
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello from TCP! Please upgrade to HTTP/3</h1></body></html>")

    def log_message(self, format, *args):
        return  # Optional: Suppress logging noise

httpd = HTTPServer(('localhost', 8443), AltSvcRedirectHandler)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving HTTPS with Alt-Svc header on https://localhost:8443 ...")
httpd.serve_forever()
