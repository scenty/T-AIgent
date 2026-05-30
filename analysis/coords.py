# -*- coding: utf-8 -*-
"""NetCDF 坐标与时间维度自适应工具"""

import numpy as np
import xarray as xr

LAT_NAMES = ("latitude", "lat", "LAT", "Latitude", "y")
LON_NAMES = ("longitude", "lon", "LON", "Longitude", "x")
TIME_NAMES = ("time", "Time", "T", "t")


def find_coord_name(ds, candidates):
    for name in candidates:
        if name in ds.coords or name in ds.dims:
            return name
        if name in ds.data_vars and ds[name].ndim == 1:
            return name
    for name in ds.dims:
        lower = name.lower()
        if any(c.lower() in lower for c in candidates):
            return name
    return None


def get_lat_lon_time_names(ds):
    lat = find_coord_name(ds, LAT_NAMES)
    lon = find_coord_name(ds, LON_NAMES)
    time = find_coord_name(ds, TIME_NAMES)
    return lat, lon, time


def normalize_longitude(lon, lon_array):
    arr = np.asarray(lon_array)
    if arr.size == 0:
        return lon
    if arr.min() >= 0 and arr.max() > 180 and lon < 0:
        return lon + 360
    if arr.min() < 0 and lon > 180:
        return lon - 360
    return lon


def nearest_index(coord_values, target):
    arr = np.asarray(coord_values)
    return int(np.abs(arr - target).argmin())


def region_slice(coord_values, vmin, vmax):
    arr = np.asarray(coord_values)
    if arr.size == 0:
        return slice(None)
    if arr[0] <= arr[-1]:
        lo, hi = min(vmin, vmax), max(vmin, vmax)
    else:
        lo, hi = max(vmin, vmax), min(vmin, vmax)
    return slice(lo, hi)


def select_region(var, lat_name, lon_name, lat_min, lat_max, lon_min, lon_max):
    lat_slice = region_slice(var[lat_name].values, lat_min, lat_max)
    lon_slice = region_slice(var[lon_name].values, lon_min, lon_max)
    return var.sel({lat_name: lat_slice, lon_name: lon_slice})


def get_coord_value(ds, name, index):
    return float(ds[name].isel({name: index}).values)


def parse_time_index(ds, time_name, datetime_str):
    if time_name is None:
        return None, "文件无时间维度"
    times = ds[time_name]
    if not np.issubdtype(times.dtype, np.datetime64):
        decoded = xr.decode_cf(ds[[time_name]])
        times = decoded[time_name]
    target = np.datetime64(datetime_str)
    idx = int(np.abs(times.values - target).argmin())
    actual = str(times.isel({time_name: idx}).values)
    return idx, actual
