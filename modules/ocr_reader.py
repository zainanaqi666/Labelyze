# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

import cv2
import numpy as np
from modules.security_utils import sanitize_text

# ── Singleton OCR model ────────────────────────────────────────────────────────
_easyocr_reader = None
_use_easyocr = False

def _get_ocr_reader():
    global _easyocr_reader, _use_easyocr
    if _easyocr_reader is None:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
            _use_easyocr = True
        except Exception:
            _use_easyocr = False
    return _easyocr_reader, _use_easyocr


# ── Image preprocessing ────────────────────────────────────────────────────────
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    OpenCV preprocessing pipeline for pharmaceutical label images.
    Handles small fonts, curved surfaces, uneven lighting.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image.")

        # Upscale small images for better OCR accuracy
        h, w = img.shape[:2]
        if w < 1200:
            scale = 1200 / w
            img = cv2.resize(img, None, fx=scale, fy=scale,
                             interpolation=cv2.INTER_CUBIC)

        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # CLAHE contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Denoising
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)

        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 13, 3
        )

        # Sharpening kernel
        kernel = np.array([[0, -1, 0], [-1, 5.5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(thresh, -1, kernel)

        # Morphological cleanup
        kernel2 = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(sharpened, cv2.MORPH_CLOSE, kernel2)

        return cleaned

    except Exception:
        # Return original as fallback
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        return img if img is not None else np.zeros((100, 100), dtype=np.uint8)


# ── EasyOCR extraction ─────────────────────────────────────────────────────────
def _extract_easyocr(preprocessed: np.ndarray) -> tuple[str, float]:
    reader, use_easy = _get_ocr_reader()
    if not use_easy or reader is None:
        return "", 0.0
    try:
        results = reader.readtext(preprocessed, detail=1, paragraph=False)
        if not results:
            return "", 0.0
        lines = []
        confidences = []
        for (_, text, conf) in results:
            if text.strip():
                lines.append(text.strip())
                confidences.append(conf)
        full_text = "\n".join(lines)
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return full_text, avg_conf
    except Exception:
        return "", 0.0


# ── Tesseract fallback ─────────────────────────────────────────────────────────
def _extract_tesseract(preprocessed: np.ndarray) -> tuple[str, float]:
    try:
        import pytesseract
        from PIL import Image
        pil_img = Image.fromarray(preprocessed)
        text = pytesseract.image_to_string(pil_img, config="--psm 6 --oem 3")
        return text.strip(), 0.70
    except Exception:
        return "", 0.0


# ── Single image extraction ────────────────────────────────────────────────────
def extract_from_image_bytes(image_bytes: bytes) -> tuple[str, float]:
    """Extract text from a single image. Returns (text, confidence)."""
    try:
        preprocessed = preprocess_image(image_bytes)
        _, use_easy = _get_ocr_reader()

        if use_easy:
            text, conf = _extract_easyocr(preprocessed)
        else:
            text, conf = _extract_tesseract(preprocessed)

        if not text.strip():
            # Try raw image if preprocessed failed
            nparr = np.frombuffer(image_bytes, np.uint8)
            raw = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if raw is not None and use_easy:
                reader, _ = _get_ocr_reader()
                if reader:
                    results = reader.readtext(raw, detail=1, paragraph=False)
                    lines = [r[1] for r in results if r[1].strip()]
                    confs = [r[2] for r in results if r[1].strip()]
                    text = "\n".join(lines)
                    conf = sum(confs) / len(confs) if confs else 0.3

        return sanitize_text(text), round(conf, 3)

    except Exception as e:
        return f"[OCR Error: {str(e)[:100]}]", 0.0


# ── Multiple images ────────────────────────────────────────────────────────────
def extract_from_multiple_images(uploaded_files) -> tuple[str, float]:
    """
    Process multiple label images (carton sides).
    Returns merged text and average confidence.
    """
    all_texts = []
    all_confs = []

    for i, f in enumerate(uploaded_files):
        try:
            image_bytes = f.read()
            f.seek(0)
            text, conf = extract_from_image_bytes(image_bytes)
            if text.strip() and not text.startswith("[OCR Error"):
                all_texts.append(f"[SIDE {i+1}]\n{text.strip()}")
                all_confs.append(conf)
        except Exception:
            continue

    if not all_texts:
        return "", 0.0

    combined = "\n\n".join(all_texts)
    avg_conf = sum(all_confs) / len(all_confs)
    return sanitize_text(combined), round(avg_conf, 3)


# ── Confidence classification ──────────────────────────────────────────────────
def get_confidence_level(confidence: float) -> tuple[str, str | None]:
    """Returns (level, warning_message)."""
    if confidence >= 0.85:
        return "HIGH", None
    elif confidence >= 0.60:
        return "MEDIUM", "Moderate OCR confidence. Review extracted text carefully before running analysis."
    else:
        return "LOW", "Low OCR confidence. Text may contain errors. Please review and correct before analysis."


# ── Legacy compatibility ───────────────────────────────────────────────────────
def get_label_text(source, is_file: bool = True) -> str:
    """Legacy single-source entry point."""
    if is_file:
        try:
            with open(source, "rb") as f:
                image_bytes = f.read()
            text, _ = extract_from_image_bytes(image_bytes)
            return text
        except Exception:
            return ""
    return sanitize_text(str(source))
