from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@sock.route('/chat')
def echo(sock):
    clients.append(sock)
    while True:
        data = sock.receive()
        for client in clients:
            if client != sock:
                client.send(data)

if __name__ == '__main__':
  app.run(debug=True)