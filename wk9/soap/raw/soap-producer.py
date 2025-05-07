from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_soap():
    if b'sayHello' in request.data:
        name = "Unknown"
        # Basic XML parsing (very fragile, but fine for a minimal example)
        if b'<name>' in request.data:
            name = request.data.decode().split('<name>')[1].split('</name>')[0]

        response_xml = f"""<?xml version="1.0"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
          <soapenv:Body>
            <sayHelloResponse xmlns="http://example.com/soap">
              <return>Hello, {name}!</return>
            </sayHelloResponse>
          </soapenv:Body>
        </soapenv:Envelope>"""

        return Response(response_xml, content_type='text/xml')

    return Response("Invalid SOAP action", status=500)

if __name__ == '__main__':
    app.run(port=8000)
