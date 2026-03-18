import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("label_sample.png")

text = pytesseract.image_to_string(img)

print("\n===== EXTRACTED TEXT =====\n")
print(text)