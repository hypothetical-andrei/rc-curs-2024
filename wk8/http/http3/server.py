import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

class HttpServerProtocol:
    def __init__(self, stream_handler):
        self.stream_handler = stream_handler

    async def stream_received(self, stream_id, data, fin):
        await self.stream_handler(stream_id, data, fin)

async def handle_stream(stream_id, data, fin):
    print(f"Received stream {stream_id}: {data.decode()}")
    # Here you would parse HTTP/3 headers etc., for now just echo back
    return

async def main():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = await serve(
        host="127.0.0.1",
        port=4433,
        configuration=configuration,
        create_protocol=lambda: HttpServerProtocol(handle_stream),
    )

    # 🔥 Keep running forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
