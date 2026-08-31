from __future__ import annotations

from datetime import datetime
from typing import Dict, Any

STATUSES = {"PASS", "FAIL", "UNKNOWN"}


def _source_map(case: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {s["id"]: s for s in case.get("sources", [])}


def evaluate_g1(case: Dict[str, Any]) -> str:
    sources = _source_map(case)
    material_facts = [s for s in case.get("statements", []) if s.get("type") == "FACT"]
    if not material_facts:
        return "UNKNOWN"
    saw_unknown = False
    for statement in material_facts:
        ids = statement.get("source_ids") or []
        if not ids:
            return "FAIL"
        for sid in ids:
            source = sources.get(sid)
            if not source:
                saw_unknown = True
                continue
            tier = source.get("tier")
            if tier is None or not source.get("url"):
                saw_unknown = True
            elif tier == 4:
                return "FAIL"
    return "UNKNOWN" if saw_unknown else "PASS"


def evaluate_g2(case: Dict[str, Any]) -> str:
    metadata = case.get("metadata", {})
    required = [metadata.get(k) for k in ("source_date", "observed_at", "data_period", "updated_at")]
    if any(v in (None, "") for v in required):
        return "UNKNOWN"
    current_language = any(
        token in (s.get("text") or "").lower()
        for s in case.get("statements", [])
        for token in ("currently", "latest price", "current price", "지금", "현재")
    )
    if current_language:
        try:
            source_date = datetime.fromisoformat(str(metadata["source_date"])[:10])
            observed = datetime.fromisoformat(str(metadata["observed_at"]).replace("Z", "+00:00"))
            if (observed.date() - source_date.date()).days > 7:
                return "FAIL"
        except ValueError:
            return "UNKNOWN"
    return "PASS"


def evaluate_g3(case: Dict[str, Any]) -> str:
    statements = case.get("statements", [])
    if not statements:
        return "UNKNOWN"
    certainty_terms = ("definitely", "certainly", "guaranteed", "확정", "무조건", "반드시")
    future_terms = ("next quarter", "will ", "forecast", "outlook", "전망", "예상")
    for s in statements:
        text = (s.get("text") or "").lower()
        stype = s.get("type")
        reported = s.get("reported_or_calculated")
        if stype not in {"FACT", "INTERPRETATION", "FORECAST", "OPINION"}:
            return "UNKNOWN"
        if stype == "FACT" and any(t in text for t in future_terms) and any(t in text for t in certainty_terms):
            return "FAIL"
        if stype == "FACT" and reported == "REPORTED" and "will " in text:
            return "FAIL"
    return "PASS"


def evaluate_g4(case: Dict[str, Any]) -> str:
    sources = _source_map(case)
    saw_unknown = False
    for s in case.get("statements", []):
        if s.get("type") != "FACT":
            continue
        ids = s.get("source_ids") or []
        if not ids:
            return "FAIL"
        for sid in ids:
            source = sources.get(sid)
            if not source or not source.get("url"):
                saw_unknown = True
    return "UNKNOWN" if saw_unknown else "PASS"


def evaluate_g5(case: Dict[str, Any]) -> str:
    check = case.get("investment_language_check")
    if not isinstance(check, dict):
        return "UNKNOWN"
    required = (
        "guaranteed_return_language",
        "mandatory_buy_language",
        "absolute_price_direction_claim",
        "risk_or_uncertainty_present",
    )
    if any(k not in check for k in required):
        return "UNKNOWN"
    if check["guaranteed_return_language"] or check["mandatory_buy_language"] or check["absolute_price_direction_claim"]:
        return "FAIL"
    return "PASS"


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    gates = {
        "G1_SOURCE": evaluate_g1(case),
        "G2_FRESHNESS": evaluate_g2(case),
        "G3_FACT_SEPARATION": evaluate_g3(case),
        "G4_CITATION": evaluate_g4(case),
        "G5_INVESTMENT_CONTENT": evaluate_g5(case),
    }
    if "FAIL" in gates.values():
        overall = "FAIL"
    elif "UNKNOWN" in gates.values():
        overall = "UNKNOWN"
    else:
        overall = "PASS"
    return {"gate_results": gates, "overall_result": overall}
