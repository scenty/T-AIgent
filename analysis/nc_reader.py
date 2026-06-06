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


def _scalar_coord_value(ds, name):
    if not name or name not in ds:
        return None
    val = ds[name].values
    return float(val) if val.ndim == 0 else float(val.flat[0])


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

    def _dataset_summary(self) -> Dict[str, Any]:
        summary = {
            "dimensions": dict(self.dataset.sizes),
            "variables": list(self.dataset.data_vars.keys()),
            "coordinates": list(self.dataset.coords.keys()),
            "global_attributes": {k: str(v) for k, v in self.dataset.attrs.items()},
            "coord_names": {"lat": self.lat_name, "lon": self.lon_name, "time": self.time_name},
            "variable_dims": {name: list(self.dataset[name].dims) for name in self.dataset.data_vars},
        }
        return summary

    def _file_coord_value(self, name: Optional[str]) -> Optional[float]:
        return _scalar_coord_value(self.dataset, name)

    def select_series_at_point(self, var, latitude: float, longitude: float):
        dims = set(var.dims)
        lat_name, lon_name = self.lat_name, self.lon_name

        if lat_name in dims and lon_name in dims:
            nlat = var.sizes.get(lat_name, self.dataset.sizes.get(lat_name, 0))
            nlon = var.sizes.get(lon_name, self.dataset.sizes.get(lon_name, 0))
            if nlat <= 1 and nlon <= 1:
                series = var.isel({lat_name: 0, lon_name: 0})
                out_lat = self._file_coord_value(lat_name) or latitude
                out_lon = self._file_coord_value(lon_name) or longitude
                return series, out_lat, out_lon, "grid_1x1"
            lon = normalize_longitude(longitude, self.dataset[lon_name].values)
            lat_idx = nearest_index(self.dataset[lat_name].values, latitude)
            lon_idx = nearest_index(self.dataset[lon_name].values, lon)
            series = var.isel({lat_name: lat_idx, lon_name: lon_idx})
            out_lat = get_coord_value(self.dataset, lat_name, lat_idx)
            out_lon = get_coord_value(self.dataset, lon_name, lon_idx)
            return series, out_lat, out_lon, "grid"

        if self.time_name and self.time_name in dims:
            out_lat = self._file_coord_value(lat_name) if lat_name else latitude
            out_lon = self._file_coord_value(lon_name) if lon_name else longitude
            return var, out_lat, out_lon, "time_series"

        return None, None, None, "unsupported"

    def open_file(self, file_path: str) -> Dict[str, Any]:
        if self.dataset is not None:
            self.dataset.close()
            self.dataset = None
        self.dataset = xr.open_dataset(file_path)
        self.file_path = file_path
        self._refresh_coords()
        from meta.data_config import infer_layout_mode, match_root_for_path

        root = match_root_for_path(file_path)
        root_layout = (root or {}).get("layout")
        variable_dims = {name: list(self.dataset[name].dims) for name in self.dataset.data_vars}
        layout_mode = infer_layout_mode(
            variable_dims, self.lat_name, self.lon_name,
            dict(self.dataset.sizes), root_layout,
        )
        return {
            "success": True,
            "message": f"成功打开文件: {file_path}",
            "coords": {"lat": self.lat_name, "lon": self.lon_name, "time": self.time_name},
            "layout_mode": layout_mode,
            "file_info": self._dataset_summary(),
        }

    def get_file_info(self) -> Dict[str, Any]:
        if self.dataset is None:
            return {"success": False, "message": "请先打开文件"}
        return {"success": True, "file_info": self._dataset_summary()}

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
        if variable_name not in self.dataset.data_vars:
            return {"success": False, "message": f"变量 '{variable_name}' 不存在"}

        var = self.dataset[variable_name]
        series, out_lat, out_lon, layout_mode = self.select_series_at_point(var, latitude, longitude)
        if series is None:
            return {
                "success": False,
                "message": f"变量 '{variable_name}' 维度 {list(var.dims)} 不支持按点提取",
            }

        if time_index is not None and self.time_name and self.time_name in series.dims:
            data = series.isel({self.time_name: time_index})
        else:
            data = series

        result = {
            "variable": variable_name,
            "latitude": out_lat,
            "longitude": out_lon,
            "value": float(data.values),
            "units": var.attrs.get("units", "未知"),
        }
        return {
            "success": True,
            "data": result,
            "metadata": {"file": self.file_path, "layout_mode": layout_mode},
        }

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

        var = self.dataset[variable_name]
        series, out_lat, out_lon, layout_mode = self.select_series_at_point(var, latitude, longitude)
        if series is None:
            return {
                "success": False,
                "message": f"变量 '{variable_name}' 维度 {list(var.dims)} 不支持时间序列提取",
            }

        if self.time_name and self.time_name in series.dims:
            if start_time_idx is not None and end_time_idx is not None:
                series = series.isel({self.time_name: slice(start_time_idx, end_time_idx + 1)})
            times = [str(t) for t in series[self.time_name].values.tolist()] if self.time_name in series.coords else None
            values = series.values.tolist()
        else:
            values = [float(series.values)]
            times = None

        return {
            "success": True,
            "data": {
                "variable": variable_name,
                "longitude": out_lon,
                "latitude": out_lat,
                "times": times,
                "values": values,
                "units": var.attrs.get("units", "未知"),
            },
            "metadata": {"file": self.file_path, "layout_mode": layout_mode},
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
