# -*- coding: utf-8 -*-
"""统一工具注册与函数调用分发"""

from analysis.nc_reader import nc_reader
from analysis import statistics as stats
from meta.scanner import scan_directories
from meta.catalog import nc_catalog
from meta.classifier import extract_file_meta
from risk.assessor import (
    assess_sea_state,
    assess_comprehensive_risk,
    assess_region_risk,
    get_risk_criteria,
    session_context,
)
#from report.generator import generate_briefing_preview,generate_briefing_docx,list_briefing_templates

# ---------- Meta 工具 ----------
META_FUNCTIONS = [
    {
        "name": "scan_nc_directories",
        "description": "递归扫描本地目录下的 NetCDF 文件，返回文件列表",
        "parameters": {
            "type": "object",
            "properties": {
                "directories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要扫描的目录列表，不提供则使用 config/data_roots.yaml 中的配置",
                }
            },
        },
    },
    {
        "name": "build_nc_catalog",
        "description": "扫描并构建 NC 文件索引缓存，解析头信息、产品分类、时空范围",
        "parameters": {
            "type": "object",
            "properties": {
                "directories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可选，指定扫描目录",
                },
                "force": {"type": "boolean", "description": "是否强制重建索引"},
            },
        },
    },
    {
        "name": "analyze_data_availability",
        "description": "按要素、区域、时间分析 NC 数据可用性，输出文字报告和推荐文件",
        "parameters": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "enum": ["wind", "wave", "surge"], "description": "目标要素"},
                "lon_min": {"type": "number"}, "lon_max": {"type": "number"},
                "lat_min": {"type": "number"}, "lat_max": {"type": "number"},
                "time_start": {"type": "string", "description": "目标起始时间"},
                "time_end": {"type": "string", "description": "目标结束时间"},
                "product_type": {
                    "type": "string",
                    "enum": ["large_grid", "small_grid", "point_ai", "field_ai"],
                },
            },
        },
    },
    {
        "name": "get_nc_file_detail",
        "description": "获取单个 NC 文件的详细 meta 信息（维度、变量、分类、时空范围）",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "NC 文件完整路径"},
            },
            "required": ["file_path"],
        },
    },
]

# ---------- 分析工具 ----------
ANALYSIS_FUNCTIONS = [
    {
        "name": "open_nc_file",
        "description": "打开 NetCDF 文件",
        "parameters": {
            "type": "object",
            "properties": {"file_path": {"type": "string"}},
            "required": ["file_path"],
        },
    },
    {
        "name": "get_nc_file_info",
        "description": "获取当前打开的 NC 文件基本信息",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "read_nc_variable",
        "description": "读取 NC 变量数据（小数据量）",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "time_index": {"type": "integer"},
                "lat_index": {"type": "integer"},
                "lon_index": {"type": "integer"},
            },
            "required": ["variable_name"],
        },
    },
    {
        "name": "extract_location_data",
        "description": "提取指定经纬度位置的数据",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "time_index": {"type": "integer"},
            },
            "required": ["variable_name", "latitude", "longitude"],
        },
    },
    {
        "name": "extract_area_stat",
        "description": "计算矩形区域内变量的统计值（mean/max/min/std/var/p90/p95）",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "lon_min": {"type": "number"}, "lon_max": {"type": "number"},
                "lat_min": {"type": "number"}, "lat_max": {"type": "number"},
                "stat": {"type": "string", "enum": ["mean", "max", "min", "std", "var", "p90", "p95"]},
                "time_index": {"type": "integer"},
            },
            "required": ["variable_name", "lon_min", "lon_max", "lat_min", "lat_max"],
        },
    },
    {
        "name": "extract_area_stats",
        "description": "区域统计（支持 time_avg 时间平均）",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "lon_min": {"type": "number"}, "lon_max": {"type": "number"},
                "lat_min": {"type": "number"}, "lat_max": {"type": "number"},
                "stat": {"type": "string", "enum": ["mean", "max", "min", "std", "var", "p90", "p95"]},
                "time_index": {"type": "integer"},
                "time_avg": {"type": "boolean", "description": "是否对时间维求平均"},
            },
            "required": ["variable_name", "lon_min", "lon_max", "lat_min", "lat_max"],
        },
    },
    {
        "name": "extract_point_stats",
        "description": "单点指定时间范围的统计（mean/max/min/std/var）",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "start_time_idx": {"type": "integer"},
                "end_time_idx": {"type": "integer"},
                "stat": {"type": "string", "enum": ["mean", "max", "min", "std", "var", "p90", "p95"]},
            },
            "required": ["variable_name", "latitude", "longitude"],
        },
    },
    {
        "name": "find_max_value_location",
        "description": "找出变量最大值及坐标",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "time_index": {"type": "integer"},
                "lon_min": {"type": "number"}, "lon_max": {"type": "number"},
                "lat_min": {"type": "number"}, "lat_max": {"type": "number"},
            },
            "required": ["variable_name"],
        },
    },
    {
        "name": "find_min_value_location",
        "description": "找出变量最小值及坐标",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "time_index": {"type": "integer"},
                "lon_min": {"type": "number"}, "lon_max": {"type": "number"},
                "lat_min": {"type": "number"}, "lat_max": {"type": "number"},
            },
            "required": ["variable_name"],
        },
    },
    {
        "name": "extract_point_series",
        "description": "提取固定经纬度点的时间序列",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "longitude": {"type": "number"},
                "latitude": {"type": "number"},
                "start_time_idx": {"type": "integer"},
                "end_time_idx": {"type": "integer"},
            },
            "required": ["variable_name", "longitude", "latitude"],
        },
    },
    {
        "name": "extract_extreme_events",
        "description": "统计单点超过阈值的次数和占比",
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {"type": "string"},
                "threshold": {"type": "number"},
                "longitude": {"type": "number"},
                "latitude": {"type": "number"},
                "start_time_idx": {"type": "integer"},
                "end_time_idx": {"type": "integer"},
            },
            "required": ["variable_name", "threshold", "longitude", "latitude"],
        },
    },
    {
        "name": "compare_sources",
        "description": "对比多个 NC 文件在同一点位的数值差异",
        "parameters": {
            "type": "object",
            "properties": {
                "file_paths": {"type": "array", "items": {"type": "string"}},
                "variable_name": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "time_index": {"type": "integer"},
            },
            "required": ["file_paths", "variable_name", "latitude", "longitude"],
        },
    },
    {
        "name": "query_by_datetime",
        "description": "将 datetime 字符串转换为最近的时间索引",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "如 2024-08-15T12:00:00"},
            },
            "required": ["datetime_str"],
        },
    },
    {
        "name": "close_nc_file",
        "description": "关闭当前 NC 文件",
        "parameters": {"type": "object", "properties": {}},
    },
]

# ---------- 风险工具 ----------
RISK_FUNCTIONS = [
    {
        "name": "assess_sea_state",
        "description": "根据风/浪/潮数值评估各要素及综合预警等级（中国海洋预警标准）",
        "parameters": {
            "type": "object",
            "properties": {
                "wave_height": {"type": "number", "description": "有效波高(m)"},
                "surge_height": {"type": "number", "description": "风暴潮增水(m)"},
                "wind_speed": {"type": "number", "description": "平均风速(m/s)"},
                "location": {"type": "string"},
                "time_label": {"type": "string"},
            },
        },
    },
    {
        "name": "assess_comprehensive_risk",
        "description": "从统计结果列表自动识别要素并评估综合风险",
        "parameters": {
            "type": "object",
            "properties": {
                "stats_results": {"type": "array", "items": {"type": "object"}},
                "location": {"type": "string"},
                "time_label": {"type": "string"},
            },
            "required": ["stats_results"],
        },
    },
    {
        "name": "assess_region_risk",
        "description": "区域代表性数值的风险评估",
        "parameters": {
            "type": "object",
            "properties": {
                "wave_height": {"type": "number"},
                "surge_height": {"type": "number"},
                "wind_speed": {"type": "number"},
                "region_name": {"type": "string"},
                "time_label": {"type": "string"},
            },
        },
    },
    {
        "name": "get_risk_criteria",
        "description": "返回当前风险判定依据和阈值说明",
        "parameters": {"type": "object", "properties": {}},
    },
]

# ---------- 简报工具 ----------
REPORT_FUNCTIONS = [
    {
        "name": "generate_briefing_preview",
        "description": "生成 Markdown 格式简报预览并保存到 output 目录",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "region": {"type": "string"},
                "data_sources": {"type": "array", "items": {"type": "string"}},
                "impact_analysis": {"type": "string"},
            },
        },
    },
    {
        "name": "generate_briefing_docx",
        "description": "生成 Word 格式正式简报",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "region": {"type": "string"},
                "data_sources": {"type": "array", "items": {"type": "string"}},
                "impact_analysis": {"type": "string"},
            },
        },
    },
    {
        "name": "list_briefing_templates",
        "description": "列出可用简报模板",
        "parameters": {"type": "object", "properties": {}},
    },
]

functions = META_FUNCTIONS + ANALYSIS_FUNCTIONS + RISK_FUNCTIONS + REPORT_FUNCTIONS


def _track_stats(result):
    if result.get("success") and result.get("result") and result.get("query"):
        session_context.setdefault("last_stats", []).append(result)
    return result


def handle_function_call(function_name, arguments):
    args = arguments or {}

    # Meta
    if function_name == "scan_nc_directories":
        return scan_directories(args.get("directories"))
    if function_name == "build_nc_catalog":
        r = nc_catalog.build(args.get("directories"), args.get("force", False))
        if r.get("success"):
            session_context["last_catalog_summary"] = r.get("summary")
        return r
    if function_name == "analyze_data_availability":
        return nc_catalog.analyze_availability(
            args.get("element"), args.get("lon_min"), args.get("lon_max"),
            args.get("lat_min"), args.get("lat_max"),
            args.get("time_start"), args.get("time_end"), args.get("product_type"),
        )
    if function_name == "get_nc_file_detail":
        return nc_catalog.get_file_detail(args["file_path"]) if nc_catalog.entries else {
            "success": True, "detail": extract_file_meta(args["file_path"])
        }

    # Analysis - nc_reader
    if function_name == "open_nc_file":
        return nc_reader.open_file(args["file_path"])
    if function_name == "get_nc_file_info":
        return nc_reader.get_file_info()
    if function_name == "read_nc_variable":
        return nc_reader.read_variable(
            args["variable_name"], args.get("time_index"),
            args.get("lat_index"), args.get("lon_index"),
        )
    if function_name == "extract_location_data":
        r = nc_reader.extract_location_data(
            args["variable_name"], args["latitude"], args["longitude"], args.get("time_index"),
        )
        if r.get("success"):
            r = {
                **r,
                "query": {"variable": args["variable_name"]},
                "result": {"value": r["data"]["value"], "units": r["data"].get("units", "")},
            }
            return _track_stats(r)
        return r
    if function_name == "extract_area_stat":
        r = nc_reader.extract_area_stat(
            args["variable_name"], args["lon_min"], args["lon_max"],
            args["lat_min"], args["lat_max"], args.get("stat", "mean"), args.get("time_index"),
        )
        return _track_stats(r)
    if function_name == "extract_area_stats":
        r = stats.extract_area_stats(
            args["variable_name"], args["lon_min"], args["lon_max"],
            args["lat_min"], args["lat_max"], args.get("stat", "mean"),
            args.get("time_index"), args.get("time_avg", False),
        )
        return _track_stats(r)
    if function_name == "extract_point_stats":
        r = stats.extract_point_stats(
            args["variable_name"], args["latitude"], args["longitude"],
            args.get("start_time_idx"), args.get("end_time_idx"), args.get("stat", "mean"),
        )
        return _track_stats(r)
    if function_name == "find_max_value_location":
        return nc_reader.find_extreme_location(args["variable_name"], "max", args.get("time_index"),
            args.get("lon_min"), args.get("lon_max"), args.get("lat_min"), args.get("lat_max"))
    if function_name == "find_min_value_location":
        return nc_reader.find_extreme_location(args["variable_name"], "min", args.get("time_index"),
            args.get("lon_min"), args.get("lon_max"), args.get("lat_min"), args.get("lat_max"))
    if function_name == "extract_point_series":
        return nc_reader.extract_point_series(
            args["variable_name"], args["longitude"], args["latitude"],
            args.get("start_time_idx"), args.get("end_time_idx"),
        )
    if function_name == "extract_extreme_events":
        return stats.extract_extreme_events(
            args["variable_name"], args["threshold"],
            args["longitude"], args["latitude"],
            args.get("start_time_idx"), args.get("end_time_idx"),
        )
    if function_name == "compare_sources":
        return stats.compare_sources(
            args["file_paths"], args["variable_name"],
            args["latitude"], args["longitude"], args.get("time_index"),
        )
    if function_name == "query_by_datetime":
        return stats.query_by_datetime(args["datetime_str"])
    if function_name == "close_nc_file":
        return nc_reader.close_file()

    # Risk
    if function_name == "assess_sea_state":
        return assess_sea_state(
            args.get("wave_height"), args.get("surge_height"), args.get("wind_speed"),
            args.get("location"), args.get("time_label"),
        )
    if function_name == "assess_comprehensive_risk":
        return assess_comprehensive_risk(
            args["stats_results"], args.get("location"), args.get("time_label"),
        )
    if function_name == "assess_region_risk":
        return assess_region_risk(
            args.get("wave_height"), args.get("surge_height"), args.get("wind_speed"),
            args.get("region_name"), args.get("time_label"),
        )
    if function_name == "get_risk_criteria":
        return get_risk_criteria()

    # Report
    if function_name == "generate_briefing_preview":
        return generate_briefing_preview(
            args.get("title"), args.get("region"), args.get("data_sources"),
            args.get("stats_summary"), args.get("risk_data"), args.get("impact_analysis"),
        )
    if function_name == "generate_briefing_docx":
        return generate_briefing_docx(
            args.get("title"), args.get("region"), args.get("data_sources"),
            args.get("stats_summary"), args.get("risk_data"), args.get("impact_analysis"),
        )
    if function_name == "list_briefing_templates":
        return list_briefing_templates()

    return {"success": False, "message": f"未知函数: {function_name}"}
