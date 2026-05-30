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


def scan_directories(
    directories: Optional[List[str]] = None,
    extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    cfg = load_scan_config()
    scan_cfg = cfg.get("scan", {})
    ext_list = extensions or scan_cfg.get("extensions", [".nc", ".nc4"])

    if directories:
        roots = [{"path": d, "description": ""} for d in directories]
    else:
        roots = cfg.get("roots", [])

    found = []
    missing_roots = []

    for root in roots:
        path = root["path"] if isinstance(root, dict) else root
        p = Path(path).expanduser()
        if not p.exists():
            missing_roots.append(str(p))
            continue
        for dirpath, _, filenames in os.walk(p):
            for fname in filenames:
                if any(fname.endswith(ext) for ext in ext_list):
                    full = str(Path(dirpath) / fname)
                    found.append({
                        "path": full,
                        "root": str(p),
                        "size_bytes": os.path.getsize(full),
                    })

    return {
        "success": True,
        "scanned_roots": [r["path"] if isinstance(r, dict) else r for r in roots],
        "missing_roots": missing_roots,
        "file_count": len(found),
        "files": found,
    }
