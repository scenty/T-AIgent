# Meta 分析记忆

- 更新时间: 2026-05-31T11:51:42
- 文件总数: 3
- 索引路径: D:\03-WorkingSync\T-AIgent\cache\nc_catalog.json

## 要素分布
- `surge`: 1
- `wave`: 1
- `wind`: 1

## 产品分布
- `small_grid`: 3

## 结构化缓存（供程序读取）
```json
{
  "file_count": 3,
  "catalog_path": "D:\\03-WorkingSync\\T-AIgent\\cache\\nc_catalog.json",
  "summary": {
    "by_element": {
      "surge": 1,
      "wave": 1,
      "wind": 1
    },
    "by_product": {
      "small_grid": 3
    }
  }
}
```

## 工具调用记录

### 2026-05-31T11:52:20 | build_nc_catalog
- 参数:
```json
{
  "force": true
}
```
- 响应:
```json
{
  "success": true,
  "file_count": 3,
  "error_count": 0,
  "errors": [],
  "catalog_path": "D:\\03-WorkingSync\\T-AIgent\\cache\\nc_catalog.json",
  "summary": {
    "by_element": {
      "surge": 1,
      "wave": 1,
      "wind": 1
    },
    "by_product": {
      "small_grid": 3
    }
  }
}
```

### 2026-05-31T11:52:27 | analyze_data_availability
- 参数:
```json
{
  "element": "wave",
  "time_start": "2025-05-31",
  "time_end": "2025-05-31"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "element": "wave",
    "region": {
      "lon_min": null,
      "lon_max": null,
      "lat_min": null,
      "lat_max": null
    },
    "time": {
      "start": "2025-05-31",
      "end": "2025-05-31"
    },
    "product_type": null
  },
  "counts": {
    "available": 1,
    "partial": 0,
    "unavailable": 2
  },
  "available_files": [
    {
      "path": "sample_data\\wave_forecast_small_grid.nc",
      "elements": [
        "wave"
      ],
      "product_type": "small_grid",
      "product_label": "小网格数值预报",
      "time_range": {
        "start": "0",
        "end": "71",
        "count": 72
      },
      "bbox": {
        "lat_min": 20.0,
        "lat_max": 24.0,
        "lon_min": 112.0,
        "lon_max": 116.0
      },
      "status": "available",
      "reason": "满足查询条件"
    }
  ],
  "partial_files": [],
  "unavailable_files": [
    {
      "path": "sample_data\\surge_forecast_large_grid.nc",
      "elements": [
        "surge"
      ],
      "product_type": "small_grid",
      "product_label": "小网格数值预报",
      "time_range": {
        "start": "0",
        "end": "71",
        "count": 72
      },
      "bbox": {
        "lat_min": 20.0,
        "lat_max": 24.0,
        "lon_min": 112.0,
        "lon_max": 116.0
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "sample_data\\wind_forecast.nc",
      "elements": [
        "wind"
      ],
      "product_type": "small_grid",
      "product_label": "小网格数值预报",
      "time_range": {
        "start": "0",
        "end": "71",
        "count": 72
      },
      "bbox": {
        "lat_min": 20.0,
        "lat_max": 24.0,
        "lon_min": 112.0,
        "lon_max": 116.0
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    }
  ],
  "recommended": [
    "sample_data\\wave_forecast_small_grid.nc"
  ],
  "report": "# NC 数据可用性分析报告\n\n## 1. 扫描概况\n- 索引文件总数: 3\n- 完全可用: 1 | 部分可用: 0 | 不可用: 2\n\n## 2. 查询条件\n- 目标要素: 海浪\n- 目标时间: 2025-05-31 ~ 2025-05-31\n\n## 3. 可用文件清单\n- [available] sample_data\\wave_forecast_small_grid.nc (小网格数值预报)\n\n## 5. 结论与推荐\n推荐使用: sample_data\\wave_forecast_small_grid.nc"
}
```

### 2026-05-31T11:52:32 | get_nc_file_detail
- 参数:
```json
{
  "file_path": "sample_data\\wave_forecast_small_grid.nc"
}
```
- 响应:
```json
{
  "success": true,
  "detail": {
    "path": "sample_data\\wave_forecast_small_grid.nc",
    "dimensions": {
      "time": 72,
      "latitude": 20,
      "longitude": 25
    },
    "variables": [
      "swh"
    ],
    "coordinates": [
      "time",
      "latitude",
      "longitude"
    ],
    "global_attributes": {
      "title": "示例海浪预报",
      "source": "test"
    },
    "lat_name": "latitude",
    "lon_name": "longitude",
    "time_name": "time",
    "bbox": {
      "lat_min": 20.0,
      "lat_max": 24.0,
      "lon_min": 112.0,
      "lon_max": 116.0
    },
    "time_range": {
      "start": "0",
      "end": "71",
      "count": 72
    },
    "readable": true,
    "elements": [
      "wave"
    ],
    "product_type": "small_grid",
    "disaster_types": [
      "wave"
    ],
    "path_tags": [
      "wave"
    ],
    "elements_detail": {
      "wave": "swh"
    },
    "size_bytes": 297611
  }
}
```

### 2026-05-31T11:52:35 | open_nc_file
- 参数:
```json
{
  "file_path": "sample_data\\wave_forecast_small_grid.nc"
}
```
- 响应:
```json
{
  "success": true,
  "message": "成功打开文件: sample_data\\wave_forecast_small_grid.nc",
  "coords": {
    "lat": "latitude",
    "lon": "longitude",
    "time": "time"
  },
  "file_info": "<xarray.Dataset> Size: 289kB\nDimensions:    (time: 72, latitude: 20, longitude: 25)\nCoordinates:\n  * time       (time) datetime64[ns] 576B 2024-08-15 ... 2024-08-17T23:00:00\n  * latitude   (latitude) float64 160B 20.0 20.21 20.42 ... 23.58 23.79 24.0\n  * longitude  (longitude) float64 200B 112.0 112.2 112.3 ... 115.7 115.8 116.0\nData variables:\n    swh        (time, latitude, longitude) float64 288kB ...\nAttributes:\n    title:    示例海浪预报\n    source:   test"
}
```

### 2026-05-31T11:52:40 | query_by_datetime
- 参数:
```json
{
  "datetime_str": "2025-05-31T00:00:00"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "datetime": "2025-05-31T00:00:00"
  },
  "result": {
    "time_index": 71,
    "actual_time": "2024-08-17T23:00:00.000000000"
  },
  "metadata": {
    "file": "sample_data\\wave_forecast_small_grid.nc"
  }
}
```

## 文件状态
- 更新时间: 2026-05-31T12:08:35
- 文件总数: 3
- 索引路径: D:\03-WorkingSync\T-AIgent\cache\nc_catalog.json

### 要素分布
- `surge`: 1
- `wave`: 1
- `wind`: 1

### 产品分布
- `small_grid`: 3

### 结构化缓存（供程序读取）
```json
{
  "file_count": 3,
  "catalog_path": "D:\\03-WorkingSync\\T-AIgent\\cache\\nc_catalog.json",
  "summary": {
    "by_element": {
      "surge": 1,
      "wave": 1,
      "wind": 1
    },
    "by_product": {
      "small_grid": 3
    }
  }
}
```

### 2026-05-31T12:08:47 | scan_nc_directories
- 参数:
```json
{}
```
- 响应:
```json
{
  "success": true,
  "scanned_roots": [
    "\\data\\ocean",
    "sample_data"
  ],
  "missing_roots": [
    "\\data\\ocean"
  ],
  "root_stats": [
    {
      "root": "\\data\\ocean",
      "exists": false,
      "file_count": 0,
      "size_bytes": 0
    },
    {
      "root": "sample_data",
      "exists": true,
      "file_count": 3,
      "size_bytes": 2199606
    }
  ],
  "file_count": 3,
  "files": [
    {
      "path": "sample_data\\surge_forecast_large_grid.nc",
      "root": "sample_data",
      "size_bytes": 1737443
    },
    {
      "path": "sample_data\\wave_forecast_small_grid.nc",
      "root": "sample_data",
      "size_bytes": 297611
    },
    {
      "path": "sample_data\\wind_forecast.nc",
      "root": "sample_data",
      "size_bytes": 164552
    }
  ]
}
```
