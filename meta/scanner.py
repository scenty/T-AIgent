# -*- coding: utf-8 -*-
"""递归扫描本地 NC 文件"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "data_roots.yaml"


def load_scan_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {"roots": [], "scan": {"extensions": [".nc", ".nc4"], "exclude_patterns": []}}


def _normalize_directories(directories: Optional[List[str]], config_roots: List[Any]) -> List[str]:
    if directories:
        raw_items: List[str] = []
        for item in directories:
            if not item:
                continue
            for part in str(item).replace("\n", ";").replace(",", ";").split(";"):
                cleaned = part.strip()
                if cleaned:
                    raw_items.append(cleaned)
    else:
        raw_items = []
        for root in config_roots:
            if isinstance(root, dict):
                root_path = str(root.get("path", "")).strip()
                if root_path:
                    raw_items.append(root_path)
            else:
                root_path = str(root).strip()
                if root_path:
                    raw_items.append(root_path)

    seen: set[str] = set()
    normalized: List[str] = []
    for root in raw_items:
        expanded = str(Path(root).expanduser())
        key = expanded.lower() if os.name == "nt" else expanded
        if key in seen:
            continue
        seen.add(key)
        normalized.append(expanded)
    return normalized


def scan_directories(
    directories: Optional[List[str]] = None,
    extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    cfg = load_scan_config()
    scan_cfg = cfg.get("scan", {})
    ext_list = [ext.lower() for ext in (extensions or scan_cfg.get("extensions", [".nc", ".nc4"]))]
    normalized_roots = _normalize_directories(directories, cfg.get("roots", []))

    found = []
    missing_roots = []
    root_stats = []

    for root_path in normalized_roots:
        p = Path(root_path)
        if not p.exists():
            missing_roots.append(str(p))
            root_stats.append({
                "root": str(p),
                "exists": False,
                "file_count": 0,
                "size_bytes": 0,
            })
            continue

        root_file_count = 0
        root_total_size = 0
        for dirpath, _, filenames in os.walk(p):
            for fname in filenames:
                if any(fname.lower().endswith(ext) for ext in ext_list):
                    full = str(Path(dirpath) / fname)
                    file_size = os.path.getsize(full)
                    found.append({
                        "path": full,
                        "root": str(p),
                        "size_bytes": file_size,
                        "mtime": os.path.getmtime(full),
                    })
                    root_file_count += 1
                    root_total_size += file_size

        root_stats.append({
            "root": str(p),
            "exists": True,
            "file_count": root_file_count,
            "size_bytes": root_total_size,
        })

    return {
        "success": True,
        "scanned_roots": normalized_roots,
        "missing_roots": missing_roots,
        "root_stats": root_stats,
        "file_count": len(found),
        "files": found,
    }
