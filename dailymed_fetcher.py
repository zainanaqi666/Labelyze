import requests
from lxml import etree

user_input = input("Enter drug name OR NDC code: ")

# Step 1: search DailyMed
search_url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={user_input}"
search_response = requests.get(search_url)
search_data = search_response.json()

label = search_data["data"][0]

setid = label["setid"]
title = label["title"]

print("Search Input:", user_input)
print("Label Title:", title)

# Step 2: download label XML
label_url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml"
label_response = requests.get(label_url)

root = etree.fromstring(label_response.content)

target_sections = [
"INDICATIONS AND USAGE",
"DOSAGE AND ADMINISTRATION",
"CONTRAINDICATIONS",
"WARNINGS AND PRECAUTIONS",
"ADVERSE REACTIONS",
"DRUG INTERACTIONS",
"OVERDOSAGE",
"STORAGE",
"HANDLING"
]

# dictionary to store label sections
label_data = {}

for element in root.iter():

    if "title" in element.tag and element.text:

        title_text = element.text.strip().upper()

        for section in target_sections:

            if section in title_text:

                parent = element.getparent()

                for child in parent.iter():

                    if child.text:

                        text = child.text.strip()

                        if len(text) > 50:

                            label_data[section] = text[:1000]
                            break

# print stored data
print("\nStored Regulatory Sections:\n")

for section, text in label_data.items():

    print("SECTION:", section)
    print("TEXT:", text[:200])
    print("\n-------------------------")import pytesseract
from PIL import Image

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
img = Image.open("label_sample.png")

# Extract text
text = pytesseract.image_to_string(img)

print("\n===== EXTRACTED TEXT =====\n")
print(text)