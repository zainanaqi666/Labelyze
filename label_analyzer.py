import pytesseract
from PIL import Image
import requests

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("=== DRUG LABEL COMPLIANCE ANALYZER ===\n")

# Ask user for drug name
drug = input("Enter drug name: ")

# Fetch official label from DailyMed
search_url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={drug}"
search_data = requests.get(search_url).json()

if not search_data["data"]:
    print("Drug not found in DailyMed")
    exit()

setid = search_data["data"][0]["setid"]

label_url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml"
label_xml = requests.get(label_url).text.lower()

# Load label image
img = Image.open("label_sample.png")

# OCR extraction
ocr_text = pytesseract.image_to_string(img).lower()

# Sections to check
sections = {
"INDICATIONS": ["indications", "indications and usage"],
"DOSAGE": ["dosage", "dosage and administration"],
"CONTRAINDICATIONS": ["contraindications"],
"WARNINGS": ["warnings", "warnings and precautions"],
"ADVERSE REACTIONS": ["adverse reactions"],
"DRUG INTERACTIONS": ["drug interactions"],
"OVERDOSAGE": ["overdosage"],
"STORAGE": ["storage", "how supplied"]
}

print("\n=== COMPLIANCE REPORT ===\n")

score = 0
total = len(sections)

for section, keywords in sections.items():

    label_has = any(word in label_xml for word in keywords)
    image_has = any(word in ocr_text for word in keywords)

    if label_has and image_has:
        print(section + " → OK")
        score += 1

    elif label_has and not image_has:
        print(section + " → MISSING FROM LABEL IMAGE")

    elif not label_has and image_has:
        print(section + " → EXTRA SECTION FOUND")

    else:
        print(section + " → NOT PRESENT")

# Compliance score
percentage = (score / total) * 100

print("\nCompliance Score:", round(percentage,2), "%")