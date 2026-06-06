# -*- coding: utf-8 -*-
"""NC 产品类型自动分类"""

from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import yaml
import xarray as xr

from analysis.coords import get_lat_lon_time_names
from meta.data_config import (
    infer_layout_mode,
    match_elements_from_variables,
    match_root_for_path,
    parse_station_code_from_path,
)

BASE_DIR = Path(__file__).resolve().parent.parent
VAR_MAP_PATH = BASE_DIR / "config" / "variable_map.yaml"
DATA_ROOTS_PATH = BASE_DIR / "config" / "data_roots.yaml"


def load_variable_map():
    if VAR_MAP_PATH.exists():
        with open(VAR_MAP_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {"elements": {}, "path_keywords": {}}


def load_grid_threshold():
    if DATA_ROOTS_PATH.exists():
        with open(DATA_ROOTS_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        return cfg.get("grid_threshold", 100)
    return 100


def match_element(var_names: List[str], var_map: dict) -> List[str]:
    elements = match_elements_from_variables(var_names)
    if elements:
        return elements
    lower_vars = {v.lower() for v in var_names}
    for elem, info in var_map.get("elements", {}).items():
        for v in info.get("variables", []):
            if v.lower() in lower_vars:
                elements.append(elem)
                break
    return elements


def match_path_keywords(path: str, var_map: dict) -> List[str]:
    tags = []
    lower_path = path.lower()
    for tag, keywords in var_map.get("path_keywords", {}).items():
        for kw in keywords:
            if kw.lower() in lower_path:
                tags.append(tag)
                break
    return tags


def classify_file_meta(meta: dict) -> dict:
    var_map = load_variable_map()
    threshold = load_grid_threshold()
    path = meta.get("path", "")
    var_names = meta.get("variables", [])
    dims = meta.get("dimensions", {})

    lat_name = meta.get("lat_name")
    lon_name = meta.get("lon_name")
    time_name = meta.get("time_name")
    variable_dims = meta.get("variable_dims", {})

    root = match_root_for_path(path)
    root_layout = (root or {}).get("layout")
    layout_mode = infer_layout_mode(variable_dims, lat_name, lon_name, dims, root_layout)

    elements = match_element(var_names, var_map)
    path_tags = match_path_keywords(path, var_map)

    if root and root.get("product_type"):
        product_type = root.get("product_type")
    elif lat_name and lon_name:
        nlat = dims.get(lat_name, 0)
        nlon = dims.get(lon_name, 0)
        if nlat <= 1 and nlon <= 1:
            product_type = "point_ai"
        elif max(nlat, nlon) >= threshold:
            product_type = "large_grid"
        else:
            product_type = "small_grid"
    elif time_name and len(dims) <= 2:
        product_type = "point_ai"
    else:
        product_type = "unknown"

    if "field_ai" in path_tags or "ai" in path.lower():
        if product_type in ("large_grid", "small_grid"):
            product_type = "field_ai"

    if "point_ai" in path_tags:
        product_type = "point_ai"

    disaster_types = []
    for elem in elements:
        if elem in ("wave", "surge"):
            disaster_types.append(elem)

    filename_pattern = (root_layout or {}).get("filename_pattern")
    station_code = parse_station_code_from_path(path, filename_pattern)

    return {
        "elements": elements,
        "product_type": product_type,
        "disaster_types": disaster_types,
        "path_tags": path_tags,
        "layout_mode": layout_mode,
        "variable_dims": variable_dims,
        "station_code": station_code,
        "layout_source": root.get("path") if root else None,
    }


def extract_file_meta(file_path: str) -> Dict[str, Any]:
    var_map = load_variable_map()
    ds = xr.open_dataset(file_path, decode_times=False)
    lat_name, lon_name, time_name = get_lat_lon_time_names(ds)

    dims = {k: int(v) for k, v in ds.sizes.items()}
    variables = list(ds.data_vars.keys())
    coords = list(ds.coords.keys())
    variable_dims = {name: list(ds[name].dims) for name in ds.data_vars}

    bbox = None
    if lat_name and lon_name:
        lat_vals = ds[lat_name].values
        lon_vals = ds[lon_name].values
        bbox = {
            "lat_min": float(np_min(lat_vals)),
            "lat_max": float(np_max(lat_vals)),
            "lon_min": float(np_min(lon_vals)),
            "lon_max": float(np_max(lon_vals)),
        }

    time_range = None
    if time_name:
        tvals = ds[time_name].values
        if len(tvals) > 0:
            time_range = {"start": str(tvals[0]), "end": str(tvals[-1]), "count": len(tvals)}

    meta = {
        "path": file_path,
        "dimensions": dims,
        "variables": variables,
        "coordinates": coords,
        "variable_dims": variable_dims,
        "global_attributes": {k: str(v)[:200] for k, v in ds.attrs.items()},
        "lat_name": lat_name,
        "lon_name": lon_name,
        "time_name": time_name,
        "bbox": bbox,
        "time_range": time_range,
        "readable": True,
    }
    ds.close()

    classification = classify_file_meta(meta)
    meta.update(classification)
    meta["elements_detail"] = {
        elem: var_map.get("elements", {}).get(elem, {}).get("canonical", elem)
        for elem in classification.get("elements", [])
    }
    root = match_root_for_path(file_path)
    if root and root.get("variables"):
        meta["root_variables"] = root.get("variables")
    return meta


def np_min(arr):
    return float(np.min(arr))


def np_max(arr):
    return float(np.max(arr))
