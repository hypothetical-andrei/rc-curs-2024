import requests

soap_body = """<?xml version="1.0"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <sayHello xmlns="http://example.com/soap">
      <name>Alice</name>
    </sayHello>
  </soapenv:Body>
</soapenv:Envelope>"""

headers = {'Content-Type': 'text/xml; charset=utf-8'}
response = requests.post("http://localhost:8000", data=soap_body, headers=headers)

print("Response from server:\n", response.text)
