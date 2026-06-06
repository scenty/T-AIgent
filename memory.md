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
- 更新时间: 2026-06-06T20:28:15
- 文件总数: 223
- 索引路径: C:\Users\scent\WorkingSync\T-AIgent\cache\nc_catalog.json

### 要素分布
- `wave`: 170
- `surge`: 50
- `wind`: 3

### 产品分布
- `field_ai`: 20
- `point_ai`: 200
- `large_grid`: 3

### 结构化缓存（供程序读取）
```json
{
  "file_count": 223,
  "catalog_path": "C:\\Users\\scent\\WorkingSync\\T-AIgent\\cache\\nc_catalog.json",
  "summary": {
    "by_element": {
      "wave": 170,
      "surge": 50,
      "wind": 3
    },
    "by_product": {
      "field_ai": 20,
      "point_ai": 200,
      "large_grid": 3
    }
  },
  "reused_count": 223,
  "new_count": 0
}
```

### 2026-06-06T20:28:33 | analyze_data_availability
- 参数:
```json
{
  "element": "wave",
  "time_start": "2026-05-30T00:00:00",
  "time_end": "2026-05-31T00:00:00"
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
      "start": "2026-05-30T00:00:00",
      "end": "2026-05-31T00:00:00"
    },
    "product_type": null
  },
  "counts": {
    "available": 0,
    "partial": 170,
    "unavailable": 53
  },
  "available_files": [],
  "partial_files": [
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260521_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231312.0",
        "end": "231455.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260522_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231336.0",
        "end": "231479.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260523_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231360.0",
        "end": "231503.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260524_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231384.0",
        "end": "231527.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260525_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231408.0",
        "end": "231551.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260526_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231432.0",
        "end": "231575.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260527_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231456.0",
        "end": "231599.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260528_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231480.0",
        "end": "231623.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260529_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231504.0",
        "end": "231647.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc",
      "elements": [
        "wave"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "231528.0",
        "end": "231671.0",
        "count": 144
      },
      "bbox": {
        "lat_min": 15.0,
        "lat_max": 30.0,
        "lon_min": 110.0,
        "lon_max": 135.0
      },
      "status": "partial",
      "reason": "时间范围晚于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46694A_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46699A_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46708A_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46714D_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46744A_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46757B_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_46761F_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C5W09_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6AH2_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6B01_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6F01_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6S62_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6S94_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6V27_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6W08_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260521\\EC_point_wave_C6W10_20260521.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46694A_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46699A_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46708A_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46714D_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46744A_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46757B_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_46761F_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C5W09_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6AH2_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6B01_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6F01_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6S62_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6S94_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6V27_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6W08_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260522\\EC_point_wave_C6W10_20260522.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46694A_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46699A_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46708A_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46714D_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46744A_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46757B_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_46761F_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C5W09_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6AH2_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6B01_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6F01_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6S62_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6S94_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6V27_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6W08_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260523\\EC_point_wave_C6W10_20260523.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46694A_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46699A_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46708A_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46714D_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46744A_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46757B_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_46761F_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C5W09_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6AH2_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6B01_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6F01_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6S62_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6S94_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6V27_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6W08_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260524\\EC_point_wave_C6W10_20260524.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46694A_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46699A_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46708A_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46714D_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46744A_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46757B_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_46761F_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C5W09_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6AH2_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6B01_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6F01_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6S62_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6S94_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6V27_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6W08_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260525\\EC_point_wave_C6W10_20260525.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46694A_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46699A_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46708A_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46714D_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46744A_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46757B_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_46761F_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C5W09_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6AH2_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6B01_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6F01_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6S62_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6S94_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6V27_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6W08_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260526\\EC_point_wave_C6W10_20260526.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46694A_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46699A_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46708A_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46714D_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46744A_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46757B_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_46761F_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C5W09_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6AH2_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6B01_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6F01_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6S62_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6S94_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6V27_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6W08_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260527\\EC_point_wave_C6W10_20260527.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46694A_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46699A_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46708A_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46714D_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46744A_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46757B_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_46761F_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C5W09_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6AH2_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6B01_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6F01_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6S62_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6S94_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6V27_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6W08_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260528\\EC_point_wave_C6W10_20260528.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46694A_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46699A_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46708A_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46714D_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46744A_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46757B_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_46761F_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C5W09_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6AH2_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6B01_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6F01_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6S62_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6S94_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6V27_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6W08_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260529\\EC_point_wave_C6W10_20260529.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46694A_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.096389770507812,
        "lat_max": 25.096389770507812,
        "lon_min": 121.92250061035156,
        "lon_max": 121.92250061035156
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46699A_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.030834197998047,
        "lat_max": 24.030834197998047,
        "lon_min": 121.63249969482422,
        "lon_max": 121.63249969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46708A_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.84861183166504,
        "lat_max": 24.84861183166504,
        "lon_min": 121.92610931396484,
        "lon_max": 121.92610931396484
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46714D_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.316667556762695,
        "lat_max": 22.316667556762695,
        "lon_min": 120.375,
        "lon_max": 120.375
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46744A_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.41722297668457,
        "lat_max": 22.41722297668457,
        "lon_min": 120.4383316040039,
        "lon_max": 120.4383316040039
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.76277732849121,
        "lat_max": 24.76277732849121,
        "lon_min": 120.84361267089844,
        "lon_max": 120.84361267089844
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46761F_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.13249969482422,
        "lat_max": 23.13249969482422,
        "lon_min": 121.42028045654297,
        "lon_max": 121.42028045654297
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C5W09_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.256389617919922,
        "lat_max": 23.256389617919922,
        "lon_min": 119.68389129638672,
        "lon_max": 119.68389129638672
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6AH2_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.302778244018555,
        "lat_max": 25.302778244018555,
        "lon_min": 121.5280532836914,
        "lon_max": 121.5280532836914
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6B01_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 25.620277404785156,
        "lat_max": 25.620277404785156,
        "lon_min": 122.06610870361328,
        "lon_max": 122.06610870361328
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6F01_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 24.237499237060547,
        "lat_max": 24.237499237060547,
        "lon_min": 120.40888977050781,
        "lon_max": 120.40888977050781
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6S62_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.766387939453125,
        "lat_max": 21.766387939453125,
        "lon_min": 124.07416534423828,
        "lon_max": 124.07416534423828
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6S94_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 22.06861114501953,
        "lat_max": 22.06861114501953,
        "lon_min": 121.57861328125,
        "lon_max": 121.57861328125
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6V27_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 21.091110229492188,
        "lat_max": 21.091110229492188,
        "lon_min": 118.81999969482422,
        "lon_max": 118.81999969482422
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6W08_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 26.356111526489258,
        "lat_max": 26.356111526489258,
        "lon_min": 120.51083374023438,
        "lon_max": 120.51083374023438
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    },
    {
      "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_C6W10_20260530.nc",
      "elements": [
        "wave"
      ],
      "product_type": "point_ai",
      "product_label": "单点智能预报",
      "time_range": {
        "start": "0.0",
        "end": "167.0",
        "count": 168
      },
      "bbox": {
        "lat_min": 23.190834045410156,
        "lat_max": 23.190834045410156,
        "lon_min": 119.66471862792969,
        "lon_max": 119.66471862792969
      },
      "status": "partial",
      "reason": "时间范围早于目标"
    }
  ],
  "unavailable_files": [
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260521.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260522.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260523.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260524.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260525.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260526.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260527.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260528.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260529.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    },
    {
      "path": "data\\dailyforecast\\storm_surge_for_spatiotemporal\\surge_predicted_20260530.nc",
      "elements": [
        "surge"
      ],
      "product_type": "field_ai",
      "product_label": "时空场智能预报",
      "time_range": {
        "start": "0.0",
        "end": "360.0",
        "count": 85
      },
      "bbox": {
        "lat_min": 23.82626724243164,
        "lat_max": 25.17373275756836,
        "lon_min": 116.70337677001953,
        "lon_max": 120.29662322998047
      },
      "status": "unavailable",
      "reason": "不含要素 wave"
    }
  ],
  "recommended": [],
  "report": "# NC 数据可用性分析报告\n\n## 1. 扫描概况\n- 索引文件总数: 223\n- 完全可用: 0 | 部分可用: 170 | 不可用: 53\n\n## 2. 查询条件\n- 目标要素: 海浪\n- 目标时间: 2026-05-30T00:00:00 ~ 2026-05-31T00:00:00\n\n## 3. 可用文件清单\n\n## 4. 部分可用文件\n- data\\dailyforecast\\AutoWave\\res_EC\\20260521_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260522_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260523_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260524_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260525_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260526_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260527_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260528_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260529_wave_forecast_1h.nc: 时间范围晚于目标\n- data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc: 时间范围晚于目标\n\n## 5. 结论与推荐\n无完全匹配文件，可考虑部分可用文件并注意时空范围限制。"
}
```

### 2026-06-06T20:28:49 | get_nc_file_detail
- 参数:
```json
{
  "file_path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc"
}
```
- 响应:
```json
{
  "success": true,
  "detail": {
    "path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "dimensions": {
      "time": 168,
      "lat": 1,
      "lon": 1
    },
    "variables": [
      "station_name",
      "swh",
      "mwp",
      "mwd"
    ],
    "coordinates": [
      "time",
      "lat",
      "lon"
    ],
    "variable_dims": {
      "station_name": [],
      "swh": [
        "time"
      ],
      "mwp": [
        "time"
      ],
      "mwd": [
        "time"
      ]
    },
    "global_attributes": {},
    "lat_name": "lat",
    "lon_name": "lon",
    "time_name": "time",
    "bbox": {
      "lat_min": 24.76277732849121,
      "lat_max": 24.76277732849121,
      "lon_min": 120.84361267089844,
      "lon_max": 120.84361267089844
    },
    "time_range": {
      "start": "0.0",
      "end": "167.0",
      "count": 168
    },
    "readable": true,
    "elements": [
      "wave"
    ],
    "product_type": "point_ai",
    "disaster_types": [
      "wave"
    ],
    "path_tags": [
      "wave",
      "point_ai",
      "field_ai"
    ],
    "layout_mode": "time_series",
    "station_code": "46757B",
    "layout_source": "./data/dailyforecast/wave_for_single_point/outputs/nc_files",
    "elements_detail": {
      "wave": "swh"
    },
    "root_variables": {
      "wave": [
        "swh",
        "mwp",
        "mwd"
      ]
    },
    "size_bytes": 11348,
    "mtime": 1780221271.0
  }
}
```

### 2026-06-06T20:28:49 | get_nc_file_detail
- 参数:
```json
{
  "file_path": "data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc"
}
```
- 响应:
```json
{
  "success": true,
  "detail": {
    "path": "data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc",
    "dimensions": {
      "time": 144,
      "latitude": 64,
      "longitude": 72
    },
    "variables": [
      "hs_torch",
      "mwp_torch",
      "mwd_torch",
      "uwind_torch",
      "vwind_torch",
      "mask"
    ],
    "coordinates": [
      "longitude",
      "latitude",
      "time"
    ],
    "variable_dims": {
      "hs_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mwp_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mwd_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "uwind_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "vwind_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mask": [
        "latitude",
        "longitude"
      ]
    },
    "global_attributes": {
      "title": "CuboidWaveModel wave forecast",
      "institution": "Generated by CuboidWaveModel script",
      "source": "CuboidWaveModel output",
      "history": "Created 2026-05-30 11:52:21 UTC",
      "Conventions": "CF-1.6",
      "MODEL_INPUT_WIND_FILE": "D://Project//EC//20260530000000_ECMWF_wind_msl.nc"
    },
    "lat_name": "latitude",
    "lon_name": "longitude",
    "time_name": "time",
    "bbox": {
      "lat_min": 15.0,
      "lat_max": 30.0,
      "lon_min": 110.0,
      "lon_max": 135.0
    },
    "time_range": {
      "start": "231528.0",
      "end": "231671.0",
      "count": 144
    },
    "readable": true,
    "elements": [
      "wave"
    ],
    "product_type": "field_ai",
    "disaster_types": [
      "wave"
    ],
    "path_tags": [
      "wave",
      "field_ai"
    ],
    "layout_mode": "grid",
    "station_code": null,
    "layout_source": "./data/dailyforecast/AutoWave/res_EC",
    "elements_detail": {
      "wave": "swh"
    },
    "root_variables": {
      "wave": [
        "hs_torch",
        "mwp_torch",
        "mwd_torch",
        "uwind_torch",
        "vwind_torch"
      ]
    },
    "size_bytes": 13279528,
    "mtime": 1780221202.0
  }
}
```

### 2026-06-06T20:28:58 | open_nc_file
- 参数:
```json
{
  "file_path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc"
}
```
- 响应:
```json
{
  "success": true,
  "message": "成功打开文件: data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
  "coords": {
    "lat": "lat",
    "lon": "lon",
    "time": "time"
  },
  "layout_mode": "time_series",
  "file_info": {
    "dimensions": {
      "time": 168,
      "lat": 1,
      "lon": 1
    },
    "variables": [
      "station_name",
      "swh",
      "mwp",
      "mwd"
    ],
    "coordinates": [
      "time",
      "lat",
      "lon"
    ],
    "global_attributes": {},
    "coord_names": {
      "lat": "lat",
      "lon": "lon",
      "time": "time"
    },
    "variable_dims": {
      "station_name": [],
      "swh": [
        "time"
      ],
      "mwp": [
        "time"
      ],
      "mwd": [
        "time"
      ]
    }
  }
}
```

### 2026-06-06T20:29:03 | query_by_datetime
- 参数:
```json
{
  "datetime_str": "2026-05-30T00:00:00"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "datetime": "2026-05-30T00:00:00"
  },
  "result": {
    "time_index": 0,
    "actual_time": "2026-05-30T00:00:00.000000000"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc"
  }
}
```

### 2026-06-06T20:29:07 | close_nc_file
- 参数:
```json
{}
```
- 响应:
```json
{
  "success": true,
  "message": "文件已关闭"
}
```

### 2026-06-06T20:29:11 | open_nc_file
- 参数:
```json
{
  "file_path": "data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc"
}
```
- 响应:
```json
{
  "success": true,
  "message": "成功打开文件: data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc",
  "coords": {
    "lat": "latitude",
    "lon": "longitude",
    "time": "time"
  },
  "layout_mode": "grid",
  "file_info": {
    "dimensions": {
      "time": 144,
      "latitude": 64,
      "longitude": 72
    },
    "variables": [
      "hs_torch",
      "mwp_torch",
      "mwd_torch",
      "uwind_torch",
      "vwind_torch",
      "mask"
    ],
    "coordinates": [
      "longitude",
      "latitude",
      "time"
    ],
    "global_attributes": {
      "title": "CuboidWaveModel wave forecast",
      "institution": "Generated by CuboidWaveModel script",
      "source": "CuboidWaveModel output",
      "history": "Created 2026-05-30 11:52:21 UTC",
      "Conventions": "CF-1.6",
      "MODEL_INPUT_WIND_FILE": "D://Project//EC//20260530000000_ECMWF_wind_msl.nc"
    },
    "coord_names": {
      "lat": "latitude",
      "lon": "longitude",
      "time": "time"
    },
    "variable_dims": {
      "hs_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mwp_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mwd_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "uwind_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "vwind_torch": [
        "time",
        "latitude",
        "longitude"
      ],
      "mask": [
        "latitude",
        "longitude"
      ]
    }
  }
}
```

### 2026-06-06T20:29:16 | query_by_datetime
- 参数:
```json
{
  "datetime_str": "2026-05-30T00:00:00"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "datetime": "2026-05-30T00:00:00"
  },
  "result": {
    "time_index": 0,
    "actual_time": "2026-05-31T00:00:00.000000000"
  },
  "metadata": {
    "file": "data\\dailyforecast\\AutoWave\\res_EC\\20260530_wave_forecast_1h.nc"
  }
}
```

### 2026-06-06T20:29:29 | close_nc_file
- 参数:
```json
{}
```
- 响应:
```json
{
  "success": true,
  "message": "文件已关闭"
}
```

### 2026-06-06T20:32:37 | lookup_station
- 参数:
```json
{
  "name": "新竹",
  "element": "wave"
}
```
- 响应:
```json
{
  "success": true,
  "count": 1,
  "stations": [
    {
      "station_id": "S46757B",
      "file_code": "46757B",
      "name": "新竹浮标",
      "aliases": [
        "新竹",
        "新竹浮标",
        "新竹站",
        "台湾新竹"
      ],
      "lat": 24.76333333,
      "lon": 120.8441667,
      "type": "buoy",
      "elements": [
        "wave"
      ],
      "data_root": "./data/dailyforecast/wave_for_single_point/outputs/nc_files",
      "filename_pattern": "EC_point_wave_{station_code}_*.nc",
      "nc_filename_example": "EC_point_wave_46757B_*.nc"
    }
  ]
}
```

### 2026-06-06T20:32:47 | open_nc_file
- 参数:
```json
{
  "file_path": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc"
}
```
- 响应:
```json
{
  "success": true,
  "message": "成功打开文件: data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
  "coords": {
    "lat": "lat",
    "lon": "lon",
    "time": "time"
  },
  "layout_mode": "time_series",
  "file_info": {
    "dimensions": {
      "time": 168,
      "lat": 1,
      "lon": 1
    },
    "variables": [
      "station_name",
      "swh",
      "mwp",
      "mwd"
    ],
    "coordinates": [
      "time",
      "lat",
      "lon"
    ],
    "global_attributes": {},
    "coord_names": {
      "lat": "lat",
      "lon": "lon",
      "time": "time"
    },
    "variable_dims": {
      "station_name": [],
      "swh": [
        "time"
      ],
      "mwp": [
        "time"
      ],
      "mwd": [
        "time"
      ]
    }
  }
}
```

### 2026-06-06T20:32:56 | extract_point_series
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "start_time_idx": 0,
  "end_time_idx": 167
}
```
- 响应:
```json
{
  "success": true,
  "data": {
    "variable": "swh",
    "longitude": 120.84361267089844,
    "latitude": 24.76277732849121,
    "times": [
      "1780099200000000000",
      "1780102800000000000",
      "1780106400000000000",
      "1780110000000000000",
      "1780113600000000000",
      "1780117200000000000",
      "1780120800000000000",
      "1780124400000000000",
      "1780128000000000000",
      "1780131600000000000",
      "1780135200000000000",
      "1780138800000000000",
      "1780142400000000000",
      "1780146000000000000",
      "1780149600000000000",
      "1780153200000000000",
      "1780156800000000000",
      "1780160400000000000",
      "1780164000000000000",
      "1780167600000000000",
      "1780171200000000000",
      "1780174800000000000",
      "1780178400000000000",
      "1780182000000000000",
      "1780185600000000000",
      "1780189200000000000",
      "1780192800000000000",
      "1780196400000000000",
      "1780200000000000000",
      "1780203600000000000",
      "1780207200000000000",
      "1780210800000000000",
      "1780214400000000000",
      "1780218000000000000",
      "1780221600000000000",
      "1780225200000000000",
      "1780228800000000000",
      "1780232400000000000",
      "1780236000000000000",
      "1780239600000000000",
      "1780243200000000000",
      "1780246800000000000",
      "1780250400000000000",
      "1780254000000000000",
      "1780257600000000000",
      "1780261200000000000",
      "1780264800000000000",
      "1780268400000000000",
      "1780272000000000000",
      "1780275600000000000",
      "1780279200000000000",
      "1780282800000000000",
      "1780286400000000000",
      "1780290000000000000",
      "1780293600000000000",
      "1780297200000000000",
      "1780300800000000000",
      "1780304400000000000",
      "1780308000000000000",
      "1780311600000000000",
      "1780315200000000000",
      "1780318800000000000",
      "1780322400000000000",
      "1780326000000000000",
      "1780329600000000000",
      "1780333200000000000",
      "1780336800000000000",
      "1780340400000000000",
      "1780344000000000000",
      "1780347600000000000",
      "1780351200000000000",
      "1780354800000000000",
      "1780358400000000000",
      "1780362000000000000",
      "1780365600000000000",
      "1780369200000000000",
      "1780372800000000000",
      "1780376400000000000",
      "1780380000000000000",
      "1780383600000000000",
      "1780387200000000000",
      "1780390800000000000",
      "1780394400000000000",
      "1780398000000000000",
      "1780401600000000000",
      "1780405200000000000",
      "1780408800000000000",
      "1780412400000000000",
      "1780416000000000000",
      "1780419600000000000",
      "1780423200000000000",
      "1780426800000000000",
      "1780430400000000000",
      "1780434000000000000",
      "1780437600000000000",
      "1780441200000000000",
      "1780444800000000000",
      "1780448400000000000",
      "1780452000000000000",
      "1780455600000000000",
      "1780459200000000000",
      "1780462800000000000",
      "1780466400000000000",
      "1780470000000000000",
      "1780473600000000000",
      "1780477200000000000",
      "1780480800000000000",
      "1780484400000000000",
      "1780488000000000000",
      "1780491600000000000",
      "1780495200000000000",
      "1780498800000000000",
      "1780502400000000000",
      "1780506000000000000",
      "1780509600000000000",
      "1780513200000000000",
      "1780516800000000000",
      "1780520400000000000",
      "1780524000000000000",
      "1780527600000000000",
      "1780531200000000000",
      "1780534800000000000",
      "1780538400000000000",
      "1780542000000000000",
      "1780545600000000000",
      "1780549200000000000",
      "1780552800000000000",
      "1780556400000000000",
      "1780560000000000000",
      "1780563600000000000",
      "1780567200000000000",
      "1780570800000000000",
      "1780574400000000000",
      "1780578000000000000",
      "1780581600000000000",
      "1780585200000000000",
      "1780588800000000000",
      "1780592400000000000",
      "1780596000000000000",
      "1780599600000000000",
      "1780603200000000000",
      "1780606800000000000",
      "1780610400000000000",
      "1780614000000000000",
      "1780617600000000000",
      "1780621200000000000",
      "1780624800000000000",
      "1780628400000000000",
      "1780632000000000000",
      "1780635600000000000",
      "1780639200000000000",
      "1780642800000000000",
      "1780646400000000000",
      "1780650000000000000",
      "1780653600000000000",
      "1780657200000000000",
      "1780660800000000000",
      "1780664400000000000",
      "1780668000000000000",
      "1780671600000000000",
      "1780675200000000000",
      "1780678800000000000",
      "1780682400000000000",
      "1780686000000000000",
      "1780689600000000000",
      "1780693200000000000",
      "1780696800000000000",
      "1780700400000000000"
    ],
    "values": [
      0.8563389778137207,
      0.8565377593040466,
      0.8574898838996887,
      0.8826864361763,
      0.9099687933921814,
      0.9296297430992126,
      0.9682437181472778,
      1.0030544996261597,
      1.035017967224121,
      1.059338092803955,
      1.0642465353012085,
      1.049675464630127,
      1.0383214950561523,
      1.0235004425048828,
      1.0024356842041016,
      0.9593623280525208,
      0.9062867760658264,
      0.8486598134040833,
      0.8385048508644104,
      0.8212661147117615,
      0.7968136072158813,
      0.7933773398399353,
      0.7814680933952332,
      0.7686450481414795,
      0.794992983341217,
      0.8226287961006165,
      0.8421747088432312,
      0.8937669396400452,
      0.9405407309532166,
      0.9663461446762085,
      0.9892886877059937,
      0.9982678890228271,
      0.9958305358886719,
      0.9871354699134827,
      0.9627242684364319,
      0.9306501746177673,
      0.9133959412574768,
      0.8880780339241028,
      0.8647777438163757,
      0.8535344004631042,
      0.8417730927467346,
      0.8263238668441772,
      0.8064361214637756,
      0.7875108122825623,
      0.7719307541847229,
      0.7634191513061523,
      0.7516745924949646,
      0.7401378154754639,
      0.7476361393928528,
      0.7583848237991333,
      0.7754250764846802,
      0.8055886626243591,
      0.8358296155929565,
      0.8663710355758667,
      0.8750900626182556,
      0.8847468495368958,
      0.8993625044822693,
      0.8687154650688171,
      0.8455177545547485,
      0.8269252181053162,
      0.7915276885032654,
      0.7585483193397522,
      0.7336018681526184,
      0.7076551914215088,
      0.6872292160987854,
      0.6738386750221252,
      0.6543861031532288,
      0.6497730612754822,
      0.6548230051994324,
      0.6396066546440125,
      0.6394110321998596,
      0.646807849407196,
      0.6430057883262634,
      0.6530855894088745,
      0.6730998754501343,
      0.668748140335083,
      0.6805098652839661,
      0.7011652588844299,
      0.6763941049575806,
      0.6749822497367859,
      0.6886769533157349,
      0.6557866930961609,
      0.6387582421302795,
      0.6325163245201111,
      0.6022784113883972,
      0.5940712690353394,
      0.5994737148284912,
      0.568183958530426,
      0.5571889281272888,
      0.5563840270042419,
      0.5298370122909546,
      0.5219923257827759,
      0.5242070555686951,
      0.5218505859375,
      0.5300452709197998,
      0.5447373986244202,
      0.5636225342750549,
      0.5916181206703186,
      0.6224159598350525,
      0.6514212489128113,
      0.6934097409248352,
      0.744002103805542,
      0.7567261457443237,
      0.7723358869552612,
      0.7909170985221863,
      0.7565903067588806,
      0.7319238781929016,
      0.7123106122016907,
      0.6734447479248047,
      0.6399694085121155,
      0.6123173236846924,
      0.5945531725883484,
      0.5850796103477478,
      0.5842516422271729,
      0.6025676727294922,
      0.6330471634864807,
      0.6758633852005005,
      0.7211375832557678,
      0.7768620252609253,
      0.8418946862220764,
      0.8659319281578064,
      0.8948206305503845,
      0.9237391352653503,
      0.9226988554000854,
      0.9276759028434753,
      0.942226767539978,
      0.9233124852180481,
      0.9126487970352173,
      0.9093181490898132,
      0.8736969232559204,
      0.846188485622406,
      0.8230373859405518,
      0.7718260288238525,
      0.7277788519859314,
      0.696584165096283,
      0.6479186415672302,
      0.6169893145561218,
      0.6066091656684875,
      0.5700404047966003,
      0.5493414998054504,
      0.5438663959503174,
      0.5107840299606323,
      0.4957999885082245,
      0.4940287470817566,
      0.47356167435646057,
      0.47207918763160706,
      0.4849534034729004,
      0.47152987122535706,
      0.4767927825450897,
      0.5024493932723999,
      0.4939821660518646,
      0.5053063035011292,
      0.5357239842414856,
      0.5191658735275269,
      0.5188881754875183,
      0.5393571257591248,
      0.5239809155464172,
      0.5387768745422363,
      0.6057140827178955,
      0.6274594664573669,
      0.6762733459472656,
      0.7481035590171814,
      0.7652298808097839,
      0.7930833697319031,
      0.8267289400100708,
      0.8418895602226257,
      0.8591427206993103,
      0.8670490384101868
    ],
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series"
  }
}
```

### 2026-06-06T20:32:56 | extract_point_stats
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "stat": "max"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "location": {
      "latitude": 24.76277732849121,
      "longitude": 120.84361267089844
    },
    "stat": "max",
    "time_range_idx": [
      null,
      null
    ]
  },
  "result": {
    "value": 1.0642465353012085,
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series",
    "n_samples": 168
  }
}
```

### 2026-06-06T20:32:56 | extract_point_stats
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "stat": "mean"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "location": {
      "latitude": 24.76277732849121,
      "longitude": 120.84361267089844
    },
    "stat": "mean",
    "time_range_idx": [
      null,
      null
    ]
  },
  "result": {
    "value": 0.7430973599354426,
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series",
    "n_samples": 168
  }
}
```

### 2026-06-06T20:32:56 | extract_point_stats
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "stat": "p90"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "location": {
      "latitude": 24.76277732849121,
      "longitude": 120.84361267089844
    },
    "stat": "p90",
    "time_range_idx": [
      null,
      null
    ]
  },
  "result": {
    "value": 0.941046541929245,
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series",
    "n_samples": 168
  }
}
```

### 2026-06-06T20:32:56 | extract_point_stats
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "stat": "p95"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "location": {
      "latitude": 24.76277732849121,
      "longitude": 120.84361267089844
    },
    "stat": "p95",
    "time_range_idx": [
      null,
      null
    ]
  },
  "result": {
    "value": 0.9974148154258728,
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series",
    "n_samples": 168
  }
}
```

### 2026-06-06T20:33:04 | extract_point_stats
- 参数:
```json
{
  "variable_name": "swh",
  "longitude": 120.8436,
  "latitude": 24.7628,
  "stat": "std"
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "location": {
      "latitude": 24.76277732849121,
      "longitude": 120.84361267089844
    },
    "stat": "std",
    "time_range_idx": [
      null,
      null
    ]
  },
  "result": {
    "value": 0.15420926516917816,
    "units": "m"
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc",
    "layout_mode": "time_series",
    "n_samples": 168
  }
}
```

### 2026-06-06T20:33:04 | extract_extreme_events
- 参数:
```json
{
  "variable_name": "swh",
  "threshold": 1.0,
  "longitude": 120.8436,
  "latitude": 24.7628
}
```
- 响应:
```json
{
  "success": true,
  "query": {
    "variable": "swh",
    "threshold": 1.0,
    "location": {
      "latitude": 24.7628,
      "longitude": 120.8436
    }
  },
  "result": {
    "exceed_count": 8,
    "total_count": 168,
    "exceed_ratio": 0.0476,
    "max_value": 1.0642465353012085
  },
  "metadata": {
    "file": "data\\dailyforecast\\wave_for_single_point\\outputs\\nc_files\\20260530\\EC_point_wave_46757B_20260530.nc"
  }
}
```

### 2026-06-06T20:33:04 | get_risk_criteria
- 参数:
```json
{}
```
- 响应:
```json
{
  "success": true,
  "criteria": "# 当前风险判定依据\n\n## wave\n- 单位: m\n- 参考: 有效波高分级（业务常用阈值）\n  - 蓝色: >= 2.5\n  - 黄色: >= 3.5\n  - 橙色: >= 4.5\n  - 红色: >= 6.0\n\n## surge\n- 单位: m\n- 参考: 风暴潮增水分级（相对平均海面）\n  - 蓝色: >= 0.3\n  - 黄色: >= 0.5\n  - 橙色: >= 0.8\n  - 红色: >= 1.2\n\n## wind\n- 单位: m/s\n- 参考: 海上大风平均风速分级\n  - 蓝色: >= 10.8\n  - 黄色: >= 17.2\n  - 橙色: >= 24.5\n  - 红色: >= 32.7\n\n综合策略: max_level"
}
```

### 2026-06-06T20:33:13 | assess_sea_state
- 参数:
```json
{
  "wave_height": 1.0642,
  "location": "台湾新竹浮标 (46757B)",
  "time_label": "2026-05-30 00:00 ~ 2026-06-06 00:00 (168h预报)"
}
```
- 响应:
```json
{
  "success": true,
  "location": "台湾新竹浮标 (46757B)",
  "time": "2026-05-30 00:00 ~ 2026-06-06 00:00 (168h预报)",
  "assessments": [
    {
      "element": "wave",
      "value": 1.0642,
      "unit": "m",
      "level_id": "none",
      "level_name": "无警",
      "reference": "有效波高分级（业务常用阈值）",
      "thresholds": {
        "blue": 2.5,
        "yellow": 3.5,
        "orange": 4.5,
        "red": 6.0
      }
    }
  ],
  "comprehensive": {
    "level_id": "none",
    "level_name": "无警",
    "advice": "海况总体平稳，可正常开展海上作业，请关注最新预报。"
  }
}
```

### 2026-06-06T20:33:21 | close_nc_file
- 参数:
```json
{}
```
- 响应:
```json
{
  "success": true,
  "message": "文件已关闭"
}
```
