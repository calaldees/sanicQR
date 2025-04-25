import base64
from io import BytesIO

import qrcode  # type: ignore[import-untyped]
import sanic
from qrcode.image.pure import PyPNGImage  # type: ignore[import-untyped]

app = sanic.Sanic("QR")


def build_qr_png_bytes(data: str) -> bytes:
    r"""
    >>> png_bytes = build_qr_png_bytes('abc')
    >>> png_bytes.startswith(b'\x89PNG\r\n')
    True
    """
    buffer = BytesIO()
    qrcode.make(data, image_factory=PyPNGImage).save(buffer)
    return buffer.getvalue()


def build_qr_png_base64(data: str) -> bytes:
    """
    >>> build_qr_png_base64('abc')
    b'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAAEiAQAAAAB1xeIbAAABDUlEQVR4nO3YQQ6DIBCF4Uk8AEfi6j1SD2BCYWAUbahdOCRtfhalwufqBUaQ9EV7CAqFQqH+QklrS5JYHuPTRiLKW+lDehaVf/RfN4FyVSWSAkSC+S0w1ByVRzaPmqv6rFBzlHaakK2ObgLlqbqKvMX0sW6j7lIXDeWochCrZRJW0SXS9iiUtypzDRht36QoZ5V7+xCqIGlM62lnQnmolGxNSLAiUVbHMSGUi6pnXh3u96hTQigPZc0S2l9C+SrLZKm1uc0FexXlqaJ2pxu3t4RQLup441YKtAWGmqbahY+0gjBICOWgdE3sh4JBQqg7lXb1xm14CkC5qL0i16+hwRkZdb+6aCgUCoX6efUCVPGJPFhcrgoAAAAASUVORK5CYII='
    """
    return b"data:image/png;base64," + base64.encodebytes(
        build_qr_png_bytes(data)
    ).replace(b"\n", b"")


@app.get("/")
async def root(request: sanic.Request) -> sanic.HTTPResponse:
    return sanic.response.text("/qr_png?data=xxx or /qr_png_base64?data=xxx")


@app.get("/qr_png")
async def qr_png(request: sanic.Request) -> sanic.HTTPResponse:
    data = request.args.get("data", "")
    return sanic.response.raw(build_qr_png_bytes(data), content_type="image/png")


@app.get("/qr_png_base64")
async def qr_png_base64(request: sanic.Request) -> sanic.HTTPResponse:
    data = request.args.get("data", "")
    return sanic.response.raw(build_qr_png_base64(data), content_type="text/plain")
