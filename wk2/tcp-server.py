import socketserver

class SimpleHandler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    print("{} wrote:".format(self.client_address[0]))
    print(self.data)
    self.request.sendall(self.data.upper())

HOST, PORT = "localhost", 12345
with socketserver.TCPServer((HOST, PORT), SimpleHandler) as server:
    server.serve_forever()