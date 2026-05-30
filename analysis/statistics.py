# -*- coding: utf-8 -*-
"""扩展时空统计分析"""

from typing import Any, Dict, List, Optional

import numpy as np
import xarray as xr

from analysis.nc_reader import nc_reader
from analysis.coords import (
    normalize_longitude,
    nearest_index,
    select_region,
    get_coord_value,
    parse_time_index,
)


def _require_open():
    if nc_reader.dataset is None:
        return {"success": False, "message": "请先打开文件"}
    return None


def _resolve_variable(variable_name: str):
    if variable_name in nc_reader.dataset.data_vars:
        return variable_name
    return None


def extract_point_stats(
    variable_name: str,
    latitude: float,
    longitude: float,
    start_time_idx: Optional[int] = None,
    end_time_idx: Optional[int] = None,
    stat: str = "mean",
) -> Dict[str, Any]:
    err = _require_open()
    if err:
        return err
    if _resolve_variable(variable_name) is None:
        return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

    lon = normalize_longitude(longitude, nc_reader.dataset[nc_reader.lon_name].values)
    lat_idx = nearest_index(nc_reader.dataset[nc_reader.lat_name].values, latitude)
    lon_idx = nearest_index(nc_reader.dataset[nc_reader.lon_name].values, lon)

    var = nc_reader.dataset[variable_name]
    series = var.isel({nc_reader.lat_name: lat_idx, nc_reader.lon_name: lon_idx})
    if nc_reader.time_name and nc_reader.time_name in series.dims:
        if start_time_idx is not None and end_time_idx is not None:
            series = series.isel({nc_reader.time_name: slice(start_time_idx, end_time_idx + 1)})
        values = series.values.astype(float)
    else:
        values = np.array([float(series.values)])

    value = _stat_on_array(values, stat)
    return {
        "success": True,
        "query": {
            "variable": variable_name,
            "location": {"latitude": latitude, "longitude": longitude},
            "stat": stat,
            "time_range_idx": [start_time_idx, end_time_idx],
        },
        "result": {"value": value, "units": var.attrs.get("units", "未知")},
        "metadata": {
            "file": nc_reader.file_path,
            "grid_point": {
                "latitude": get_coord_value(nc_reader.dataset, nc_reader.lat_name, lat_idx),
                "longitude": get_coord_value(nc_reader.dataset, nc_reader.lon_name, lon_idx),
            },
            "n_samples": len(values.flatten()),
        },
    }


def extract_area_stats(
    variable_name: str,
    lon_min: float, lon_max: float, lat_min: float, lat_max: float,
    stat: str = "mean",
    time_index: Optional[int] = None,
    time_avg: bool = False,
) -> Dict[str, Any]:
    err = _require_open()
    if err:
        return err
    if _resolve_variable(variable_name) is None:
        return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

    var = nc_reader.dataset[variable_name]
    sel_var = select_region(var, nc_reader.lat_name, nc_reader.lon_name, lat_min, lat_max, lon_min, lon_max)

    if time_avg and nc_reader.time_name and nc_reader.time_name in sel_var.dims:
        sel_var = sel_var.mean(dim=nc_reader.time_name)
    elif time_index is not None and nc_reader.time_name and nc_reader.time_name in sel_var.dims:
        sel_var = sel_var.isel({nc_reader.time_name: time_index})

    value = nc_reader._compute_stat(sel_var, stat)
    if value is None:
        return {"success": False, "message": f"不支持的统计方法: {stat}"}

    return {
        "success": True,
        "query": {
            "variable": variable_name,
            "region": {"lon": [lon_min, lon_max], "lat": [lat_min, lat_max]},
            "stat": stat,
            "time_index": time_index,
            "time_avg": time_avg,
        },
        "result": {"value": value, "units": var.attrs.get("units", "未知")},
        "metadata": {"file": nc_reader.file_path, "n_samples": int(sel_var.size)},
    }


def extract_extreme_events(
    variable_name: str,
    threshold: float,
    longitude: float,
    latitude: float,
    start_time_idx: Optional[int] = None,
    end_time_idx: Optional[int] = None,
) -> Dict[str, Any]:
    err = _require_open()
    if err:
        return err

    series_result = extract_point_series_raw(
        variable_name, longitude, latitude, start_time_idx, end_time_idx
    )
    if not series_result.get("success"):
        return series_result

    values = np.array(series_result["values"], dtype=float)
    exceed = values > threshold
    count = int(np.sum(exceed))

    return {
        "success": True,
        "query": {
            "variable": variable_name,
            "threshold": threshold,
            "location": {"latitude": latitude, "longitude": longitude},
        },
        "result": {
            "exceed_count": count,
            "total_count": len(values),
            "exceed_ratio": round(count / len(values), 4) if len(values) else 0,
            "max_value": float(np.max(values)) if len(values) else None,
        },
        "metadata": {"file": nc_reader.file_path},
    }


def extract_point_series_raw(
    variable_name, longitude, latitude, start_time_idx, end_time_idx
):
    lon = normalize_longitude(longitude, nc_reader.dataset[nc_reader.lon_name].values)
    lat_idx = nearest_index(nc_reader.dataset[nc_reader.lat_name].values, latitude)
    lon_idx = nearest_index(nc_reader.dataset[nc_reader.lon_name].values, lon)
    var = nc_reader.dataset[variable_name]
    series = var.isel({nc_reader.lat_name: lat_idx, nc_reader.lon_name: lon_idx})
    if nc_reader.time_name and nc_reader.time_name in series.dims:
        if start_time_idx is not None and end_time_idx is not None:
            series = series.isel({nc_reader.time_name: slice(start_time_idx, end_time_idx + 1)})
        values = series.values.tolist()
    else:
        values = [float(series.values)]
    return {"success": True, "values": values}


def compare_sources(
    file_paths: List[str],
    variable_name: str,
    latitude: float,
    longitude: float,
    time_index: Optional[int] = None,
) -> Dict[str, Any]:
    results = []
    for fp in file_paths:
        nc_reader.open_file(fp)
        r = nc_reader.extract_location_data(variable_name, latitude, longitude, time_index)
        results.append({"file": fp, "success": r.get("success"), "value": r.get("data", {}).get("value")})
    nc_reader.close_file()

    valid = [x for x in results if x.get("value") is not None]
    if len(valid) >= 2:
        diff = abs(valid[0]["value"] - valid[1]["value"])
        mean_val = sum(x["value"] for x in valid) / len(valid)
    else:
        diff = None
        mean_val = valid[0]["value"] if valid else None

    return {
        "success": True,
        "query": {"variable": variable_name, "files": file_paths},
        "result": {"comparisons": results, "mean": mean_val, "max_diff": diff},
    }


def query_by_datetime(datetime_str: str) -> Dict[str, Any]:
    return nc_reader.query_by_datetime(datetime_str)


def _stat_on_array(values, stat: str):
    arr = np.asarray(values, dtype=float)
    if stat == "mean":
        return float(np.nanmean(arr))
    if stat == "max":
        return float(np.nanmax(arr))
    if stat == "min":
        return float(np.nanmin(arr))
    if stat == "std":
        return float(np.nanstd(arr))
    if stat == "var":
        return float(np.nanvar(arr))
    if stat == "p90":
        return float(np.nanpercentile(arr, 90))
    if stat == "p95":
        return float(np.nanpercentile(arr, 95))
    return None
