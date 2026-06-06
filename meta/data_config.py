# -*- coding: utf-8 -*-
"""data_roots.yaml 配置加载：根目录、站点、layout、变量"""

import re
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_ROOTS_PATH = BASE_DIR / "config" / "data_roots.yaml"


def load_data_roots() -> dict:
    if DATA_ROOTS_PATH.exists():
        with open(DATA_ROOTS_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {"roots": [], "stations": []}


def station_id_to_file_code(station_id: str) -> Optional[str]:
    if not station_id:
        return None
    sid = station_id.strip()
    if sid.startswith("S") and len(sid) > 1:
        return sid[1:]
    return sid


def parse_station_code_from_path(file_path: str, pattern: Optional[str] = None) -> Optional[str]:
    name = Path(file_path).name
    if pattern:
        regex = pattern.replace("{station_code}", r"(?P<code>[^_/]+)")
        regex = regex.replace("*", ".*")
        match = re.match(regex, name, re.IGNORECASE)
        if match and match.groupdict().get("code"):
            return match.group("code")
    match = re.search(r"EC_point_wave_([^_]+)_", name, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r"storm_surge_forecast_sp_([^_]+)_", name, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def match_root_for_path(file_path: str, cfg: Optional[dict] = None) -> Optional[dict]:
    cfg = cfg or load_data_roots()
    path_norm = str(Path(file_path)).replace("\\", "/").lower()
    best = None
    best_len = -1
    for root in cfg.get("roots", []):
        root_path = str(root.get("path", "")).replace("\\", "/").strip("./").lower()
        if not root_path:
            continue
        if root_path in path_norm or path_norm.startswith(root_path):
            if len(root_path) > best_len:
                best = root
                best_len = len(root_path)
    return best


def collect_variables_for_root(root: dict) -> Dict[str, List[str]]:
    variables = root.get("variables") or {}
    return {k: list(v) for k, v in variables.items()}


def match_elements_from_variables(var_names: List[str], cfg: Optional[dict] = None) -> List[str]:
    cfg = cfg or load_data_roots()
    lower_vars = {v.lower() for v in var_names}
    elements = []
    for root in cfg.get("roots", []):
        for elem, names in (root.get("variables") or {}).items():
            if elem in elements:
                continue
            for name in names:
                if name.lower() in lower_vars:
                    elements.append(elem)
                    break
    return elements


def infer_layout_mode(
    variable_dims: Dict[str, List[str]],
    lat_name: Optional[str],
    lon_name: Optional[str],
    dimensions: Dict[str, int],
    root_layout: Optional[dict] = None,
) -> str:
    data_vars = {
        k: v for k, v in variable_dims.items()
        if k not in ("station_name",) and v
    }
    if not data_vars:
        return (root_layout or {}).get("access_mode", "grid")

    sample_dims = next(iter(data_vars.values()))
    has_lat = lat_name and lat_name in sample_dims
    has_lon = lon_name and lon_name in sample_dims
    if has_lat and has_lon:
        nlat = dimensions.get(lat_name, 1)
        nlon = dimensions.get(lon_name, 1)
        if nlat <= 1 and nlon <= 1:
            return "grid_1x1"
        return "grid"
    if "time" in sample_dims and not has_lat and not has_lon:
        return "time_series"
    return (root_layout or {}).get("access_mode", "grid")


def lookup_station(
    name: Optional[str] = None,
    file_code: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    element: Optional[str] = None,
) -> Dict[str, Any]:
    cfg = load_data_roots()
    stations = cfg.get("stations") or []
    matches = []

    query = (name or "").strip()
    code_query = (file_code or "").strip()

    for st in stations:
        if element and element not in (st.get("elements") or []):
            continue
        if code_query and st.get("file_code") != code_query:
            continue
        if query:
            names = [st.get("name", "")]
            names.extend(st.get("aliases") or [])
            if not any(query in n or n in query for n in names if n):
                continue
        matches.append(st)

    if latitude is not None and longitude is not None and not query and not code_query:
        def dist(st):
            return (float(st.get("lat", 0)) - latitude) ** 2 + (float(st.get("lon", 0)) - longitude) ** 2
        stations_filtered = [s for s in stations if s.get("lat") is not None]
        if element:
            stations_filtered = [s for s in stations_filtered if element in (s.get("elements") or [])]
        if stations_filtered:
            nearest = min(stations_filtered, key=dist)
            matches = [nearest]

    results = []
    for st in matches:
        root_hint = None
        filename_pattern = None
        for root in cfg.get("roots", []):
            if element and root.get("element") != element:
                continue
            if st.get("type") == "tide" and root.get("element") == "wave":
                continue
            if st.get("file_code") and root.get("layout", {}).get("filename_pattern"):
                root_hint = root.get("path")
                filename_pattern = root["layout"]["filename_pattern"]
                break
        entry = {
            "station_id": st.get("station_id"),
            "file_code": st.get("file_code"),
            "name": st.get("name"),
            "aliases": st.get("aliases") or [],
            "lat": st.get("lat"),
            "lon": st.get("lon"),
            "type": st.get("type"),
            "elements": st.get("elements") or [],
            "data_root": root_hint,
            "filename_pattern": filename_pattern,
        }
        if entry["file_code"] and filename_pattern:
            entry["nc_filename_example"] = filename_pattern.replace("{station_code}", entry["file_code"])
        results.append(entry)

    if not results:
        return {"success": False, "message": "未找到匹配站点", "query": {"name": name, "file_code": file_code}}

    return {"success": True, "count": len(results), "stations": results}
