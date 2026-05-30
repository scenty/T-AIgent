# -*- coding: utf-8 -*-
"""中国海洋预警等级标准"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_PATH = BASE_DIR / "config" / "risk_rules.yaml"

LEVEL_ORDER = ["none", "blue", "yellow", "orange", "red"]


def load_rules() -> dict:
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def value_to_level(value: float, thresholds: dict) -> str:
    if value >= thresholds.get("red", float("inf")):
        return "red"
    if value >= thresholds.get("orange", float("inf")):
        return "orange"
    if value >= thresholds.get("yellow", float("inf")):
        return "yellow"
    if value >= thresholds.get("blue", float("inf")):
        return "blue"
    return "none"


def level_name(rules: dict, level_id: str) -> str:
    for lv in rules.get("levels", []):
        if lv["id"] == level_id:
            return lv["name"]
    return level_id


def assess_element(value: float, element: str, rules: Optional[dict] = None) -> Dict[str, Any]:
    rules = rules or load_rules()
    elem_rules = rules.get(element, {})
    thresholds = elem_rules.get("thresholds", {})
    level_id = value_to_level(value, thresholds)
    return {
        "element": element,
        "value": value,
        "unit": elem_rules.get("unit", ""),
        "level_id": level_id,
        "level_name": level_name(rules, level_id),
        "reference": elem_rules.get("reference", ""),
        "thresholds": thresholds,
    }


def merge_levels(levels: List[str], strategy: str = "max_level") -> str:
    if not levels:
        return "none"
    if strategy == "max_level":
        best = "none"
        for lv in levels:
            if LEVEL_ORDER.index(lv) > LEVEL_ORDER.index(best):
                best = lv
        return best
    return levels[0]


def get_criteria_text() -> str:
    rules = load_rules()
    lines = ["# 当前风险判定依据", ""]
    for elem in ("wave", "surge", "wind"):
        r = rules.get(elem, {})
        lines.append(f"## {elem}")
        lines.append(f"- 单位: {r.get('unit', '')}")
        lines.append(f"- 参考: {r.get('reference', '')}")
        for k, v in r.get("thresholds", {}).items():
            lines.append(f"  - {level_name(rules, k)}: >= {v}")
        lines.append("")
    lines.append(f"综合策略: {rules.get('comprehensive_strategy', 'max_level')}")
    return "\n".join(lines)
