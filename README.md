# Labelyze
### AI-Powered Pharmaceutical Label Compliance & Batch Release Verification Tool

Labelyze is an AI-assisted compliance tool that checks pharmaceutical labels against regulatory requirements and generates deviation reports for batch release verification.

---

## What it does

- Checks Indian pharmaceutical labels against **Schedule M of the Drugs & Cosmetics Act (CDSCO)**
- Checks international labels against **FDA / ICH guidelines**
- Identifies the **drug schedule classification** (Schedule H, H1, X, OTC, or Banned)
- Flags **banned drugs** under Indian regulations
- Uses **AI semantic matching** (Sentence Transformers) to understand label text beyond keyword matching
- Generates a professional **Label Deviation Report (PDF)** ready for QA sign-off

---

## Modules

| Module | Purpose |
|--------|---------|
| `modules/schedule_m_reference.py` | Schedule M mandatory label checklist |
| `modules/drug_schedule_db.py` | Drug schedule database (H, H1, X, OTC, Banned) |
| `modules/section_detector.py` | AI-powered section detection using Sentence Transformers |
| `modules/ocr_reader.py` | OCR text extraction from label images |
| `modules/risk_analyzer.py` | Compliance scoring and risk level calculation |
| `modules/dailymed_fetcher.py` | DailyMed API integration for FDA reference labels |
| `ui.py` | Streamlit web interface |
| `app.py` | Terminal-based testing entry point |

---

## How to run

**Install dependencies:**
```
pip install streamlit sentence-transformers pytesseract Pillow fpdf2 requests
```

**Run the web interface:**
```
streamlit run ui.py
```

---

## Regulatory coverage

**Indian market (CDSCO)** checks against Schedule M mandatory items:
- Drug name and strength
- Batch / lot number
- Manufacturing and expiry date
- Manufacturer name and address
- Manufacturing licence number
- Schedule H / H1 / X marking
- Storage instructions
- Net quantity and MRP

**International export (FDA / ICH)** checks for:
- Indications and usage
- Dosage and administration
- Contraindications
- Warnings and precautions
- Adverse reactions
- Drug interactions

---

## Drug schedule database

The tool identifies drug schedule classification for 100+ common Indian pharmaceutical compounds including Schedule H, H1, X, OTC drugs and drugs banned in India under the Drugs & Cosmetics Act.

---

## Built with

- Python 3
- Streamlit
- Sentence Transformers (all-MiniLM-L6-v2)
- Tesseract OCR
- FPDF2
- DailyMed API (US National Library of Medicine)

---

*Built as a portfolio project by a final year B.Pharm student targeting QA/RA roles in the Indian pharmaceutical industry.*
