# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com


def analyze_risk(section_results: list[dict]) -> dict:
    """
    Converts section detection results into a compliance summary.
    Critical items (15 pts) weighted higher than non-critical (10 pts).
    """
    if not section_results:
        return {
            "score": 0, "risk_level": "HIGH", "can_release": False,
            "passed": [], "critical_fails": [], "partial_items": [],
            "total_checks": 0, "passed_count": 0,
            "fail_count": 0, "partial_count": 0,
        }

    total_points  = 0
    earned_points = 0
    critical_fails = []
    partial_items  = []
    passed_items   = []

    for item in section_results:
        weight = 15 if item.get("critical") else 10
        total_points += weight

        if item["status"] == "pass":
            earned_points += weight
            passed_items.append(item["label"])

        elif item["status"] == "partial":
            earned_points += weight // 2
            partial_items.append({
                "label":  item["label"],
                "detail": item.get("found") or "Incomplete",
                "rule":   item.get("rule", ""),
                "id":     item.get("id", ""),
            })

        else:
            if item.get("critical"):
                critical_fails.append({
                    "label": item["label"],
                    "rule":  item.get("rule", ""),
                    "id":    item.get("id", ""),
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
        "partial_count":  len(partial_items),
    }
