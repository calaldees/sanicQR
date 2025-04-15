from io import BytesIO
import base64

import qrcode
import sanic
from qrcode.image.pure import PyPNGImage

app = sanic.Sanic("QR")


def get_qr_png_bytes(data: str) -> bytes:
    buffer = BytesIO()
    qrcode.make(data, image_factory=PyPNGImage).save(buffer)
    return buffer.getvalue()


def get_qr_png_base64(data: str) -> bytes:
    return b"data:image/png;base64," + base64.encodebytes(
        get_qr_png_bytes(data)
    ).replace(b"\n", b"")


@app.get("/")
async def root(request: sanic.Request) -> sanic.HTTPResponse:
    return sanic.response.text("/png?data=xxx or /png_base64?data=xxx")


@app.get("/png")
async def qr_png(request: sanic.Request) -> sanic.HTTPResponse:
    data = request.args.get("data", "")
    return sanic.response.raw(get_qr_png_bytes(data), content_type="image/png")


@app.get("/png_base64")
async def qr_base64(request: sanic.Request) -> sanic.HTTPResponse:
    data = request.args.get("data", "")
    return sanic.response.raw(get_qr_png_base64(data), content_type="text/plain")
