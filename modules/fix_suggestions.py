# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

FIX_SUGGESTIONS = {
    "drug_name": {
        "title": "Drug Name & Strength",
        "suggestion": "Add prominently: '[Generic Name] Tablets/Capsules/Syrup IP [Strength] mg/ml'",
        "example": "Metformin Hydrochloride Tablets IP 500 mg",
        "corrective_action": "Revise label artwork to include generic drug name and strength on the principal display panel. Submit revised artwork for QA approval before next batch release.",
        "rule": "Rule 96 — Drug name must appear on the principal display panel",
    },
    "batch_number": {
        "title": "Batch / Lot Number",
        "suggestion": "Add: 'Batch No. [XXXXXX]' or 'Lot No. [XXXXXX]'",
        "example": "Batch No. B240312",
        "corrective_action": "Print batch number during batch-specific label printing stage. Verify batch coding system is operational and producing legible output.",
        "rule": "Rule 96 — Batch number required for traceability and recall management",
    },
    "manufacturing_date": {
        "title": "Manufacturing Date",
        "suggestion": "Add: 'Mfg. Date: [Month Year]' or 'Date of Manufacture: [Month Year]'",
        "example": "Mfg. Date: March 2024",
        "corrective_action": "Include manufacturing date in batch-specific variable printing. Verify date format compliance with Rule 96.",
        "rule": "Rule 96 — Manufacturing date must be stated on the label",
    },
    "expiry_date": {
        "title": "Expiry Date",
        "suggestion": "Add: 'Exp. Date: [Month Year]' or 'Use Before: [Month Year]'",
        "example": "Exp. Date: February 2026",
        "corrective_action": "Include expiry date derived from approved stability data. Verify shelf life assignment per ICH Q1A guidelines.",
        "rule": "Rule 96 — Expiry date is mandatory on all drug labels",
    },
    "manufacturer_name": {
        "title": "Manufacturer Name & Address",
        "suggestion": "Add: 'Manufactured by: [Company Name], [Full Address with PIN code]'",
        "example": "Manufactured by: Aurobindo Pharma Ltd, Plot No. 2, Hyderabad - 500018, Telangana, India",
        "corrective_action": "Add full legal name and registered address of manufacturer including PIN code. Verify against current drug licence details.",
        "rule": "Rule 96 — Full manufacturer name and address is mandatory",
    },
    "license_number": {
        "title": "Manufacturing Licence Number",
        "suggestion": "Add: 'Lic. No. [XX/XX/XXXX]' or 'Drug Lic. No. [XXXXXXXX]'",
        "example": "Lic. No. KD/2019/1234",
        "corrective_action": "Add manufacturing licence number as issued by the State Licensing Authority. Verify current licence validity before batch release.",
        "rule": "Rule 96(1) — Manufacturing licence number must appear on all drug labels",
    },
    "schedule_marking": {
        "title": "Schedule H / H1 / X Marking",
        "suggestion": "Add prominently: 'Schedule H' or 'Rx'. For H1: 'Schedule H1'. For X: 'Schedule X'",
        "example": "Schedule H — Not to be sold without the prescription of a Registered Medical Practitioner",
        "corrective_action": "Add appropriate schedule classification marking per Drugs & Cosmetics Act. Verify schedule classification of active ingredient against current CDSCO schedule list.",
        "rule": "D&C Act Rule 96 — Prescription schedule marking is mandatory for all prescription drugs",
    },
    "storage": {
        "title": "Storage Instructions",
        "suggestion": "Add: 'Store below [X]°C in a cool, dry place. Protect from light and moisture.'",
        "example": "Store below 25°C in a cool, dry place. Protect from direct sunlight and moisture. Keep out of reach of children.",
        "corrective_action": "Add specific temperature range based on approved stability study data. Ensure storage conditions match approved product specification.",
        "rule": "Schedule M GMP — Storage conditions must be clearly labelled",
    },
    "net_quantity": {
        "title": "Net Quantity / Pack Size",
        "suggestion": "Add: '[N] Tablets/Capsules' or 'Net Contents: [N] ml'",
        "example": "10 Tablets per strip  or  Net Contents: 100 ml",
        "corrective_action": "Declare net quantity per Legal Metrology Act requirements. Verify pack size matches declaration and actual contents.",
        "rule": "Legal Metrology Act — Net quantity declaration is mandatory",
    },
    "mrp": {
        "title": "Maximum Retail Price (MRP)",
        "suggestion": "Add: 'MRP: Rs. [XX.XX] (Inclusive of all taxes)'",
        "example": "MRP: Rs. 35.00 (Incl. of all taxes)",
        "corrective_action": "Print MRP inclusive of all taxes as per Drugs Price Control Order. Verify current approved MRP with marketing/regulatory team before printing.",
        "rule": "Drugs Price Control Order — MRP must be printed on the label",
    },
}


def get_fix_suggestions(section_results: list[dict]) -> list[dict]:
    """Returns fix suggestions for all failed and partial items."""
    fixes = []
    for item in section_results:
        if item["status"] in ["fail", "partial"]:
            item_id = item.get("id", "")
            if item_id in FIX_SUGGESTIONS:
                fix = FIX_SUGGESTIONS[item_id].copy()
                fix["id"] = item_id
                fix["status"] = item["status"]
                fixes.append(fix)
    return fixes
