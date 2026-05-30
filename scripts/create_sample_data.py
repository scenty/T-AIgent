# -*- coding: utf-8 -*-
"""生成示例 NC 数据用于测试"""

from pathlib import Path
import numpy as np
import xarray as xr

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def create_wave_file(path: Path):
    times = np.arange("2024-08-15T00:00:00", "2024-08-18T00:00:00", dtype="datetime64[h]")
    lats = np.linspace(20, 24, 20)
    lons = np.linspace(112, 116, 25)
    swh = np.random.uniform(1.0, 4.5, (len(times), len(lats), len(lons)))

    ds = xr.Dataset(
        {"swh": (["time", "latitude", "longitude"], swh)},
        coords={"time": times, "latitude": lats, "longitude": lons},
        attrs={"title": "示例海浪预报", "source": "test"},
    )
    ds["swh"].attrs = {"units": "m", "long_name": "significant wave height"}
    ds.to_netcdf(path)


def create_surge_file(path: Path):
    times = np.arange("2024-08-15T00:00:00", "2024-08-18T00:00:00", dtype="datetime64[h]")
    lats = np.linspace(20, 24, 50)
    lons = np.linspace(112, 116, 60)
    surge = np.random.uniform(0.1, 1.0, (len(times), len(lats), len(lons)))

    ds = xr.Dataset(
        {"surge": (["time", "lat", "lon"], surge)},
        coords={"time": times, "lat": lats, "lon": lons},
        attrs={"title": "示例风暴潮预报"},
    )
    ds["surge"].attrs = {"units": "m"}
    ds.to_netcdf(path)


def create_wind_file(path: Path):
    times = np.arange("2024-08-15T00:00:00", "2024-08-18T00:00:00", dtype="datetime64[h]")
    lats = np.linspace(20, 24, 15)
    lons = np.linspace(112, 116, 18)
    speed = np.random.uniform(5, 20, (len(times), len(lats), len(lons)))

    ds = xr.Dataset(
        {"wind_speed": (["time", "latitude", "longitude"], speed)},
        coords={"time": times, "latitude": lats, "longitude": lons},
    )
    ds["wind_speed"].attrs = {"units": "m/s"}
    ds.to_netcdf(path)


def main():
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    create_wave_file(SAMPLE_DIR / "wave_forecast_small_grid.nc")
    create_surge_file(SAMPLE_DIR / "surge_forecast_large_grid.nc")
    create_wind_file(SAMPLE_DIR / "wind_forecast.nc")
    print(f"示例数据已生成到 {SAMPLE_DIR}")


if __name__ == "__main__":
    main()
