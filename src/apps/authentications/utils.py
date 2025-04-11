import base64
from io import BytesIO

import qrcode


def generate_qrcode(mfa_hash):
    """Утилита для генерации QR-кода."""

    img = qrcode.make(mfa_hash)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return img_str
