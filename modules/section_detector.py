# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Unauthorised commercial use is prohibited.
# Licensed under CC BY-NC 4.0 — see LICENSE file for details.
# Contact: zainanaqi666@gmail.com
from modules.schedule_m_reference import SCHEDULE_M_CHECKLIST

FDA_SECTIONS = [
    {"id": "indications",       "label": "Indications and usage",
     "keywords": ["indication", "used for", "used to treat", "treatment of"]},
    {"id": "dosage",            "label": "Dosage and administration",
     "keywords": ["dosage", "dose", "administration", "how to take", "take"]},
    {"id": "contraindications", "label": "Contraindications",
     "keywords": ["contraindication", "do not use", "not for use in"]},
    {"id": "warnings",          "label": "Warnings and precautions",
     "keywords": ["warning", "precaution", "caution", "avoid"]},
    {"id": "adverse",           "label": "Adverse reactions",
     "keywords": ["adverse", "side effect", "undesirable", "reaction"]},
    {"id": "interactions",      "label": "Drug interactions",
     "keywords": ["interaction", "interacts with", "do not take with"]},
]

SEMANTIC_DESCRIPTIONS = {
    "drug_name":          "drug name strength dosage form tablets capsules mg ml",
    "batch_number":       "batch number lot number production batch code",
    "manufacturing_date": "manufacturing date date of manufacture production date made on",
    "expiry_date":        "expiry date expiration date use before use by best before valid until",
    "manufacturer_name":  "manufactured by produced by made by company name manufacturer address",
    "license_number":     "manufacturing licence license number drug licence authorization number",
    "schedule_marking":   "schedule H prescription only rx symbol controlled drug",
    "storage":            "storage instructions store below temperature cool dry place refrigerate",
    "net_quantity":       "net quantity pack size number of tablets capsules contents",
    "mrp":                "maximum retail price MRP price cost rupees",
}

_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _model = None
    return _model


def semantic_score(text_chunk, description):
    model = get_model()
    if model is None:
        return 0.0
    try:
        import torch
        embeddings = model.encode([text_chunk, description], convert_to_tensor=True)
        cos_sim = torch.nn.functional.cosine_similarity(
            embeddings[0].unsqueeze(0),
            embeddings[1].unsqueeze(0)
        ).item()
        return cos_sim
    except Exception:
        return 0.0


def detect_sections_cdsco(label_text):
    text_lower = label_text.lower()
    sentences = [s.strip() for s in label_text.replace("\n", ". ").split(".") if s.strip()]
    results = []

    for item in SCHEDULE_M_CHECKLIST:
        keyword_matches = [kw for kw in item["keywords"] if kw in text_lower]

        if len(keyword_matches) >= 2:
            status = "pass"
            found_text = f"Detected: {', '.join(keyword_matches[:3])}"

        elif len(keyword_matches) == 1:
            status = "pass"
            found_text = f"Detected: '{keyword_matches[0]}'"

        else:
            best_score = 0.0
            best_sentence = ""
            description = SEMANTIC_DESCRIPTIONS.get(item["id"], item["label"])

            for sentence in sentences:
                if len(sentence) > 5:
                    score = semantic_score(sentence, description)
                    if score > best_score:
                        best_score = score
                        best_sentence = sentence

            if best_score >= 0.45:
                status = "pass"
                found_text = f"AI match ({int(best_score * 100)}%): '{best_sentence[:50]}'"
            elif best_score >= 0.30:
                status = "partial"
                found_text = f"Possible match ({int(best_score * 100)}%): '{best_sentence[:50]}'"
            else:
                status = "fail"
                found_text = None

        results.append({
            "id":       item["id"],
            "label":    item["label"],
            "status":   status,
            "found":    found_text,
            "rule":     item["rule"],
            "critical": item["critical"]
        })

    return results


def detect_sections_fda(label_text):
    text_lower = label_text.lower()
    results = []

    for section in FDA_SECTIONS:
        matches = [kw for kw in section["keywords"] if kw in text_lower]

        if matches:
            status = "pass"
            found_text = f"Detected: '{matches[0]}'"
        else:
            status = "fail"
            found_text = None

        results.append({
            "id":       section["id"],
            "label":    section["label"],
            "status":   status,
            "found":    found_text,
            "rule":     "FDA labeling requirements 21 CFR 201",
            "critical": True
        })

    return results


def detect_sections(label_text, mode="cdsco"):
    if mode == "cdsco":
        return detect_sections_cdsco(label_text)
    else:
        return detect_sections_fda(label_text)
