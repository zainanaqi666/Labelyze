# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Unauthorised commercial use is prohibited.
# Licensed under CC BY-NC 4.0 — see LICENSE file for details.
# Contact: zainanaqi666@gmail.com
import streamlit as st
from modules.ocr_reader import get_label_text
from modules.section_detector import detect_sections
from modules.risk_analyzer import analyze_risk
from modules.drug_schedule_db import lookup_drug
from fpdf import FPDF
import datetime


def generate_pdf_report(risk, mode, label_type, drug_name="", drug_info=None):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    def clean(text):
        return str(text).replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').strip()

    context = "CDSCO / Schedule M (Indian market)" if mode == "cdsco" else "FDA 21 CFR 201 (US market)"
    report_no = f"LDR-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    date_str = datetime.datetime.now().strftime("%d-%b-%Y")
    time_str = datetime.datetime.now().strftime("%H:%M")

    if risk["can_release"]:
        decision = "APPROVED FOR RELEASE"
    elif risk["risk_level"] == "MEDIUM":
        decision = "ON HOLD - REVIEW REQUIRED"
    else:
        decision = "ON HOLD - DO NOT RELEASE"

    def section_header(title):
        pdf.set_fill_color(220, 220, 220)
        pdf.set_draw_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(15)
        pdf.cell(180, 7, title, ln=True, fill=True, border=1)

    pdf.set_draw_color(0, 0, 0)
    pdf.rect(15, 15, 180, 20, style="D")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(15, 18)
    pdf.cell(180, 8, "LABEL DEVIATION REPORT", align="C", ln=True)
    pdf.ln(6)

    row_h = 7

    section_header("SECTION 1 - REVIEW DETAILS")

    def info_row(label1, val1, label2, val2):
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(35, row_h, label1, border=1)
        pdf.set_font("Helvetica", "", 9)
        y = pdf.get_y()
        pdf.multi_cell(55, row_h, val1, border=1)
        new_y = pdf.get_y()
        pdf.set_xy(105, y)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(35, row_h, label2, border=1)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(45, row_h, val2, border=1)
        if pdf.get_y() < new_y:
            pdf.set_y(new_y)

    info_row("Date of Review:", date_str, "Time:", time_str)
    info_row("Product / Drug:", (clean(drug_name) if drug_name else "As per label"), "Label Type:", label_type)
    info_row("Regulatory Context:", ("CDSCO / Schedule M" if mode == "cdsco" else "FDA 21 CFR 201"), "Review Type:", "Label Compliance")
    if drug_info:
        info_row("Drug Schedule:", drug_info["label"][:38], "Drug Category:", drug_info["category"][:38])
    pdf.ln(4)

    if drug_info and drug_info["schedule"] == "BANNED":
        section_header("WARNING - BANNED DRUG DETECTED")
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(180, 7, f"This drug ({drug_info['drug']}) is BANNED in India.", border=1, ln=True)
        pdf.set_x(15)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(180, 6, clean(drug_info["explanation"]), border=1)
        pdf.ln(4)

    section_header("SECTION 2 - COMPLIANCE SUMMARY")
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(60, 7, "Compliance Score", border=1, align="C")
    pdf.cell(30, 7, "Risk Level", border=1, align="C")
    pdf.cell(40, 7, "Checks Passed", border=1, align="C")
    pdf.cell(50, 7, "Release Decision", border=1, align="C", ln=True)

    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(60, 9, f"{risk['score']}%", border=1, align="C")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 9, risk["risk_level"], border=1, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(40, 9, f"{risk['passed_count']} / {risk['total_checks']}", border=1, align="C")
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(50, 9, clean(decision[:28]), border=1, align="C", ln=True)
    pdf.ln(4)

    if risk["critical_fails"]:
        section_header(f"SECTION 3 - CRITICAL MISSING ITEMS ({risk['fail_count']}) - Must be corrected before release")
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(8, 7, "No.", border=1, align="C")
        pdf.cell(80, 7, "Missing Item", border=1)
        pdf.cell(92, 7, "Applicable Rule / Regulation", border=1, ln=True)
        for i, item in enumerate(risk["critical_fails"], 1):
            label_text_clean = clean(item["label"])
            rule_text_clean = clean(item["rule"])
            y = pdf.get_y()
            pdf.set_x(15)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(8, 14, str(i), border=1, align="C", ln=False)
            pdf.set_x(23)
            pdf.multi_cell(80, 7, label_text_clean, border=1)
            y_after = pdf.get_y()
            pdf.set_xy(103, y)
            pdf.multi_cell(92, 7, rule_text_clean, border=1)
            pdf.set_y(max(y_after, pdf.get_y()))
        pdf.ln(3)

    if risk["partial_items"]:
        section_header(f"SECTION 4 - PARTIAL / UNCLEAR ITEMS ({risk['partial_count']}) - Review recommended")
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(8, 7, "No.", border=1, align="C")
        pdf.cell(60, 7, "Item", border=1)
        pdf.cell(112, 7, "Finding & Rule", border=1, ln=True)
        for i, item in enumerate(risk["partial_items"], 1):
            detail = clean(item["detail"]) if item["detail"] else "Incomplete"
            rule = clean(item["rule"])
            combined = f"{detail} | {rule}"
            y = pdf.get_y()
            pdf.set_x(15)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(8, 12, str(i), border=1, align="C", ln=False)
            pdf.cell(60, 12, clean(item["label"][:35]), border=1, ln=False)
            pdf.multi_cell(112, 6, combined, border=1)
            new_y = pdf.get_y()
            if new_y < y + 12:
                pdf.set_y(y + 12)
        pdf.ln(3)

    if risk["passed"]:
        section_header(f"SECTION 5 - PASSED CHECKS ({risk['passed_count']} items)")
        for i, label in enumerate(risk["passed"], 1):
            pdf.set_x(15)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(8, 6, str(i), border=1, align="C")
            pdf.cell(172, 6, f"  [PASS]  {clean(label)}", border=1, ln=True)
        pdf.ln(3)

    section_header("SECTION 6 - CORRECTIVE ACTION & SIGN-OFF")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_x(15)
    pdf.cell(180, 6, "Corrective action required:", border="LR", ln=True)
    pdf.set_x(15)
    pdf.cell(180, 8, "", border="LR", ln=True)
    pdf.set_x(15)
    pdf.cell(180, 8, "", border="LR", ln=True)
    pdf.set_x(15)
    pdf.cell(180, 8, "", border="LRB", ln=True)
    pdf.ln(3)

    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(60, 7, "Reviewed by:", border=1)
    pdf.cell(60, 7, "Approved by:", border=1)
    pdf.cell(60, 7, "Date of Closure:", border=1, ln=True)
    pdf.set_x(15)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 14, "", border=1)
    pdf.cell(60, 14, "", border=1)
    pdf.cell(60, 14, "", border=1, ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(80, 80, 80)
    pdf.set_x(15)
    pdf.cell(180, 5, f"Generated: {date_str}  {time_str}", align="C", ln=True)

    return bytes(pdf.output())


st.set_page_config(
    page_title="Labelyze",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background-color: #f7f4ef; }

.block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

.brand-box {
    background: #eee8dc;
    border: 2px solid #1a1a1a;
    border-radius: 16px;
    padding: 36px 40px 28px 40px;
    margin-bottom: 28px;
    text-align: center;
}
.brand-name {
    font-size: 240px;
    font-weight: 900;
    color: #1a1a1a;
    letter-spacing: -4px;
    margin: 0;
    line-height: 1;
}
.brand-sub {
    font-size: 16px;
    font-weight: 500;
    color: #444;
    margin: 12px 0 0 0;
    line-height: 1.5;
}

.how-box {
    background: #eee8dc;
    border: 1.5px solid #d6cfc3;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 28px;
}
.how-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin: 0 0 12px 0;
}
.how-step {
    font-size: 15px;
    font-weight: 500;
    color: #1a1a1a;
    margin: 7px 0;
    padding-left: 4px;
}

.section-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin: 0 0 10px 0;
}

label, .stRadio label p {
    font-size: 16px !important;
    font-weight: 500 !important;
    color: #1a1a1a !important;
}

.stRadio > div {
    gap: 12px !important;
}

div[data-baseweb="radio"] label {
    background: #eee8dc !important;
    border: 1.5px solid #d6cfc3 !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #1a1a1a !important;
    cursor: pointer !important;
}

div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
div[data-baseweb="select"] input,
div[data-baseweb="select"] div {
    background-color: #eee8dc !important;
    color: #1a1a1a !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    border-color: #b5ad9e !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] * {
    color: #1a1a1a !important;
    font-size: 16px !important;
}

div[data-baseweb="popover"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] * {
    background-color: #f7f4ef !important;
    color: #1a1a1a !important;
    font-size: 15px !important;
}

.stTextArea textarea {
    background-color: #eee8dc !important;
    border: 1.5px solid #d6cfc3 !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    color: #1a1a1a !important;
    padding: 14px !important;
}

.stFileUploader > div {
    background-color: #eee8dc !important;
    border: 1.5px dashed #888 !important;
    border-radius: 12px !important;
    padding: 24px !important;
}

.stFileUploader label, .stFileUploader p, .stFileUploader span,
.stFileUploader small, .stFileUploader div {
    color: #1a1a1a !important;
    font-size: 15px !important;
}

section[data-testid="stFileUploadDropzone"],
section[data-testid="stFileUploadDropzone"] > div,
div[data-testid="stFileUploader"],
div[data-testid="stFileUploader"] > div,
div[data-testid="stFileUploader"] section {
    background-color: #eee8dc !important;
    border: 1.5px dashed #888 !important;
    border-radius: 12px !important;
}

section[data-testid="stFileUploadDropzone"] *,
div[data-testid="stFileUploader"] *,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploader"] small {
    color: #1a1a1a !important;
    background-color: transparent !important;
}

.stButton > button {
    background-color: #f7f4ef !important;
    color: #1a1a1a !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 14px 28px !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    margin-top: 8px !important;
}

.stButton > button:hover {
    background-color: #eee8dc !important;
    color: #1a1a1a !important;
}

.stButton > button:disabled {
    background-color: #ccc8c0 !important;
    color: #888 !important;
    border: 2px solid #aaa !important;
}

.stDownloadButton > button {
    background-color: #1a1a1a !important;
    color: #f7f4ef !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 14px 28px !important;
    width: 100% !important;
    margin-top: 8px !important;
}

.stDownloadButton > button:hover {
    background-color: #333 !important;
    color: #f7f4ef !important;
}

div[data-testid="metric-container"] {
    background: #eee8dc !important;
    border: 1.5px solid #d6cfc3 !important;
    border-radius: 12px !important;
    padding: 20px 16px !important;
}

div[data-testid="metric-container"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #888 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    font-size: 36px !important;
    font-weight: 800 !important;
    color: #1a1a1a !important;
}

.stAlert {
    border-radius: 10px !important;
    font-size: 15px !important;
}

.stAlert p {
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #1a1a1a !important;
}

hr {
    border: none !important;
    border-top: 1.5px solid #d6cfc3 !important;
    margin: 24px 0 !important;
}

h3 {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #1a1a1a !important;
    letter-spacing: -0.5px !important;
}

h4 {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

p, span, li {
    font-size: 15px !important;
    color: #1a1a1a !important;
}

small, .stCaption p {
    font-size: 13px !important;
    color: #888 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#eee8dc;border:2px solid #1a1a1a;border-radius:16px;padding:48px 44px 36px 44px;margin-bottom:28px;text-align:left;">
    <div style="font-family:'Times New Roman',Times,serif;font-size:clamp(42px, 11vw, 96px);font-weight:900;color:#2C1810;letter-spacing:-4px;margin:0 0 16px 0;line-height:1;display:block;-webkit-text-fill-color:#2C1810;">Labelyze</div>
    <div style="font-size:17px;font-weight:500;color:#444444;margin:0;line-height:1.5;display:block;">AI-powered pharmaceutical label compliance &amp; batch release verification</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="how-box">
    <p class="how-title">How to use</p>
    <p class="how-step">1&nbsp;&nbsp; Select your market and label type</p>
    <p class="how-step">2&nbsp;&nbsp; Upload a label photo or paste the text</p>
    <p class="how-step">3&nbsp;&nbsp; Run the check and download the deviation report</p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown('<p class="section-label">Step 1 — Regulatory context</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:17px;font-weight:600;color:#1a1a1a;margin:0 0 8px 0;">Which market is this label for?</p>', unsafe_allow_html=True)

mode = st.radio(
    "Which market is this label for?",
    options=["Indian market (CDSCO / Schedule M)", "International export (FDA / ICH guidelines)"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

label_type = st.selectbox(
    "Label type",
    ["Carton (outer packaging)", "Package insert", "Container label"]
)

st.divider()

st.markdown('<p class="section-label">Step 2 — Upload or paste your label</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:17px;font-weight:600;color:#1a1a1a;margin:0 0 8px 0;">How do you want to provide the label?</p>', unsafe_allow_html=True)

input_method = st.radio(
    "Input method",
    options=["Upload image", "Paste text"],
    horizontal=True,
    label_visibility="collapsed"
)

label_text = None

if input_method == "Upload image":
    uploaded_file = st.file_uploader(
        "Upload label image",
        type=["png", "jpg", "jpeg"],
        help="Take a clear photo of the label in good lighting"
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded label", width=300)
        with open("temp_label.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Reading text from image..."):
            label_text = get_label_text("temp_label.png", is_file=True)
        st.success(f"Extracted {len(label_text)} characters from image")
else:
    pasted_text = st.text_area(
        "Paste label text here",
        height=200,
        placeholder="""Metformin Hydrochloride Tablets IP 500 mg
Batch No. B240312
Mfg Date: March 2024   Exp Date: February 2026
Manufactured by: Aurobindo Pharma Ltd, Hyderabad
Lic No: KD/2019/1234
Schedule H
Store below 25 degrees C.
MRP: Rs. 35
Net Qty: 10 Tablets"""
    )
    if pasted_text.strip():
        label_text = pasted_text.strip()

st.divider()

st.markdown('<p class="section-label">Step 3 — Run compliance check</p>', unsafe_allow_html=True)

run_button = st.button(
    "Run compliance check",
    disabled=(label_text is None)
)

if run_button and label_text:

    selected_mode = "cdsco" if "CDSCO" in mode else "fda"

    with st.spinner("Analysing label against regulatory requirements..."):
        results = detect_sections(label_text, mode=selected_mode)
        risk = analyze_risk(results)

    first_line = label_text.strip().split("\n")[0]
    drug_info = lookup_drug(first_line)

    st.divider()
    st.markdown("### Compliance report")
    st.caption(f"{label_type}  ·  {'CDSCO / Schedule M' if selected_mode == 'cdsco' else 'FDA / ICH guidelines'}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance score", f"{risk['score']}%")
    with col2:
        st.metric("Critical missing", risk["fail_count"])
    with col3:
        st.metric("Partial / unclear", risk["partial_count"])

    st.markdown("")

    if risk["can_release"]:
        st.success("Label approved for release — all critical checks passed")
    elif risk["risk_level"] == "MEDIUM":
        st.warning("Label on hold — review partial items before release")
    else:
        st.error("Label cannot be released — critical items are missing")

    if drug_info:
        st.markdown("")
        if drug_info["schedule"] == "BANNED":
            st.error(
                f"**Drug identification: {drug_info['drug']} — {drug_info['label']}**\n\n"
                f"{drug_info['explanation']}"
            )
        else:
            st.info(
                f"**Drug identification: {drug_info['drug']} — {drug_info['label']}**\n\n"
                f"Category: {drug_info['category']}\n\n"
                f"{drug_info['explanation']}"
            )
    else:
        st.markdown("")
        st.caption("Drug not found in schedule database — please verify schedule classification manually against the current Drugs & Cosmetics Act appendix.")

    st.divider()

    if risk["critical_fails"]:
        st.markdown("#### Critical missing items")
        for item in risk["critical_fails"]:
            st.error(f"**{item['label']}**")
            st.caption(f"Rule: {item['rule']}")

    if risk["partial_items"]:
        st.markdown("#### Partial / unclear items")
        for item in risk["partial_items"]:
            st.warning(f"**{item['label']}**")
            st.caption(f"{item['detail']}")
            st.caption(f"Rule: {item['rule']}")

    if risk["passed"]:
        st.markdown("#### Passed checks")
        for label in risk["passed"]:
            st.success(f"{label}")

    st.divider()

    pdf_bytes = generate_pdf_report(risk, selected_mode, label_type, first_line, drug_info)
    st.download_button(
        label="Download deviation report (PDF)",
        data=pdf_bytes,
        file_name=f"labelyze_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf"
    )
