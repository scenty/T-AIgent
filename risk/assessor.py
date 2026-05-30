# -*- coding: utf-8 -*-
"""灾害风险综合评估"""

from typing import Any, Dict, List, Optional

from risk.standards import assess_element, merge_levels, load_rules, level_name

# 会话级上下文，供简报模块引用
session_context = {
    "last_stats": [],
    "last_risk": None,
    "last_catalog_summary": None,
}


def assess_sea_state(
    wave_height: Optional[float] = None,
    surge_height: Optional[float] = None,
    wind_speed: Optional[float] = None,
    location: Optional[str] = None,
    time_label: Optional[str] = None,
) -> Dict[str, Any]:
    rules = load_rules()
    assessments = []

    if wave_height is not None:
        assessments.append(assess_element(wave_height, "wave", rules))
    if surge_height is not None:
        assessments.append(assess_element(surge_height, "surge", rules))
    if wind_speed is not None:
        assessments.append(assess_element(wind_speed, "wind", rules))

    if not assessments:
        return {"success": False, "message": "请至少提供一个要素数值（wave_height/surge_height/wind_speed）"}

    comp_level = merge_levels([a["level_id"] for a in assessments], rules.get("comprehensive_strategy", "max_level"))
    advice = rules.get("advice", {}).get(comp_level, "")

    result = {
        "success": True,
        "location": location,
        "time": time_label,
        "assessments": assessments,
        "comprehensive": {
            "level_id": comp_level,
            "level_name": level_name(rules, comp_level),
            "advice": advice,
        },
    }
    session_context["last_risk"] = result
    return result


def assess_comprehensive_risk(
    stats_results: List[Dict[str, Any]],
    location: Optional[str] = None,
    time_label: Optional[str] = None,
) -> Dict[str, Any]:
    """从统计结果 JSON 列表自动识别要素并评估"""
    wave_height = None
    surge_height = None
    wind_speed = None

    wave_vars = {"swh", "hs", "wave_height", "significant_wave_height"}
    surge_vars = {"ssh", "surge", "storm_surge", "zeta", "eta"}
    wind_vars = {"wind_speed", "ws", "speed", "u10", "v10", "uwnd", "vwnd"}

    for item in stats_results:
        var = (item.get("query") or {}).get("variable", "")
        var_lower = var.lower()
        val = (item.get("result") or item.get("data") or {}).get("value")
        if val is None:
            val = item.get("data", {}).get("value") if isinstance(item.get("data"), dict) else None
        if val is None:
            continue
        if var_lower in wave_vars or "swh" in var_lower or "wave" in var_lower:
            wave_height = float(val)
        elif var_lower in surge_vars or "surge" in var_lower or "ssh" in var_lower:
            surge_height = float(val)
        elif var_lower in wind_vars or "wind" in var_lower:
            wind_speed = float(val)

    session_context["last_stats"] = stats_results
    return assess_sea_state(wave_height, surge_height, wind_speed, location, time_label)


def assess_region_risk(
    wave_height: Optional[float] = None,
    surge_height: Optional[float] = None,
    wind_speed: Optional[float] = None,
    region_name: Optional[str] = None,
    time_label: Optional[str] = None,
) -> Dict[str, Any]:
    result = assess_sea_state(wave_height, surge_height, wind_speed, region_name, time_label)
    if result.get("success"):
        result["scope"] = "region"
        result["region_name"] = region_name
    return result


def get_risk_criteria() -> Dict[str, Any]:
    from risk.standards import get_criteria_text
    return {"success": True, "criteria": get_criteria_text()}
