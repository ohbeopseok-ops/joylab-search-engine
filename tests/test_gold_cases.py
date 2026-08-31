import json
from pathlib import Path

import jsonschema

from engine.trust_layer import evaluate_case

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "gold_case.schema.json").read_text(encoding="utf-8"))


def load_case(name: str):
    return json.loads((ROOT / "gold_cases" / name).read_text(encoding="utf-8"))


def expected(case):
    if "expected_gate_results" in case:
        return case["expected_gate_results"], case["expected_overall_result"]
    legacy = {k: v["status"] for k, v in case["gate_results"].items()}
    return legacy, case["overall_result"]


def assert_case(filename: str):
    case = load_case(filename)
    jsonschema.Draft202012Validator(SCHEMA).validate(case)
    actual = evaluate_case(case)
    exp_gates, exp_overall = expected(case)
    assert actual["gate_results"] == exp_gates
    assert actual["overall_result"] == exp_overall


def test_gold_001_pass_path():
    assert_case("GOLD_001_SAMSUNG_ELECTRONICS_Q2_2026.json")


def test_gold_002_fail_path():
    assert_case("GOLD_002_FAIL.json")


def test_gold_003_unknown_path():
    assert_case("GOLD_003_UNKNOWN.json")


def test_unknown_never_promoted_to_pass():
    case = load_case("GOLD_003_UNKNOWN.json")
    actual = evaluate_case(case)
    assert "UNKNOWN" in actual["gate_results"].values()
    assert actual["overall_result"] == "UNKNOWN"
    assert actual["overall_result"] != "PASS"
