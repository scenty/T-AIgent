# -*- coding: utf-8 -*-
"""NetCDF 文件读取器（坐标自适应）"""

import numpy as np
import xarray as xr
from typing import Dict, Any, Optional

from analysis.coords import (
    get_lat_lon_time_names,
    normalize_longitude,
    nearest_index,
    select_region,
    get_coord_value,
    parse_time_index,
)


class NCFileReader:
    def __init__(self):
        self.dataset = None
        self.file_path = None
        self.lat_name = None
        self.lon_name = None
        self.time_name = None

    def _refresh_coords(self):
        if self.dataset is not None:
            self.lat_name, self.lon_name, self.time_name = get_lat_lon_time_names(self.dataset)

    def open_file(self, file_path: str) -> Dict[str, Any]:
        if self.dataset is not None:
            self.dataset.close()
            self.dataset = None
        self.dataset = xr.open_dataset(file_path)
        self.file_path = file_path
        self._refresh_coords()
        return {
            "success": True,
            "message": f"成功打开文件: {file_path}",
            "coords": {"lat": self.lat_name, "lon": self.lon_name, "time": self.time_name},
            "file_info": str(self.dataset),
        }

    def get_file_info(self) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        info = {
            "dimensions": dict(self.dataset.sizes),
            "variables": list(self.dataset.data_vars.keys()),
            "coordinates": list(self.dataset.coords.keys()),
            "global_attributes": {k: str(v) for k, v in self.dataset.attrs.items()},
            "coord_names": {"lat": self.lat_name, "lon": self.lon_name, "time": self.time_name},
        }
        return {"success": True, "file_info": info}

    def read_variable(
        self, variable_name: str,
        time_index: Optional[int] = None,
        lat_index: Optional[int] = None,
        lon_index: Optional[int] = None,
    ) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        if variable_name not in self.dataset.data_vars:
            return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

        var_data = self.dataset[variable_name]
        if time_index is not None and self.time_name and self.time_name in var_data.dims:
            var_data = var_data.isel({self.time_name: time_index})
        if lat_index is not None and self.lat_name and self.lat_name in var_data.dims:
            var_data = var_data.isel({self.lat_name: lat_index})
        if lon_index is not None and self.lon_name and self.lon_name in var_data.dims:
            var_data = var_data.isel({self.lon_name: lon_index})

        result = {
            "variable_name": variable_name,
            "dimensions": list(var_data.dims),
            "shape": var_data.shape,
            "values": var_data.values.tolist() if var_data.size < 100 else "数据量过大，请指定具体位置",
            "attributes": dict(var_data.attrs),
        }
        return {"success": True, "data": result}

    def extract_location_data(
        self, variable_name: str, latitude: float, longitude: float,
        time_index: Optional[int] = None,
    ) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        if not self.lat_name or not self.lon_name:
            return {"success": False, "message": "文件缺少经纬度坐标"}

        lon = normalize_longitude(longitude, self.dataset[self.lon_name].values)
        lat_idx = nearest_index(self.dataset[self.lat_name].values, latitude)
        lon_idx = nearest_index(self.dataset[self.lon_name].values, lon)

        sel = {self.lat_name: lat_idx, self.lon_name: lon_idx}
        if time_index is not None and self.time_name:
            sel[self.time_name] = time_index
        data = self.dataset[variable_name].isel(**sel)

        result = {
            "variable": variable_name,
            "latitude": get_coord_value(self.dataset, self.lat_name, lat_idx),
            "longitude": get_coord_value(self.dataset, self.lon_name, lon_idx),
            "value": float(data.values),
            "units": self.dataset[variable_name].attrs.get("units", "未知"),
        }
        return {"success": True, "data": result, "metadata": {"file": self.file_path}}

    def extract_area_stat(
        self, variable_name: str,
        lon_min: float, lon_max: float, lat_min: float, lat_max: float,
        stat: str = "mean", time_index: Optional[int] = None,
    ) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        if variable_name not in self.dataset.data_vars:
            return {"success": False, "message": f"变量 '{variable_name}' 不存在"}
        if not self.lat_name or not self.lon_name:
            return {"success": False, "message": "文件缺少经纬度坐标"}

        var = self.dataset[variable_name]
        sel_var = select_region(var, self.lat_name, self.lon_name, lat_min, lat_max, lon_min, lon_max)
        if time_index is not None and self.time_name and self.time_name in sel_var.dims:
            sel_var = sel_var.isel({self.time_name: time_index})

        value = self._compute_stat(sel_var, stat)
        if value is None:
            return {"success": False, "message": f"不支持的统计方法: {stat}"}

        return {
            "success": True,
            "query": {
                "variable": variable_name,
                "region": {"lon": [lon_min, lon_max], "lat": [lat_min, lat_max]},
                "stat": stat,
                "time_index": time_index,
            },
            "result": {"value": value, "units": var.attrs.get("units", "未知")},
            "metadata": {"file": self.file_path, "n_samples": int(sel_var.size)},
        }

    def _compute_stat(self, data, stat: str):
        stat_map = {
            "mean": lambda d: float(d.mean().values),
            "max": lambda d: float(d.max().values),
            "min": lambda d: float(d.min().values),
            "std": lambda d: float(d.std().values),
            "var": lambda d: float(d.var().values),
            "p90": lambda d: float(np.nanpercentile(d.values, 90)),
            "p95": lambda d: float(np.nanpercentile(d.values, 95)),
        }
        fn = stat_map.get(stat)
        if fn is None:
            return None
        return fn(data)

    def find_extreme_location(
        self, variable_name: str, extreme: str = "max",
        time_index: Optional[int] = None,
        lon_min: Optional[float] = None, lon_max: Optional[float] = None,
        lat_min: Optional[float] = None, lat_max: Optional[float] = None,
    ) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        if variable_name not in self.dataset.data_vars:
            return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

        var = self.dataset[variable_name]
        if all(v is not None for v in [lon_min, lon_max, lat_min, lat_max]):
            var = select_region(var, self.lat_name, self.lon_name, lat_min, lat_max, lon_min, lon_max)
        if time_index is not None and self.time_name and self.time_name in var.dims:
            var = var.isel({self.time_name: time_index})

        if extreme == "min":
            extreme_val = float(var.min().values)
            loc = var.where(var == extreme_val, drop=True).squeeze()
        else:
            extreme_val = float(var.max().values)
            loc = var.where(var == extreme_val, drop=True).squeeze()

        lon = float(loc[self.lon_name].values) if self.lon_name and self.lon_name in loc.dims else None
        lat = float(loc[self.lat_name].values) if self.lat_name and self.lat_name in loc.dims else None

        return {
            "success": True,
            "query": {"variable": variable_name, "extreme": extreme},
            "result": {
                "value": extreme_val,
                "location": {"longitude": lon, "latitude": lat},
                "units": self.dataset[variable_name].attrs.get("units", "未知"),
            },
            "metadata": {"file": self.file_path},
        }

    def find_max_value_location(self, variable_name: str, **kwargs):
        return self.find_extreme_location(variable_name, extreme="max", **kwargs)

    def extract_point_series(
        self, variable_name: str, longitude: float, latitude: float,
        start_time_idx: Optional[int] = None, end_time_idx: Optional[int] = None,
    ) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        if variable_name not in self.dataset.data_vars:
            return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

        lon = normalize_longitude(longitude, self.dataset[self.lon_name].values)
        lat_idx = nearest_index(self.dataset[self.lat_name].values, latitude)
        lon_idx = nearest_index(self.dataset[self.lon_name].values, lon)
        var = self.dataset[variable_name]

        if self.time_name and self.time_name in var.dims:
            series = var.isel({self.lat_name: lat_idx, self.lon_name: lon_idx})
            if start_time_idx is not None and end_time_idx is not None:
                series = series.isel({self.time_name: slice(start_time_idx, end_time_idx + 1)})
            times = [str(t) for t in series[self.time_name].values.tolist()] if self.time_name in series.coords else None
            values = series.values.tolist()
        else:
            values = var.isel({self.lat_name: lat_idx, self.lon_name: lon_idx}).values.tolist()
            times = None

        return {
            "success": True,
            "data": {
                "variable": variable_name,
                "longitude": get_coord_value(self.dataset, self.lon_name, lon_idx),
                "latitude": get_coord_value(self.dataset, self.lat_name, lat_idx),
                "times": times,
                "values": values,
                "units": var.attrs.get("units", "未知"),
            },
            "metadata": {"file": self.file_path},
        }

    def query_by_datetime(self, datetime_str: str) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        idx, actual = parse_time_index(self.dataset, self.time_name, datetime_str)
        if idx is None:
            return {"success": False, "message": actual}
        return {
            "success": True,
            "query": {"datetime": datetime_str},
            "result": {"time_index": idx, "actual_time": actual},
            "metadata": {"file": self.file_path},
        }

    def close_file(self) -> Dict[str, Any]:
        if self.dataset is not None:
            self.dataset.close()
            self.dataset = None
            self.file_path = None
            return {"success": True, "message": "文件已关闭"}
        return {"success": False, "message": "没有打开的文件"}


nc_reader = NCFileReader()
