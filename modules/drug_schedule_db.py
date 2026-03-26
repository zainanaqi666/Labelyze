# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

DRUG_SCHEDULE_DB = {
    # ── Antidiabetics ────────────────────────────────────────────────────────
    "metformin":         {"schedule": "H",  "category": "Antidiabetic"},
    "glibenclamide":     {"schedule": "H",  "category": "Antidiabetic"},
    "glimepiride":       {"schedule": "H",  "category": "Antidiabetic"},
    "gliclazide":        {"schedule": "H",  "category": "Antidiabetic"},
    "sitagliptin":       {"schedule": "H",  "category": "Antidiabetic"},
    "vildagliptin":      {"schedule": "H",  "category": "Antidiabetic"},
    "insulin":           {"schedule": "H",  "category": "Antidiabetic"},
    "pioglitazone":      {"schedule": "H",  "category": "Antidiabetic"},
    "empagliflozin":     {"schedule": "H",  "category": "Antidiabetic"},
    "dapagliflozin":     {"schedule": "H",  "category": "Antidiabetic"},

    # ── Antihypertensives ────────────────────────────────────────────────────
    "amlodipine":        {"schedule": "H",  "category": "Antihypertensive"},
    "atenolol":          {"schedule": "H",  "category": "Antihypertensive"},
    "enalapril":         {"schedule": "H",  "category": "Antihypertensive"},
    "ramipril":          {"schedule": "H",  "category": "Antihypertensive"},
    "losartan":          {"schedule": "H",  "category": "Antihypertensive"},
    "telmisartan":       {"schedule": "H",  "category": "Antihypertensive"},
    "olmesartan":        {"schedule": "H",  "category": "Antihypertensive"},
    "valsartan":         {"schedule": "H",  "category": "Antihypertensive"},
    "nifedipine":        {"schedule": "H",  "category": "Antihypertensive"},
    "hydrochlorothiazide": {"schedule": "H","category": "Antihypertensive"},
    "furosemide":        {"schedule": "H",  "category": "Diuretic"},
    "spironolactone":    {"schedule": "H",  "category": "Diuretic"},
    "bisoprolol":        {"schedule": "H",  "category": "Antihypertensive"},
    "metoprolol":        {"schedule": "H",  "category": "Antihypertensive"},
    "carvedilol":        {"schedule": "H",  "category": "Antihypertensive"},

    # ── Lipid lowering ───────────────────────────────────────────────────────
    "atorvastatin":      {"schedule": "H",  "category": "Lipid lowering"},
    "rosuvastatin":      {"schedule": "H",  "category": "Lipid lowering"},
    "simvastatin":       {"schedule": "H",  "category": "Lipid lowering"},
    "fenofibrate":       {"schedule": "H",  "category": "Lipid lowering"},
    "ezetimibe":         {"schedule": "H",  "category": "Lipid lowering"},

    # ── Antibiotics ─────────────────────────────────────────────────────────
    "amoxicillin":       {"schedule": "H",  "category": "Antibiotic"},
    "ampicillin":        {"schedule": "H",  "category": "Antibiotic"},
    "azithromycin":      {"schedule": "H",  "category": "Antibiotic"},
    "clarithromycin":    {"schedule": "H",  "category": "Antibiotic"},
    "doxycycline":       {"schedule": "H",  "category": "Antibiotic"},
    "erythromycin":      {"schedule": "H",  "category": "Antibiotic"},
    "metronidazole":     {"schedule": "H",  "category": "Antibiotic"},
    "tinidazole":        {"schedule": "H",  "category": "Antibiotic"},
    "ciprofloxacin":     {"schedule": "H",  "category": "Antibiotic"},
    "norfloxacin":       {"schedule": "H",  "category": "Antibiotic"},
    "ofloxacin":         {"schedule": "H",  "category": "Antibiotic"},
    "levofloxacin":      {"schedule": "H",  "category": "Antibiotic"},
    "cotrimoxazole":     {"schedule": "H",  "category": "Antibiotic"},
    "clindamycin":       {"schedule": "H",  "category": "Antibiotic"},
    "linezolid":         {"schedule": "H",  "category": "Antibiotic"},
    "vancomycin":        {"schedule": "H",  "category": "Antibiotic"},
    "amoxycillin":       {"schedule": "H",  "category": "Antibiotic"},

    # ── Schedule H1 — 3rd gen antibiotics ───────────────────────────────────
    "cefixime":          {"schedule": "H1", "category": "3rd gen antibiotic"},
    "ceftriaxone":       {"schedule": "H1", "category": "3rd gen antibiotic"},
    "cefpodoxime":       {"schedule": "H1", "category": "3rd gen antibiotic"},
    "cefuroxime":        {"schedule": "H1", "category": "3rd gen antibiotic"},
    "cefoperazone":      {"schedule": "H1", "category": "3rd gen antibiotic"},
    "meropenem":         {"schedule": "H1", "category": "Carbapenem antibiotic"},
    "imipenem":          {"schedule": "H1", "category": "Carbapenem antibiotic"},
    "piperacillin":      {"schedule": "H1", "category": "Extended spectrum antibiotic"},
    "colistin":          {"schedule": "H1", "category": "Last resort antibiotic"},
    "cefepime":          {"schedule": "H1", "category": "4th gen antibiotic"},

    # ── GI medications ───────────────────────────────────────────────────────
    "omeprazole":        {"schedule": "H",  "category": "Proton pump inhibitor"},
    "pantoprazole":      {"schedule": "H",  "category": "Proton pump inhibitor"},
    "rabeprazole":       {"schedule": "H",  "category": "Proton pump inhibitor"},
    "esomeprazole":      {"schedule": "H",  "category": "Proton pump inhibitor"},
    "ondansetron":       {"schedule": "H",  "category": "Antiemetic"},
    "domperidone":       {"schedule": "H",  "category": "Antiemetic"},
    "ranitidine":        {"schedule": "H",  "category": "H2 blocker"},

    # ── Respiratory ──────────────────────────────────────────────────────────
    "salbutamol":        {"schedule": "H",  "category": "Bronchodilator"},
    "ipratropium":       {"schedule": "H",  "category": "Bronchodilator"},
    "montelukast":       {"schedule": "H",  "category": "Antiasthmatic"},
    "budesonide":        {"schedule": "H",  "category": "Corticosteroid inhaler"},
    "fluticasone":       {"schedule": "H",  "category": "Corticosteroid inhaler"},
    "tiotropium":        {"schedule": "H",  "category": "Bronchodilator"},

    # ── Corticosteroids ──────────────────────────────────────────────────────
    "prednisolone":      {"schedule": "H",  "category": "Corticosteroid"},
    "dexamethasone":     {"schedule": "H",  "category": "Corticosteroid"},
    "betamethasone":     {"schedule": "H",  "category": "Corticosteroid"},
    "hydrocortisone":    {"schedule": "H",  "category": "Corticosteroid"},
    "methylprednisolone": {"schedule": "H", "category": "Corticosteroid"},

    # ── NSAIDs ───────────────────────────────────────────────────────────────
    "diclofenac":        {"schedule": "H",  "category": "NSAID"},
    "ibuprofen":         {"schedule": "H",  "category": "NSAID"},
    "naproxen":          {"schedule": "H",  "category": "NSAID"},
    "piroxicam":         {"schedule": "H",  "category": "NSAID"},
    "celecoxib":         {"schedule": "H",  "category": "NSAID"},
    "etoricoxib":        {"schedule": "H",  "category": "NSAID"},
    "indomethacin":      {"schedule": "H",  "category": "NSAID"},

    # ── Thyroid ──────────────────────────────────────────────────────────────
    "levothyroxine":     {"schedule": "H",  "category": "Thyroid"},
    "carbimazole":       {"schedule": "H",  "category": "Antithyroid"},
    "propylthiouracil":  {"schedule": "H",  "category": "Antithyroid"},

    # ── Anticoagulants ───────────────────────────────────────────────────────
    "warfarin":          {"schedule": "H",  "category": "Anticoagulant"},
    "heparin":           {"schedule": "H",  "category": "Anticoagulant"},
    "clopidogrel":       {"schedule": "H",  "category": "Antiplatelet"},
    "rivaroxaban":       {"schedule": "H",  "category": "Anticoagulant"},
    "apixaban":          {"schedule": "H",  "category": "Anticoagulant"},

    # ── CNS / Antidepressants ────────────────────────────────────────────────
    "amitriptyline":     {"schedule": "H",  "category": "Antidepressant"},
    "fluoxetine":        {"schedule": "H",  "category": "Antidepressant"},
    "sertraline":        {"schedule": "H",  "category": "Antidepressant"},
    "escitalopram":      {"schedule": "H",  "category": "Antidepressant"},
    "venlafaxine":       {"schedule": "H",  "category": "Antidepressant"},
    "mirtazapine":       {"schedule": "H",  "category": "Antidepressant"},
    "lithium":           {"schedule": "H",  "category": "Mood stabiliser"},
    "valproate":         {"schedule": "H",  "category": "Mood stabiliser / Antiepileptic"},
    "carbamazepine":     {"schedule": "H",  "category": "Antiepileptic"},
    "phenytoin":         {"schedule": "H",  "category": "Antiepileptic"},
    "levetiracetam":     {"schedule": "H",  "category": "Antiepileptic"},
    "phenobarbitone":    {"schedule": "H",  "category": "Antiepileptic"},
    "lamotrigine":       {"schedule": "H",  "category": "Antiepileptic"},

    # ── Schedule X — Controlled substances ──────────────────────────────────
    "alprazolam":        {"schedule": "X",  "category": "Benzodiazepine"},
    "diazepam":          {"schedule": "X",  "category": "Benzodiazepine"},
    "clonazepam":        {"schedule": "X",  "category": "Benzodiazepine"},
    "lorazepam":         {"schedule": "X",  "category": "Benzodiazepine"},
    "nitrazepam":        {"schedule": "X",  "category": "Benzodiazepine"},
    "triazolam":         {"schedule": "X",  "category": "Benzodiazepine"},
    "midazolam":         {"schedule": "X",  "category": "Benzodiazepine"},
    "zolpidem":          {"schedule": "X",  "category": "Sedative hypnotic"},
    "buprenorphine":     {"schedule": "X",  "category": "Opioid"},
    "morphine":          {"schedule": "X",  "category": "Opioid"},
    "tramadol":          {"schedule": "X",  "category": "Opioid analgesic"},
    "codeine":           {"schedule": "X",  "category": "Opioid"},
    "fentanyl":          {"schedule": "X",  "category": "Opioid"},
    "pentazocine":       {"schedule": "X",  "category": "Opioid analgesic"},

    # ── OTC ──────────────────────────────────────────────────────────────────
    "paracetamol":       {"schedule": "OTC", "category": "Analgesic / Antipyretic"},
    "acetaminophen":     {"schedule": "OTC", "category": "Analgesic / Antipyretic"},
    "cetirizine":        {"schedule": "OTC", "category": "Antihistamine"},
    "loratadine":        {"schedule": "OTC", "category": "Antihistamine"},
    "chlorpheniramine":  {"schedule": "OTC", "category": "Antihistamine"},
    "aspirin":           {"schedule": "OTC", "category": "Analgesic / Antiplatelet"},
    "zinc":              {"schedule": "OTC", "category": "Supplement"},
    "vitamin c":         {"schedule": "OTC", "category": "Supplement"},
    "vitamin d":         {"schedule": "OTC", "category": "Supplement"},
    "folic acid":        {"schedule": "OTC", "category": "Supplement"},
    "calcium":           {"schedule": "OTC", "category": "Supplement"},
    "iron":              {"schedule": "OTC", "category": "Supplement"},

    # ── Banned in India ──────────────────────────────────────────────────────
    "sibutramine":       {"schedule": "BANNED", "category": "Weight loss — banned in India 2010"},
    "nimesulide":        {"schedule": "BANNED", "category": "NSAID — banned for children under 12"},
    "phenacetin":        {"schedule": "BANNED", "category": "Analgesic — banned due to toxicity"},
    "analgin":           {"schedule": "BANNED", "category": "Metamizole — banned in India"},
    "metamizole":        {"schedule": "BANNED", "category": "Analgesic — banned in India"},
    "oxyphenbutazone":   {"schedule": "BANNED", "category": "NSAID — banned due to toxicity"},
    "phenylbutazone":    {"schedule": "BANNED", "category": "NSAID — banned in India"},
    "valdecoxib":        {"schedule": "BANNED", "category": "COX-2 inhibitor — banned"},
    "rofecoxib":         {"schedule": "BANNED", "category": "COX-2 inhibitor — banned globally"},
    "cisapride":         {"schedule": "BANNED", "category": "Prokinetic — banned due to cardiac risk"},
    "astemizole":        {"schedule": "BANNED", "category": "Antihistamine — banned due to cardiac risk"},
    "terfenadine":       {"schedule": "BANNED", "category": "Antihistamine — banned"},
    "furazolidone":      {"schedule": "BANNED", "category": "Antibiotic — banned in India"},
    "rimonabant":        {"schedule": "BANNED", "category": "Obesity drug — banned"},
    "tegaserod":         {"schedule": "BANNED", "category": "IBS drug — banned due to cardiac risk"},
}

SCHEDULE_LABELS = {
    "H":      "Schedule H — Prescription only",
    "H1":     "Schedule H1 — Strict prescription control",
    "X":      "Schedule X — Controlled substance",
    "OTC":    "Over the counter — No prescription required",
    "BANNED": "BANNED in India — Section 26A D&C Act",
}

SCHEDULE_EXPLANATIONS = {
    "H":  "This drug is classified under Schedule H of the Drugs & Cosmetics Act. It can only be dispensed with a valid doctor's prescription. The label must display 'Schedule H' or the Rx symbol prominently.",
    "H1": "This drug is classified under Schedule H1 — a stricter category introduced to control antimicrobial resistance. It requires a prescription retained by the pharmacist. Label must clearly state 'Schedule H1'.",
    "X":  "This drug is classified under Schedule X — covering psychotropics, narcotics, and strong sedatives. Requires written prescription retained for 2 years. Label must display 'Schedule X' prominently.",
    "OTC": "This drug is available over the counter without a prescription. No Schedule H, H1, or X marking is required. All other Schedule M mandatory label requirements still apply.",
    "BANNED": "WARNING: This drug or formulation has been banned in India under Section 26A of the Drugs & Cosmetics Act. Manufacturing, sale, and distribution is prohibited. Immediate regulatory review required.",
}


def lookup_drug(drug_name_text: str) -> dict | None:
    """Match drug name from label text against database."""
    if not drug_name_text:
        return None
    text_lower = drug_name_text.lower()
    for drug, info in DRUG_SCHEDULE_DB.items():
        if drug in text_lower:
            return {
                "drug":        drug.title(),
                "schedule":    info["schedule"],
                "category":    info["category"],
                "label":       SCHEDULE_LABELS[info["schedule"]],
                "explanation": SCHEDULE_EXPLANATIONS[info["schedule"]],
            }
    return None
