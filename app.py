from modules.ocr_reader import get_label_text
from modules.section_detector import detect_sections
from modules.risk_analyzer import analyze_risk

def run_compliance_check(source, mode="cdsco", is_file=False):
    """
    Full pipeline:
    1. Extract text from label (image or pasted text)
    2. Detect which regulatory sections are present
    3. Score and analyze risk
    4. Print report to terminal
    """
    print("\n" + "="*55)
    print("  PHARMACEUTICAL LABEL COMPLIANCE CHECKER")
    print("="*55)
    print(f"  Mode : {'CDSCO (Indian market)' if mode == 'cdsco' else 'FDA (US market)'}")
    print(f"  Input: {'Image file' if is_file else 'Text input'}")
    print("="*55 + "\n")

    print("Step 1: Extracting label text...")
    label_text = get_label_text(source, is_file=is_file)
    if label_text.startswith("ERROR"):
        print(label_text)
        return
    print(f"  Extracted {len(label_text)} characters of text.\n")

    print("Step 2: Detecting regulatory sections...")
    results = detect_sections(label_text, mode=mode)
    print(f"  Checked {len(results)} items.\n")

    print("Step 3: Calculating compliance score...")
    risk = analyze_risk(results)

    print("\n" + "="*55)
    print("  COMPLIANCE REPORT")
    print("="*55)
    print(f"  Score      : {risk['score']}%")
    print(f"  Risk level : {risk['risk_level']}")
    print(f"  Release    : {'APPROVED' if risk['can_release'] else 'ON HOLD - DO NOT RELEASE'}")
    print(f"  Passed     : {risk['passed_count']} / {risk['total_checks']} checks")
    print("="*55)

    if risk["critical_fails"]:
        print(f"\n  CRITICAL MISSING ({len(risk['critical_fails'])} items):")
        for item in risk["critical_fails"]:
            print(f"    [FAIL] {item['label']}")
            print(f"           Rule: {item['rule']}")

    if risk["partial_items"]:
        print(f"\n  PARTIAL / UNCLEAR ({len(risk['partial_items'])} items):")
        for item in risk["partial_items"]:
            print(f"    [WARN] {item['label']}")
            print(f"           {item['detail']}")

    if risk["passed"]:
        print(f"\n  PASSED ({len(risk['passed'])} items):")
        for label in risk["passed"]:
            print(f"    [PASS] {label}")

    print("\n" + "="*55 + "\n")
    return risk


if __name__ == "__main__":
    sample_label = """
    Metformin Hydrochloride Tablets IP 500 mg
    Batch No. B240312
    Mfg Date: March 2024   Exp Date: February 2026
    Manufactured by: Aurobindo Pharma Ltd, Hyderabad
    Store in a cool place.
    10 Tablets
    """

    run_compliance_check(
        source=sample_label,
        mode="cdsco",
        is_file=False
    )
