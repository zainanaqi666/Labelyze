# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Unauthorised commercial use is prohibited.
# Licensed under CC BY-NC 4.0 — see LICENSE file for details.
# Contact: zainanaqi666@gmail.com
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """
    Takes a file path to a label image (JPG, PNG, PDF).
    Returns extracted text as a plain string.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"ERROR: Could not read image. Details: {str(e)}"


def extract_text_from_string(raw_text):
    """
    If user pastes text directly, just clean and return it.
    """
    return raw_text.strip()


def get_label_text(source, is_file=True):
    """
    Main entry point.
    - If is_file=True, source is a file path
    - If is_file=False, source is pasted text
    """
    if is_file:
        return extract_text_from_image(source)
    else:
        return extract_text_from_string(source)
