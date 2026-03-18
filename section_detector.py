import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("label_sample.png")
text = pytesseract.image_to_string(img)

sections = [
    "INDICATIONS",
    "DOSAGE",
    "CONTRAINDICATIONS",
    "WARNINGS",
    "ADVERSE REACTIONS",
    "DRUG INTERACTIONS",
    "OVERDOSAGE",
    "STORAGE"
]

print("\n===== DETECTED LABEL SECTIONS =====\n")

for section in sections:
    if section.lower() in text.lower():
        print(f"{section} section detected")