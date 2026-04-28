import easyocr
import numpy as np
from PIL import Image
import io

# Khởi tạo reader (en + vi nếu cần)
reader = easyocr.Reader(['vi', 'en'], gpu=False)

def ocr_image_bytes(image_bytes: bytes) -> str:
    """
    OCR image bytes -> plain text
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(img)

    results = reader.readtext(img_np, detail=0)
    return "\n".join(results)