#offline 2
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(uploaded_file):
    # Read image bytes
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

    # Decode image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return "Error: Unable to read image"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang="eng")
    return text.strip()
