from io import BytesIO

import qrcode
import sanic
from qrcode.image.pure import PyPNGImage

app = sanic.Sanic("QR")


@app.get("/")
async def qr(request):
    data = request.args.get("data", "")
    buffer = BytesIO()
    qrcode.make(data, image_factory=PyPNGImage).save(buffer)
    return sanic.response.raw(buffer.getvalue(), content_type="image/png")
