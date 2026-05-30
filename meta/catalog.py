# -*- coding: utf-8 -*-
"""NC 文件索引缓存与可用性分析"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from meta.scanner import scan_directories
from meta.classifier import extract_file_meta

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CATALOG_PATH = CACHE_DIR / "nc_catalog.json"

PRODUCT_TYPE_LABELS = {
    "large_grid": "大网格数值预报",
    "small_grid": "小网格数值预报",
    "point_ai": "单点智能预报",
    "field_ai": "时空场智能预报",
    "point_or_other": "单点/其他",
    "unknown": "未识别",
}

ELEMENT_LABELS = {"wind": "风场", "wave": "海浪", "surge": "风暴潮"}


class NCCatalog:
    def __init__(self):
        self.entries: List[dict] = []
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def build(self, directories: Optional[List[str]] = None, force: bool = False) -> Dict[str, Any]:
        scan_result = scan_directories(directories)
        if not scan_result.get("success"):
            return scan_result

        entries = []
        errors = []
        for item in scan_result["files"]:
            path = item["path"]
            meta = extract_file_meta(path)
            if not meta.get("readable", True):
                errors.append({"path": path, "error": "unreadable"})
                continue
            meta["size_bytes"] = item.get("size_bytes", 0)
            entries.append(meta)

        self.entries = entries
        self._save_cache(entries, scan_result["scanned_roots"])

        return {
            "success": True,
            "file_count": len(entries),
            "error_count": len(errors),
            "errors": errors[:20],
            "catalog_path": str(CATALOG_PATH),
            "summary": self._build_summary(entries),
        }

    def load_cache(self) -> bool:
        if not CATALOG_PATH.exists():
            return False
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.entries = data.get("entries", [])
        return True

    def _save_cache(self, entries: List[dict], roots: List[str]):
        payload = {"roots": roots, "entries": entries}
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def _build_summary(self, entries: List[dict]) -> dict:
        by_element = {}
        by_product = {}
        for e in entries:
            for elem in e.get("elements", []) or ["unknown"]:
                by_element.setdefault(elem, 0)
                by_element[elem] += 1
            pt = e.get("product_type", "unknown")
            by_product.setdefault(pt, 0)
            by_product[pt] += 1
        return {"by_element": by_element, "by_product": by_product}

    def get_file_detail(self, file_path: str) -> Dict[str, Any]:
        for e in self.entries:
            if e.get("path") == file_path:
                return {"success": True, "detail": e}
        meta = extract_file_meta(file_path)
        return {"success": True, "detail": meta}

    def analyze_availability(
        self,
        element: Optional[str] = None,
        lon_min: Optional[float] = None,
        lon_max: Optional[float] = None,
        lat_min: Optional[float] = None,
        lat_max: Optional[float] = None,
        time_start: Optional[str] = None,
        time_end: Optional[str] = None,
        product_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.entries and not self.load_cache():
            return {"success": False, "message": "目录为空，请先调用 build_nc_catalog 构建索引"}

        matched = []
        partial = []
        rejected = []

        for e in self.entries:
            status, reason = self._check_entry(
                e, element, lon_min, lon_max, lat_min, lat_max,
                time_start, time_end, product_type,
            )
            row = {
                "path": e["path"],
                "elements": e.get("elements", []),
                "product_type": e.get("product_type"),
                "product_label": PRODUCT_TYPE_LABELS.get(e.get("product_type", ""), ""),
                "time_range": e.get("time_range"),
                "bbox": e.get("bbox"),
                "status": status,
                "reason": reason,
            }
            if status == "available":
                matched.append(row)
            elif status == "partial":
                partial.append(row)
            else:
                rejected.append(row)

        report_text = self._format_report(
            element, lon_min, lon_max, lat_min, lat_max,
            time_start, time_end, matched, partial, rejected,
        )

        return {
            "success": True,
            "query": {
                "element": element,
                "region": {"lon_min": lon_min, "lon_max": lon_max, "lat_min": lat_min, "lat_max": lat_max},
                "time": {"start": time_start, "end": time_end},
                "product_type": product_type,
            },
            "counts": {"available": len(matched), "partial": len(partial), "unavailable": len(rejected)},
            "available_files": matched,
            "partial_files": partial,
            "unavailable_files": rejected[:10],
            "recommended": [m["path"] for m in matched[:5]],
            "report": report_text,
        }

    def _check_entry(self, e, element, lon_min, lon_max, lat_min, lat_max, time_start, time_end, product_type):
        reasons = []
        ok = True

        if element and element not in e.get("elements", []):
            return "unavailable", f"不含要素 {element}"

        if product_type and e.get("product_type") != product_type:
            return "unavailable", f"产品类型不匹配（期望 {product_type}）"

        bbox = e.get("bbox")
        if bbox and all(v is not None for v in [lon_min, lon_max, lat_min, lat_max]):
            if not self._bbox_overlaps(bbox, lon_min, lon_max, lat_min, lat_max):
                return "unavailable", "空间范围不覆盖目标区域"

        tr = e.get("time_range")
        if tr and (time_start or time_end):
            if time_start and str(tr.get("end", "")) < time_start:
                ok = False
                reasons.append("时间范围早于目标")
            if time_end and str(tr.get("start", "")) > time_end:
                ok = False
                reasons.append("时间范围晚于目标")

        if not ok:
            return "partial", "; ".join(reasons)
        if bbox and all(v is not None for v in [lon_min, lon_max, lat_min, lat_max]):
            if not self._bbox_contains(bbox, lon_min, lon_max, lat_min, lat_max):
                return "partial", "仅部分覆盖目标区域"

        return "available", "满足查询条件"

    def _bbox_overlaps(self, bbox, lon_min, lon_max, lat_min, lat_max):
        return not (
            bbox["lon_max"] < min(lon_min, lon_max)
            or bbox["lon_min"] > max(lon_min, lon_max)
            or bbox["lat_max"] < min(lat_min, lat_max)
            or bbox["lat_min"] > max(lat_min, lat_max)
        )

    def _bbox_contains(self, bbox, lon_min, lon_max, lat_min, lat_max):
        return (
            bbox["lon_min"] <= min(lon_min, lon_max)
            and bbox["lon_max"] >= max(lon_min, lon_max)
            and bbox["lat_min"] <= min(lat_min, lat_max)
            and bbox["lat_max"] >= max(lat_min, lat_max)
        )

    def _format_report(self, element, lon_min, lon_max, lat_min, lat_max,
                       time_start, time_end, matched, partial, rejected):
        lines = ["# NC 数据可用性分析报告", ""]
        lines.append(f"## 1. 扫描概况")
        lines.append(f"- 索引文件总数: {len(self.entries)}")
        lines.append(f"- 完全可用: {len(matched)} | 部分可用: {len(partial)} | 不可用: {len(rejected)}")
        lines.append("")
        lines.append("## 2. 查询条件")
        if element:
            lines.append(f"- 目标要素: {ELEMENT_LABELS.get(element, element)}")
        if lon_min is not None:
            lines.append(f"- 目标区域: 经度 [{lon_min}, {lon_max}], 纬度 [{lat_min}, {lat_max}]")
        if time_start or time_end:
            lines.append(f"- 目标时间: {time_start or '不限'} ~ {time_end or '不限'}")
        lines.append("")
        lines.append("## 3. 可用文件清单")
        for m in matched[:15]:
            lines.append(f"- [{m['status']}] {m['path']} ({m['product_label']})")
        if partial:
            lines.append("")
            lines.append("## 4. 部分可用文件")
            for p in partial[:10]:
                lines.append(f"- {p['path']}: {p['reason']}")
        lines.append("")
        lines.append("## 5. 结论与推荐")
        if matched:
            lines.append(f"推荐使用: {matched[0]['path']}")
        elif partial:
            lines.append("无完全匹配文件，可考虑部分可用文件并注意时空范围限制。")
        else:
            lines.append("当前索引中无满足条件的文件，请检查数据目录或放宽查询条件。")
        return "\n".join(lines)


nc_catalog = NCCatalog()
