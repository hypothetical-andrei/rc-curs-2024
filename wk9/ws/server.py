from flask import Flask, send_from_directory
from flask_sock import Sock
from PIL import ImageGrab
import io
import base64

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@sock.route('/capture')
def capture(ws):
    while True:
        message = ws.receive()
        if message == "capture":
            # Capture screen
            screenshot = ImageGrab.grab()
            # Convert image to bytes
            with io.BytesIO() as output:
                screenshot.save(output, format="JPEG")
                byte_data = output.getvalue()
            # Encode as base64
            encoded_image = base64.b64encode(byte_data).decode('utf-8')
            # Send to client
            ws.send(encoded_image)

if __name__ == "__main__":
    app.run(debug=True)
