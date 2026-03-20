# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Unauthorised commercial use is prohibited.
# Licensed under CC BY-NC 4.0 — see LICENSE file for details.
# Contact: zainanaqi666@gmail.com
def analyze_risk(section_results):
    """
    Takes section detection results and returns a compliance summary.
    Critical items are worth more than non-critical items.
    """
    total_points   = 0
    earned_points  = 0
    critical_fails = []
    partial_items  = []
    passed_items   = []

    for item in section_results:
        weight = 15 if item["critical"] else 10

        total_points += weight

        if item["status"] == "pass":
            earned_points += weight
            passed_items.append(item["label"])

        elif item["status"] == "partial":
            earned_points += weight // 2
            partial_items.append({
                "label":  item["label"],
                "detail": item["found"],
                "rule":   item["rule"]
            })

        else:
            if item["critical"]:
                critical_fails.append({
                    "label": item["label"],
                    "rule":  item["rule"]
                })

    score = round((earned_points / total_points) * 100) if total_points else 0

    if score >= 85:
        risk_level = "LOW"
    elif score >= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    can_release = (risk_level == "LOW" and len(critical_fails) == 0)

    return {
        "score":          score,
        "risk_level":     risk_level,
        "can_release":    can_release,
        "passed":         passed_items,
        "critical_fails": critical_fails,
        "partial_items":  partial_items,
        "total_checks":   len(section_results),
        "passed_count":   len(passed_items),
        "fail_count":     len(critical_fails),
        "partial_count":  len(partial_items)
    }
