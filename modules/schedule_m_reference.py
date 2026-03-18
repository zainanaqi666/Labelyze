SCHEDULE_M_CHECKLIST = [
    {
        "id": "drug_name",
        "label": "Drug name and strength",
        "keywords": ["mg", "ml", "mcg", "iu", "tablet", "capsule", "syrup",
                     "injection", "cream", "ointment", "drops", "solution"],
        "rule": "Rule 96 - Drug name and strength must appear prominently",
        "critical": True
    },
    {
        "id": "batch_number",
        "label": "Batch / lot number",
        "keywords": ["batch no", "batch number", "lot no", "lot number",
                     "b.no", "b no", "mfg batch"],
        "rule": "Rule 96 - Batch number required for traceability and recall",
        "critical": True
    },
    {
        "id": "manufacturing_date",
        "label": "Manufacturing date",
        "keywords": ["mfg date", "mfg.", "manufactured", "manufacturing date",
                     "date of manufacture", "dom", "mfd"],
        "rule": "Rule 96 - Manufacturing date must be stated",
        "critical": True
    },
    {
        "id": "expiry_date",
        "label": "Expiry / use before date",
        "keywords": ["exp date", "expiry", "expiration", "use before",
                     "use by", "exp.", "best before"],
        "rule": "Rule 96 - Expiry date mandatory on all drug labels",
        "critical": True
    },
    {
        "id": "manufacturer_name",
        "label": "Manufacturer name and address",
        "keywords": ["manufactured by", "mfg by", "marketed by",
                     "pharma", "pharmaceuticals", "labs", "ltd", "pvt"],
        "rule": "Rule 96 - Full manufacturer name and address required",
        "critical": True
    },
    {
        "id": "license_number",
        "label": "Manufacturing licence number",
        "keywords": ["lic no", "lic. no", "licence no", "license no",
                     "drug licence", "mfg lic", "m.l. no"],
        "rule": "Rule 96(1) - Manufacturing licence number must appear on label",
        "critical": True
    },
    {
        "id": "schedule_marking",
        "label": "Schedule H / H1 / X marking or Rx symbol",
        "keywords": ["schedule h", "schedule h1", "schedule x",
                     "rx only", "prescription only", "rx", "sch. h"],
        "rule": "D&C Act Rule 96 - Prescription status marking is mandatory",
        "critical": True
    },
    {
        "id": "storage",
        "label": "Storage instructions",
        "keywords": ["store", "storage", "keep", "protect from",
                     "below", "temperature", "cool", "dry place", "refrigerate"],
        "rule": "Schedule M GMP - Storage conditions must be labelled",
        "critical": False
    },
    {
        "id": "net_quantity",
        "label": "Net quantity / pack size",
        "keywords": ["tablets", "capsules", "ml", "gm", "g",
                     "strip of", "bottle of", "pack of", "vial of"],
        "rule": "Legal Metrology Act - Net quantity declaration is mandatory",
        "critical": False
    },
    {
        "id": "mrp",
        "label": "Maximum retail price (MRP)",
        "keywords": ["mrp", "m.r.p", "maximum retail price",
                     "rs.", "inr", "price"],
        "rule": "Drugs Price Control Order - MRP must be printed on label",
        "critical": False
    }
]
