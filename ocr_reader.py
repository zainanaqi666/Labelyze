import cv2
import easyocr

reader = easyocr.Reader(['en'])

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def extract_text(image_path):
    image = preprocess_image(image_path)
    result = reader.readtext(image)

    lines = [item[1] for item in result]

    return "\n".join(lines)

text = extract_text("label_sample.png")

print("\n===== EXTRACTED TEXT =====\n")
print(text)