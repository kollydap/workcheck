# app/utils/qr.py
import qrcode
import io
import base64
from typing import Optional

def generate_qr_code(data: str, size: int = 10) -> str:
    """
    Generate QR code for given data and return as base64 string
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
