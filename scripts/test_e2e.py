# -*- coding: utf-8 -*-
"""端到端功能验证脚本"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from meta.scanner import scan_directories
from meta.catalog import nc_catalog
from analysis.nc_reader import nc_reader
from analysis import statistics as stats
from risk.assessor import assess_sea_state, assess_comprehensive_risk
from report.generator import generate_briefing_preview, generate_briefing_docx

SAMPLE = BASE / "sample_data"


def run_e2e():
    print("=== 1. Meta 扫描 ===")
    scan = scan_directories([str(SAMPLE)])
    assert scan["file_count"] >= 1, "应有示例文件"
    print(f"  找到 {scan['file_count']} 个文件")

    print("=== 2. 构建目录 ===")
    catalog = nc_catalog.build([str(SAMPLE)])
    assert catalog["success"]
    print(f"  索引 {catalog['file_count']} 个文件")

    print("=== 3. 可用性分析 ===")
    avail = nc_catalog.analyze_availability(
        element="wave", lon_min=113, lon_max=115, lat_min=21, lat_max=23,
    )
    assert avail["success"]
    print(f"  可用: {avail['counts']['available']}")

    wave_file = SAMPLE / "wave_forecast_small_grid.nc"
    print("=== 4. 区域统计 ===")
    nc_reader.open_file(str(wave_file))
    area = stats.extract_area_stats("swh", 113, 115, 21, 23, stat="mean", time_index=12)
    assert area["success"]
    print(f"  区域平均波高: {area['result']['value']:.2f} m")

    dt = nc_reader.query_by_datetime("2024-08-15T12:00:00")
    assert dt["success"]
    print(f"  时间索引: {dt['result']['time_index']}")

    nc_reader.close_file()

    print("=== 5. 风险评估 ===")
    risk = assess_sea_state(wave_height=area["result"]["value"], location="珠江口")
    assert risk["success"]
    print(f"  综合等级: {risk['comprehensive']['level_name']}")

    print("=== 6. 简报生成 ===")
    md = generate_briefing_preview(region="珠江口", stats_summary=[area], risk_data=risk)
    docx = generate_briefing_docx(region="珠江口")
    assert md["success"] and docx["success"]
    print(f"  Markdown: {md['path']}")
    print(f"  Word: {docx['path']}")

    print("\n=== 全部测试通过 ===")


if __name__ == "__main__":
    run_e2e()
