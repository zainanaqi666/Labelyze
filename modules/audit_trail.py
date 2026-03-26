# © 2026 Zaina Naqi. All rights reserved.
# Labelyze — AI-Powered Pharmaceutical Label Compliance Tool
# Licensed under CC BY-NC 4.0
# Contact: zainanaqi666@gmail.com

import json
import os
import datetime

AUDIT_FILE = "labelyze_audit_trail.json"
MAX_RECORDS = 200


def _load() -> list:
    if not os.path.exists(AUDIT_FILE):
        return []
    try:
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save(records: list) -> None:
    try:
        with open(AUDIT_FILE, "w", encoding="utf-8") as f:
            json.dump(records[-MAX_RECORDS:], f, indent=2)
    except Exception:
        pass


def log_check(label_text: str, mode: str, label_type: str,
              risk: dict, drug_info: dict | None = None) -> dict:
    records = _load()
    mode_labels = {
        "cdsco": "CDSCO / Schedule M",
        "fda":   "FDA 21 CFR 201",
        "ema":   "EU EMA Directive 2001/83/EC",
    }
    entry = {
        "id":            len(records) + 1,
        "timestamp":     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date":          datetime.datetime.now().strftime("%d-%b-%Y"),
        "time":          datetime.datetime.now().strftime("%H:%M"),
        "mode":          mode_labels.get(mode, mode),
        "label_type":    label_type,
        "drug_name":     (label_text.strip().split("\n")[0][:60] if label_text else "Unknown"),
        "score":         risk.get("score", 0),
        "risk_level":    risk.get("risk_level", "UNKNOWN"),
        "can_release":   risk.get("can_release", False),
        "passed":        risk.get("passed_count", 0),
        "total":         risk.get("total_checks", 0),
        "critical_fails": risk.get("fail_count", 0),
        "drug_schedule": drug_info["label"] if drug_info else "Not identified",
        "label_preview": (label_text[:200].replace("\n", " ") if label_text else ""),
    }
    records.append(entry)
    _save(records)
    return entry


def load_audit() -> list:
    return _load()


def get_audit_summary() -> dict | None:
    records = _load()
    if not records:
        return None
    total    = len(records)
    approved = sum(1 for r in records if r.get("can_release"))
    high     = sum(1 for r in records if r.get("risk_level") == "HIGH")
    avg      = sum(r.get("score", 0) for r in records) / total
    return {
        "total_checks": total,
        "approved":     approved,
        "on_hold":      total - approved,
        "high_risk":    high,
        "avg_score":    round(avg, 1),
        "last_check":   records[-1]["timestamp"],
    }


def clear_audit() -> None:
    _save([])
