import base64
from io import BytesIO

import pyotp
import qrcode


def generate_qrcode(mfa_hash):
    """Утилита для генерации QR-кода."""

    try:
        img = qrcode.make(mfa_hash)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    except Exception as e:
        raise ValueError(f"Error generating QR code: {e}")

    return img_str
