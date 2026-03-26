# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

import streamlit as st
import datetime
from fpdf import FPDF

from modules.ocr_reader import (
    extract_from_multiple_images,
    get_confidence_level,
    get_label_text,
)
from modules.section_detector import detect_sections
from modules.risk_analyzer import analyze_risk
from modules.drug_schedule_db import lookup_drug
from modules.fix_suggestions import get_fix_suggestions
from modules.label_comparator import compare_labels, get_submission_status
from modules.audit_trail import log_check, load_audit, get_audit_summary, clear_audit
from modules.security_utils import (
    sanitize_text,
    check_rate_limit,
    validate_image_file,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Labelyze", page_icon="", layout="centered")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background-color: #f5f0e8; }
.block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 4rem; }
.brand-box {
  background: #eee8dc; border: 2px solid #1a1a1a;
  border-radius: 16px; padding: 40px 44px 28px 44px; margin-bottom: 24px;
}
.how-box {
  background: #eee8dc; border: 1px solid #d6cfc3;
  border-radius: 12px; padding: 18px 24px; margin-bottom: 24px;
}
.section-label {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.1em; color: #888; margin-bottom: 10px;
}
div[data-testid="metric-container"] {
  background: #eee8dc !important; border: 1.5px solid #d6cfc3 !important;
  border-radius: 12px !important; padding: 16px !important;
}
div[data-testid="metric-container"] div[data-testid="metric-value"] {
  font-size: 32px !important; font-weight: 800 !important; color: #1a1a1a !important;
}
.stButton > button {
  background-color: #1a1a1a !important; color: #f5f0e8 !important;
  border: none !important; border-radius: 8px !important;
  font-size: 15px !important; font-weight: 700 !important;
  padding: 12px 24px !important; width: 100% !important;
}
.stButton > button:disabled {
  background-color: #ccc !important; color: #888 !important;
}
.stDownloadButton > button {
  background-color: #1a1a1a !important; color: #f5f0e8 !important;
  border: none !important; border-radius: 8px !important;
  font-size: 15px !important; font-weight: 700 !important;
  width: 100% !important; padding: 12px 24px !important;
}
div[data-baseweb="select"] > div, div[data-baseweb="select"] * {
  background-color: #eee8dc !important; color: #1a1a1a !important;
  font-size: 15px !important; border-color: #d6cfc3 !important;
}
div[data-baseweb="popover"] li, div[data-baseweb="popover"] * {
  background-color: #f5f0e8 !important; color: #1a1a1a !important;
}
.stTextArea textarea {
  background-color: #eee8dc !important; color: #1a1a1a !important;
  border: 1.5px solid #d6cfc3 !important; font-size: 14px !important;
}
section[data-testid="stFileUploadDropzone"],
section[data-testid="stFileUploadDropzone"] > div,
div[data-testid="stFileUploader"] section {
  background-color: #eee8dc !important;
  border: 1.5px dashed #888 !important;
  border-radius: 12px !important;
}
section[data-testid="stFileUploadDropzone"] *,
div[data-testid="stFileUploader"] * { color: #1a1a1a !important; }
label { font-size: 15px !important; font-weight: 600 !important; color: #1a1a1a !important; }
p { font-size: 15px !important; color: #1a1a1a !important; }
hr { border: none !important; border-top: 1.5px solid #d6cfc3 !important; margin: 20px 0 !important; }
.stAlert p { font-size: 14px !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-box">
  <div style="font-family:'Times New Roman',Times,serif;font-size:clamp(42px,11vw,96px);
    font-weight:900;color:#1a1a1a;letter-spacing:-4px;margin:0 0 12px 0;
    line-height:1;-webkit-text-fill-color:#1a1a1a;">Labelyze</div>
  <div style="font-size:16px;font-weight:500;color:#444;margin:0;line-height:1.5;">
    AI-powered pharmaceutical label compliance &amp; batch release verification
  </div>
</div>
<div class="how-box">
  <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;
     color:#888;margin:0 0 10px 0;">How to use</p>
  <p style="font-size:14px;font-weight:500;color:#1a1a1a;margin:5px 0;">
    1&nbsp;&nbsp; Select your regulatory market and label type</p>
  <p style="font-size:14px;font-weight:500;color:#1a1a1a;margin:5px 0;">
    2&nbsp;&nbsp; Upload all carton sides (multiple images) or paste text</p>
  <p style="font-size:14px;font-weight:500;color:#1a1a1a;margin:5px 0;">
    3&nbsp;&nbsp; Review and correct the extracted text if needed</p>
  <p style="font-size:14px;font-weight:500;color:#1a1a1a;margin:5px 0;">
    4&nbsp;&nbsp; Run the check and download your deviation report</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Label Compliance Check",
    "Label Comparison",
    "Audit Trail",
])

MODE_OPTIONS = {
    "Indian market (CDSCO / Schedule M)":          "cdsco",
    "International export (FDA / ICH guidelines)": "fda",
    "European Union (EMA / EU Directive 2001/83/EC)": "ema",
}

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — COMPLIANCE CHECK
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.divider()
    st.markdown('<p class="section-label">Step 1 — Regulatory context</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:16px;font-weight:600;color:#1a1a1a;margin:0 0 8px 0;">Which market is this label for?</p>', unsafe_allow_html=True)

    mode_display = st.radio(
        "Market", list(MODE_OPTIONS.keys()),
        label_visibility="collapsed", key="t1_mode"
    )
    selected_mode = MODE_OPTIONS[mode_display]

    label_type = st.selectbox(
        "Label type",
        ["Carton (outer packaging)", "Package insert", "Container label"],
        key="t1_ltype"
    )

    st.divider()
    st.markdown('<p class="section-label">Step 2 — Upload or paste your label</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:16px;font-weight:600;color:#1a1a1a;margin:0 0 8px 0;">How do you want to provide the label?</p>', unsafe_allow_html=True)

    input_method = st.radio(
        "Input", ["Upload images", "Paste text"],
        horizontal=True, label_visibility="collapsed", key="t1_input"
    )

    label_text   = None
    ocr_conf     = None
    ocr_engine   = "Paste"

    if input_method == "Upload images":
        st.markdown("**Upload all sides of the label** — front, back, and any side panels")
        uploaded_files = st.file_uploader(
            "Upload label images",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="t1_files",
            help="You can select multiple files at once for all sides of the carton",
        )

        if uploaded_files:
            # Validate files
            errors = []
            valid_files = []
            for f in uploaded_files:
                ok, msg = validate_image_file(f)
                if ok:
                    valid_files.append(f)
                else:
                    errors.append(f"{f.name}: {msg}")
            for e in errors:
                st.error(e)

            if valid_files:
                # Rate limit
                allowed, msg = check_rate_limit("ocr")
                if not allowed:
                    st.error(msg)
                else:
                    # Show previews
                    cols = st.columns(min(len(valid_files), 4))
                    for i, f in enumerate(valid_files):
                        with cols[i % 4]:
                            st.image(f, caption=f"Side {i+1}", use_container_width=True)
                            f.seek(0)

                    with st.spinner(f"Reading text from {len(valid_files)} image(s)..."):
                        try:
                            raw_text, ocr_conf = extract_from_multiple_images(valid_files)
                        except Exception as e:
                            st.error(f"OCR failed: {str(e)[:200]}. Please paste the label text instead.")
                            raw_text, ocr_conf = "", 0.0

                    if raw_text.strip():
                        conf_level, conf_warning = get_confidence_level(ocr_conf)
                        if conf_warning:
                            st.warning(f"OCR confidence: **{conf_level}** ({int(ocr_conf*100)}%) — {conf_warning}")
                        else:
                            st.success(f"OCR confidence: **{conf_level}** ({int(ocr_conf*100)}%) — Text extracted successfully")

                        st.markdown("**Review and correct extracted text if needed:**")
                        label_text = st.text_area(
                            "Extracted text (editable)",
                            value=raw_text,
                            height=220,
                            key="t1_ocr_edit",
                            help="Correct any OCR errors before running the compliance check",
                        )
                        label_text = sanitize_text(label_text) if label_text else None
                    else:
                        st.warning("No text could be extracted. Please paste the label text manually.")
    else:
        raw_paste = st.text_area(
            "Paste label text here",
            height=220,
            key="t1_paste",
            placeholder="""Metformin Hydrochloride Tablets IP 500 mg
Batch No. B240312
Mfg Date: March 2024   Exp Date: February 2026
Manufactured by: Aurobindo Pharma Ltd, Hyderabad
Lic No: KD/2019/1234
Schedule H
Store below 25 degrees C.
MRP: Rs. 35
Net Qty: 10 Tablets""",
        )
        if raw_paste and raw_paste.strip():
            label_text = sanitize_text(raw_paste)

    st.divider()
    st.markdown('<p class="section-label">Step 3 — Run compliance check</p>', unsafe_allow_html=True)

    run_btn = st.button(
        "Run compliance check",
        key="t1_run",
        disabled=(not label_text or not label_text.strip()),
    )

    if run_btn and label_text and label_text.strip():
        # Rate limit
        allowed, msg = check_rate_limit("check")
        if not allowed:
            st.error(msg)
            st.stop()

        with st.spinner("Analysing label against regulatory requirements..."):
            try:
                results  = detect_sections(label_text, mode=selected_mode)
                risk     = analyze_risk(results)
            except Exception as e:
                st.error(f"Analysis failed: {str(e)[:200]}")
                st.stop()

        first_line = label_text.strip().split("\n")[0]
        drug_info  = lookup_drug(first_line)
        fixes      = get_fix_suggestions(results)

        # Audit log
        try:
            log_check(label_text, selected_mode, label_type, risk, drug_info)
        except Exception:
            pass

        # ── Results ──────────────────────────────────────────────────────────
        st.divider()
        st.markdown("### Compliance report")
        mode_label = {
            "cdsco": "CDSCO / Schedule M",
            "fda":   "FDA 21 CFR 201",
            "ema":   "EU EMA Directive 2001/83/EC",
        }.get(selected_mode, "CDSCO")
        st.caption(f"{label_type}  ·  {mode_label}")
        if ocr_conf is not None:
            st.caption(f"OCR confidence: {int(ocr_conf*100)}%")

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Compliance score",  f"{risk['score']}%")
        with col2: st.metric("Critical missing",  risk["fail_count"])
        with col3: st.metric("Partial / unclear", risk["partial_count"])
        st.markdown("")

        if risk["can_release"]:
            st.success("Label approved for release — all critical checks passed")
        elif risk["risk_level"] == "MEDIUM":
            st.warning("Label on hold — review partial items before release")
        else:
            st.error("Label cannot be released — critical items are missing")

        # Drug identification
        if drug_info:
            st.markdown("")
            if drug_info["schedule"] == "BANNED":
                st.error(
                    f"**WARNING — Banned drug detected: {drug_info['drug']}**\n\n"
                    f"{drug_info['label']}\n\n{drug_info['explanation']}"
                )
            else:
                st.info(
                    f"**Drug identification: {drug_info['drug']} — {drug_info['label']}**\n\n"
                    f"Category: {drug_info['category']}\n\n{drug_info['explanation']}"
                )
        else:
            st.caption("Drug not found in schedule database — verify schedule classification manually against the Drugs & Cosmetics Act appendix.")

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
                st.caption(str(item.get("detail", "")))
                st.caption(f"Rule: {item['rule']}")

        if risk["passed"]:
            st.markdown("#### Passed checks")
            for lbl in risk["passed"]:
                st.success(f"{lbl}")

        # Fix My Label
        if fixes:
            st.divider()
            st.markdown("#### Fix My Label — suggested corrections")
            st.caption("AI-generated corrective text for each missing or partial item")
            for fix in fixes:
                with st.expander(f"How to fix: {fix['title']}"):
                    st.markdown(f"**Suggested text:** {fix['suggestion']}")
                    st.code(fix["example"], language=None)
                    st.markdown(f"**Corrective action:** {fix['corrective_action']}")
                    st.caption(f"Rule: {fix['rule']}")

        st.divider()

        # PDF report
        try:
            pdf_bytes = _generate_pdf(risk, selected_mode, label_type, first_line, drug_info, fixes)
            st.download_button(
                label="Download deviation report (PDF)",
                data=pdf_bytes,
                file_name=f"labelyze_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)[:200]}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LABEL COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.divider()
    st.markdown("### Label Comparison Engine")
    st.caption("Compare an old label version against a new one — identifies changes, fixes, and submission readiness.")

    comp_mode_display = st.radio(
        "Regulatory mode",
        list(MODE_OPTIONS.keys()),
        label_visibility="collapsed",
        key="t2_mode",
    )
    comp_mode = MODE_OPTIONS[comp_mode_display]

    col_old, col_new = st.columns(2)
    with col_old:
        st.markdown("**Old label version**")
        old_text = st.text_area("Old label", height=260, key="t2_old",
                                placeholder="Paste the previous label version here...")
    with col_new:
        st.markdown("**New label version**")
        new_text = st.text_area("New label", height=260, key="t2_new",
                                placeholder="Paste the updated label version here...")

    compare_btn = st.button(
        "Compare labels", key="t2_compare",
        disabled=(not old_text or not new_text or
                  not old_text.strip() or not new_text.strip()),
    )

    if compare_btn and old_text and new_text:
        old_clean = sanitize_text(old_text)
        new_clean = sanitize_text(new_text)

        with st.spinner("Comparing labels..."):
            try:
                comp = compare_labels(old_clean, new_clean, comp_mode)
            except Exception as e:
                st.error(f"Comparison failed: {str(e)[:200]}")
                st.stop()

        status_text, status_color = get_submission_status(comp)
        st.divider()
        st.markdown("### Comparison results")

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Old score",    f"{comp['old_score']}%")
        with col2:
            delta = comp["score_delta"]
            st.metric("New score", f"{comp['new_score']}%",
                      delta=f"{'+' if delta >= 0 else ''}{delta}%")
        with col3: st.metric("Similarity",    f"{comp['similarity']}%")
        with col4: st.metric("Lines changed", len(comp["added_lines"]) + len(comp["removed_lines"]))

        if status_color == "green":
            st.success(f"**{status_text}**")
        elif status_color == "orange":
            st.warning(f"**{status_text}**")
        else:
            st.error(f"**{status_text}**")

        if comp["newly_fixed"]:
            st.markdown("#### Items fixed in new version")
            for item in comp["newly_fixed"]:
                st.success(f"Fixed: {item}")

        if comp["newly_broken"]:
            st.markdown("#### Items broken in new version")
            for item in comp["newly_broken"]:
                st.error(f"Broken: {item}")

        if comp["added_lines"]:
            with st.expander(f"Content added ({len(comp['added_lines'])} lines)"):
                for line in comp["added_lines"]:
                    st.markdown(f"<span style='color:green'>+ {line}</span>", unsafe_allow_html=True)

        if comp["removed_lines"]:
            with st.expander(f"Content removed ({len(comp['removed_lines'])} lines)"):
                for line in comp["removed_lines"]:
                    st.markdown(f"<span style='color:red'>- {line}</span>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AUDIT TRAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.divider()
    st.markdown("### Audit Trail")
    st.caption("Complete log of all compliance checks — inspection ready")

    try:
        summary = get_audit_summary()
        records = load_audit()
    except Exception:
        summary, records = None, []

    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total checks", summary["total_checks"])
        with col2: st.metric("Approved",      summary["approved"])
        with col3: st.metric("On hold",       summary["on_hold"])
        with col4: st.metric("Avg score",     f"{summary['avg_score']}%")

        st.divider()
        if records:
            st.markdown("#### Check history (most recent first)")
            for record in reversed(records[-30:]):
                icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(
                    record.get("risk_level", ""), "⚪")
                release = "APPROVED" if record.get("can_release") else "ON HOLD"
                label_preview = record.get("drug_name", "Unknown")[:40]
                with st.expander(
                    f"{icon}  {record.get('date','')} {record.get('time','')}  ·  "
                    f"{label_preview}  ·  {record.get('score',0)}%  ·  {release}"
                ):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Mode:** {record.get('mode','')}")
                        st.write(f"**Label type:** {record.get('label_type','')}")
                        st.write(f"**Drug schedule:** {record.get('drug_schedule','')}")
                    with c2:
                        st.write(f"**Score:** {record.get('score',0)}%")
                        st.write(f"**Risk:** {record.get('risk_level','')}")
                        st.write(f"**Checks:** {record.get('passed',0)}/{record.get('total',0)} passed")
                    preview = record.get("label_preview", "")
                    if preview:
                        st.caption(f"Preview: {preview[:150]}...")

        if st.button("Clear audit trail", key="t3_clear"):
            try:
                clear_audit()
                st.success("Audit trail cleared.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not clear: {str(e)[:100]}")
    else:
        st.info("No compliance checks recorded yet. Run a check in the first tab to start your audit trail.")


# ══════════════════════════════════════════════════════════════════════════════
# PDF GENERATION (internal)
# ══════════════════════════════════════════════════════════════════════════════
def _generate_pdf(risk, mode, label_type, drug_name="", drug_info=None, fixes=None):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    def clean(t):
        return str(t).replace("\u2014","-").replace("\u2013","-").replace(
            "\u2018","'").replace("\u2019","'").replace("\u201c",'"').replace("\u201d",'"').strip()

    mode_labels = {
        "cdsco": "CDSCO / Schedule M (Indian market)",
        "fda":   "FDA 21 CFR 201 (US market)",
        "ema":   "EU EMA Directive 2001/83/EC",
    }
    context   = mode_labels.get(mode, "CDSCO / Schedule M")
    report_no = f"LDR-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    date_str  = datetime.datetime.now().strftime("%d-%b-%Y")
    time_str  = datetime.datetime.now().strftime("%H:%M")
    decision  = ("APPROVED FOR RELEASE" if risk["can_release"]
                 else ("ON HOLD - REVIEW REQUIRED" if risk["risk_level"]=="MEDIUM"
                       else "ON HOLD - DO NOT RELEASE"))

    def sec(title):
        pdf.set_fill_color(220,220,220); pdf.set_draw_color(0,0,0)
        pdf.set_font("Helvetica","B",9); pdf.set_text_color(0,0,0)
        pdf.set_x(15); pdf.cell(180,7,title,ln=True,fill=True,border=1)

    # Header
    pdf.rect(15,15,180,20,style="D")
    pdf.set_font("Helvetica","B",14); pdf.set_text_color(0,0,0)
    pdf.set_xy(15,18); pdf.cell(180,8,"LABEL DEVIATION REPORT",align="C",ln=True)
    pdf.ln(6)

    RH = 7
    def info_row(l1,v1,l2,v2):
        pdf.set_x(15)
        pdf.set_font("Helvetica","B",9); pdf.cell(38,RH,l1,border=1)
        pdf.set_font("Helvetica","",9);  pdf.cell(52,RH,v1,border=1)
        pdf.set_font("Helvetica","B",9); pdf.cell(38,RH,l2,border=1)
        pdf.set_font("Helvetica","",9);  pdf.cell(52,RH,v2,border=1,ln=True)

    sec("SECTION 1 - REVIEW DETAILS")
    info_row("Date of Review:", date_str, "Time:", time_str)
    info_row("Product / Drug:", clean(drug_name[:38]) if drug_name else "As per label", "Label Type:", label_type[:38])
    info_row("Regulatory Context:", clean(context[:38]), "Review Type:", "Label Compliance")
    if drug_info:
        info_row("Drug Schedule:", clean(drug_info["label"][:38]), "Category:", clean(drug_info["category"][:38]))
    pdf.ln(4)

    sec("SECTION 2 - COMPLIANCE SUMMARY")
    pdf.set_x(15); pdf.set_font("Helvetica","B",9)
    pdf.cell(60,7,"Compliance Score",border=1,align="C")
    pdf.cell(30,7,"Risk Level",border=1,align="C")
    pdf.cell(40,7,"Checks Passed",border=1,align="C")
    pdf.cell(50,7,"Release Decision",border=1,align="C",ln=True)
    pdf.set_x(15); pdf.set_font("Helvetica","B",11)
    pdf.cell(60,9,f"{risk['score']}%",border=1,align="C")
    pdf.set_font("Helvetica","B",10)
    pdf.cell(30,9,risk["risk_level"],border=1,align="C")
    pdf.set_font("Helvetica","",10)
    pdf.cell(40,9,f"{risk['passed_count']} / {risk['total_checks']}",border=1,align="C")
    pdf.set_font("Helvetica","B",9)
    pdf.cell(50,9,clean(decision[:28]),border=1,align="C",ln=True)
    pdf.ln(4)

    if risk["critical_fails"]:
        sec(f"SECTION 3 - CRITICAL MISSING ITEMS ({risk['fail_count']}) - Must be corrected before release")
        pdf.set_x(15); pdf.set_font("Helvetica","B",9)
        pdf.cell(8,7,"No.",border=1,align="C")
        pdf.cell(80,7,"Missing Item",border=1)
        pdf.cell(92,7,"Applicable Rule / Regulation",border=1,ln=True)
        for i, item in enumerate(risk["critical_fails"],1):
            y = pdf.get_y(); pdf.set_x(15); pdf.set_font("Helvetica","",9)
            pdf.cell(8,14,str(i),border=1,align="C",ln=False)
            pdf.set_x(23); pdf.multi_cell(80,7,clean(item["label"]),border=1)
            ya = pdf.get_y(); pdf.set_xy(103,y); pdf.multi_cell(92,7,clean(item["rule"]),border=1)
            pdf.set_y(max(ya, pdf.get_y()))
        pdf.ln(3)

    if risk["partial_items"]:
        sec(f"SECTION 4 - PARTIAL / UNCLEAR ITEMS ({risk['partial_count']}) - Review recommended")
        pdf.set_x(15); pdf.set_font("Helvetica","B",9)
        pdf.cell(8,7,"No.",border=1,align="C")
        pdf.cell(60,7,"Item",border=1)
        pdf.cell(112,7,"Finding & Rule",border=1,ln=True)
        for i, item in enumerate(risk["partial_items"],1):
            detail  = clean(item.get("detail","")) or "Incomplete"
            rule    = clean(item.get("rule",""))
            combined= f"{detail} | {rule}"
            y = pdf.get_y(); pdf.set_x(15); pdf.set_font("Helvetica","",9)
            pdf.cell(8,12,str(i),border=1,align="C",ln=False)
            pdf.cell(60,12,clean(item["label"][:35]),border=1,ln=False)
            pdf.multi_cell(112,6,combined,border=1)
            if pdf.get_y() < y+12: pdf.set_y(y+12)
        pdf.ln(3)

    if fixes:
        sec(f"SECTION 5 - CORRECTIVE SUGGESTIONS ({len(fixes)} items)")
        for i, fix in enumerate(fixes,1):
            pdf.set_x(15); pdf.set_font("Helvetica","B",9)
            pdf.cell(180,6,f"{i}. {clean(fix['title'])}",border="LTR",ln=True)
            pdf.set_x(15); pdf.set_font("Helvetica","",8)
            pdf.multi_cell(180,5,f"Suggestion: {clean(fix['suggestion'])}",border="LR")
            pdf.set_x(15); pdf.multi_cell(180,5,f"Example: {clean(fix['example'])}",border="LR")
            pdf.set_x(15); pdf.multi_cell(180,5,f"Action: {clean(fix['corrective_action'])}",border="LRB")
            pdf.ln(2)
        pdf.ln(3)

    if risk["passed"]:
        sec(f"SECTION 6 - PASSED CHECKS ({risk['passed_count']} items)")
        for i, lbl in enumerate(risk["passed"],1):
            pdf.set_x(15); pdf.set_font("Helvetica","",9)
            pdf.cell(8,6,str(i),border=1,align="C")
            pdf.cell(172,6,f"  [PASS]  {clean(lbl)}",border=1,ln=True)
        pdf.ln(3)

    sec("SECTION 7 - CORRECTIVE ACTION & SIGN-OFF")
    pdf.set_font("Helvetica","",9); pdf.set_x(15)
    pdf.cell(180,6,"Corrective action required:",border="LR",ln=True)
    pdf.set_x(15); pdf.cell(180,8,"",border="LR",ln=True)
    pdf.set_x(15); pdf.cell(180,8,"",border="LR",ln=True)
    pdf.set_x(15); pdf.cell(180,8,"",border="LRB",ln=True)
    pdf.ln(3); pdf.set_x(15); pdf.set_font("Helvetica","B",9)
    pdf.cell(60,7,"Reviewed by:",border=1)
    pdf.cell(60,7,"Approved by:",border=1)
    pdf.cell(60,7,"Date of Closure:",border=1,ln=True)
    pdf.set_x(15); pdf.set_font("Helvetica","",9)
    pdf.cell(60,14,"",border=1); pdf.cell(60,14,"",border=1); pdf.cell(60,14,"",border=1,ln=True)
    pdf.ln(5); pdf.set_font("Helvetica","I",8); pdf.set_text_color(80,80,80)
    pdf.set_x(15); pdf.cell(180,5,f"Generated: {date_str}  {time_str}  |  Report No: {report_no}",align="C",ln=True)

    return bytes(pdf.output())
