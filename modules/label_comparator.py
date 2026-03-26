# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

import difflib
from modules.section_detector import detect_sections
from modules.risk_analyzer import analyze_risk


def compare_labels(old_text: str, new_text: str, mode: str = "cdsco") -> dict:
    """
    Compare old label vs new label.
    Returns structured diff with compliance delta and submission readiness.
    """
    old_lines = [l.strip() for l in old_text.strip().splitlines() if l.strip()]
    new_lines = [l.strip() for l in new_text.strip().splitlines() if l.strip()]

    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    added   = [l[1:].strip() for l in diff if l.startswith("+") and not l.startswith("+++")]
    removed = [l[1:].strip() for l in diff if l.startswith("-") and not l.startswith("---")]

    old_results = detect_sections(old_text, mode=mode)
    new_results = detect_sections(new_text, mode=mode)
    old_risk    = analyze_risk(old_results)
    new_risk    = analyze_risk(new_results)

    newly_fixed  = []
    newly_broken = []
    for old_item, new_item in zip(old_results, new_results):
        if old_item["status"] in ("fail", "partial") and new_item["status"] == "pass":
            newly_fixed.append(new_item["label"])
        elif old_item["status"] == "pass" and new_item["status"] in ("fail", "partial"):
            newly_broken.append(new_item["label"])

    similarity = difflib.SequenceMatcher(None, old_text, new_text).ratio()

    return {
        "added_lines":     added,
        "removed_lines":   removed,
        "old_score":       old_risk["score"],
        "new_score":       new_risk["score"],
        "score_delta":     new_risk["score"] - old_risk["score"],
        "old_risk":        old_risk["risk_level"],
        "new_risk":        new_risk["risk_level"],
        "newly_fixed":     newly_fixed,
        "newly_broken":    newly_broken,
        "similarity":      round(similarity * 100, 1),
        "old_can_release": old_risk["can_release"],
        "new_can_release": new_risk["can_release"],
        "submission_ready": new_risk["can_release"] and len(newly_broken) == 0,
        "old_risk_full":   old_risk,
        "new_risk_full":   new_risk,
    }


def get_submission_status(comparison: dict) -> tuple[str, str]:
    """Returns (status_text, color)."""
    if comparison["submission_ready"]:
        return "READY FOR SUBMISSION", "green"
    if comparison["new_risk"] == "MEDIUM":
        return "NEEDS REVISION", "orange"
    return "HIGH RISK — DO NOT SUBMIT", "red"
