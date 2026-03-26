# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

from modules.schedule_m_reference import SCHEDULE_M_CHECKLIST

FDA_SECTIONS = [
    {"id": "indications",       "label": "Indications and usage",
     "keywords": ["indication", "used for", "used to treat", "treatment of", "indicated for"]},
    {"id": "dosage",            "label": "Dosage and administration",
     "keywords": ["dosage", "dose", "administration", "how to take", "take", "administer"]},
    {"id": "contraindications", "label": "Contraindications",
     "keywords": ["contraindication", "do not use", "not for use in", "contraindicated"]},
    {"id": "warnings",          "label": "Warnings and precautions",
     "keywords": ["warning", "precaution", "caution", "avoid", "black box"]},
    {"id": "adverse",           "label": "Adverse reactions",
     "keywords": ["adverse", "side effect", "undesirable", "reaction", "side effects"]},
    {"id": "interactions",      "label": "Drug interactions",
     "keywords": ["interaction", "interacts with", "do not take with", "drug interaction"]},
]

EMA_SECTIONS = [
    {"id": "name_eu",           "label": "Name of medicinal product",
     "keywords": ["tablets", "capsules", "solution", "mg", "ml", "mcg", "film-coated"]},
    {"id": "composition",       "label": "Qualitative and quantitative composition",
     "keywords": ["active substance", "excipient", "contains", "each tablet", "per ml", "active"]},
    {"id": "pharmaceutical",    "label": "Pharmaceutical form",
     "keywords": ["film-coated", "tablet", "capsule", "solution", "powder", "modified release"]},
    {"id": "marketing_holder",  "label": "Marketing authorisation holder",
     "keywords": ["marketing authorisation", "mah", "holder", "authorisation", "authorised"]},
    {"id": "batch_eu",          "label": "Batch number",
     "keywords": ["batch", "lot", "charge", "lot no"]},
    {"id": "expiry_eu",         "label": "Expiry date",
     "keywords": ["exp", "expiry", "expiration", "use before", "use by", "best before"]},
    {"id": "storage_eu",        "label": "Storage conditions",
     "keywords": ["store", "storage", "keep", "below", "temperature", "refrigerate", "cool"]},
    {"id": "warnings_eu",       "label": "Special warnings",
     "keywords": ["warning", "precaution", "keep out", "do not", "special warning"]},
    {"id": "prescription_eu",   "label": "Prescription / non-prescription status",
     "keywords": ["prescription", "pharmacy", "medicament", "rx", "pom"]},
    {"id": "name_holder",       "label": "Name and address of manufacturer",
     "keywords": ["manufactured by", "manufacturer", "made by", "produced by", "pharma"]},
]

SEMANTIC_DESCRIPTIONS = {
    "drug_name":          "drug name strength dosage form tablets capsules mg ml",
    "batch_number":       "batch number lot number production batch code identifier",
    "manufacturing_date": "manufacturing date date of manufacture production date made on",
    "expiry_date":        "expiry date expiration date use before use by best before valid until",
    "manufacturer_name":  "manufactured by produced by made by company name manufacturer address",
    "license_number":     "manufacturing licence license number drug licence authorization number",
    "schedule_marking":   "schedule H prescription only rx symbol controlled drug classification",
    "storage":            "storage instructions store below temperature cool dry place refrigerate",
    "net_quantity":       "net quantity pack size number of tablets capsules contents volume",
    "mrp":                "maximum retail price MRP price cost rupees amount",
}

_nlp_model = None


def _get_model():
    global _nlp_model
    if _nlp_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _nlp_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _nlp_model = None
    return _nlp_model


def _semantic_score(sentence: str, description: str) -> float:
    model = _get_model()
    if model is None or not sentence.strip():
        return 0.0
    try:
        import torch
        emb = model.encode([sentence, description], convert_to_tensor=True)
        score = torch.nn.functional.cosine_similarity(
            emb[0].unsqueeze(0), emb[1].unsqueeze(0)
        ).item()
        return max(0.0, min(1.0, score))
    except Exception:
        return 0.0


def _check_item(item_id: str, item_keywords: list, label_text: str) -> tuple[str, str | None]:
    """Returns (status, found_text)."""
    text_lower = label_text.lower()
    matches = [kw for kw in item_keywords if kw in text_lower]

    if len(matches) >= 2:
        return "pass", f"Detected: {', '.join(matches[:3])}"
    if len(matches) == 1:
        return "pass", f"Detected: '{matches[0]}'"

    # Semantic fallback
    description = SEMANTIC_DESCRIPTIONS.get(item_id, "")
    if not description:
        return "fail", None

    sentences = [s.strip() for s in label_text.replace("\n", ". ").split(".") if len(s.strip()) > 4]
    best_score, best_sentence = 0.0, ""

    for sentence in sentences[:50]:  # Limit for performance
        score = _semantic_score(sentence, description)
        if score > best_score:
            best_score = score
            best_sentence = sentence

    if best_score >= 0.45:
        return "pass", f"AI match ({int(best_score * 100)}%): '{best_sentence[:50]}'"
    if best_score >= 0.30:
        return "partial", f"Possible match ({int(best_score * 100)}%): '{best_sentence[:50]}'"
    return "fail", None


def detect_sections_cdsco(label_text: str) -> list[dict]:
    results = []
    for item in SCHEDULE_M_CHECKLIST:
        status, found_text = _check_item(item["id"], item["keywords"], label_text)
        results.append({
            "id":       item["id"],
            "label":    item["label"],
            "status":   status,
            "found":    found_text,
            "rule":     item["rule"],
            "critical": item["critical"],
        })
    return results


def detect_sections_fda(label_text: str) -> list[dict]:
    text_lower = label_text.lower()
    results = []
    for section in FDA_SECTIONS:
        matches = [kw for kw in section["keywords"] if kw in text_lower]
        if matches:
            status, found = "pass", f"Detected: '{matches[0]}'"
        else:
            status, found = _check_item(section["id"], section["keywords"], label_text)
        results.append({
            "id":       section["id"],
            "label":    section["label"],
            "status":   status,
            "found":    found,
            "rule":     "FDA labeling requirements 21 CFR 201",
            "critical": True,
        })
    return results


def detect_sections_ema(label_text: str) -> list[dict]:
    results = []
    for section in EMA_SECTIONS:
        status, found = _check_item(section["id"], section["keywords"], label_text)
        results.append({
            "id":       section["id"],
            "label":    section["label"],
            "status":   status,
            "found":    found,
            "rule":     "EU Directive 2001/83/EC — Annex I labelling requirements",
            "critical": True,
        })
    return results


def detect_sections(label_text: str, mode: str = "cdsco") -> list[dict]:
    if not label_text or not label_text.strip():
        return []
    if mode == "fda":
        return detect_sections_fda(label_text)
    if mode == "ema":
        return detect_sections_ema(label_text)
    return detect_sections_cdsco(label_text)
