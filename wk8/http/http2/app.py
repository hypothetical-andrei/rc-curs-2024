async def app(scope, receive, send):
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/html'),
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'<html><body><h1>Hello from Hypercorn HTTP/2!</h1></body></html>',
    })
