import io
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# OCR tiếng Anh + tiếng Việt
ocr_en = PaddleOCR(lang="en", use_angle_cls=True)
ocr_vi = PaddleOCR(lang="vi", use_angle_cls=True)

def run_ocr_image_bytes(image_bytes: bytes):
    """Nhận ảnh → OCR tiếng Anh + tiếng Việt."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(img)

    res_en = ocr_en.ocr(img_np)
    text_en = "\n".join([line[1][0] for line in res_en[0]]) if res_en else ""

    res_vi = ocr_vi.ocr(img_np)
    text_vi = "\n".join([line[1][0] for line in res_vi[0]]) if res_vi else ""

    return (text_en + "\n" + text_vi).strip()