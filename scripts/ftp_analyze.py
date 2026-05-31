from __future__ import annotations

from dataclasses import dataclass, asdict
from ftplib import FTP
from typing import Any, List, Tuple
import json

HOST = "120.42.36.229"
PORT = 22210
USERNAME = "zdyfsjgx"
PASSWORD = "Sjgx@1234!"
START_PATH = "/group3/"
MAX_DEPTH = 1  # 0=仅根节点，1=仅列出一级路径
OUTPUT_FILE = "ftp_tree.json"


@dataclass
class Node:
    path: str
    type: str  # "dir" | "file"
    children: List["Node"]
    description: str = ""  # 预留文字描述字段，后续可手工填写


def list_entries(ftp: FTP, remote_path: str) -> List[Tuple[str, bool]]:
    ftp.cwd(remote_path)
    lines: List[str] = []
    ftp.retrlines("LIST", lines.append)

    entries: List[Tuple[str, bool]] = []
    for line in lines:
        parts = line.split(maxsplit=8)
        if len(parts) < 9:
            continue
        perms = parts[0]
        name = parts[8]
        if name in {".", ".."}:
            continue
        is_dir = perms.startswith("d")
        entries.append((name, is_dir))
    return entries


def walk_ftp(ftp: FTP, remote_path: str, current_depth: int = 0, max_depth: int = 1) -> Node:
    items = list_entries(ftp, remote_path)
    children: List[Node] = []
    subdirs: List[str] = []
    files: List[str] = []

    for name, is_dir in items:
        if is_dir:
            subdirs.append(name)
        else:
            files.append(name)

    for dir_name in subdirs:
        full_path = f"{remote_path.rstrip('/')}/{dir_name}" if remote_path != "/" else f"/{dir_name}"
        if current_depth < max_depth:
            child = walk_ftp(ftp, full_path, current_depth + 1, max_depth)
            children.append(child)
            ftp.cwd(remote_path)
        else:
            children.append(Node(path=full_path, type="dir", children=[]))

    latest_files = list_latest_files_in_dir(ftp, remote_path, files, limit=5)
    for file_name in latest_files:
        full_path = f"{remote_path.rstrip('/')}/{file_name}" if remote_path != "/" else f"/{file_name}"
        children.append(Node(path=full_path, type="file", children=[]))

    return Node(path=remote_path, type="dir", children=children)


def list_latest_files_in_dir(ftp: FTP, remote_path: str, files: List[str], limit: int = 5) -> List[str]:
    records: List[Tuple[str, str]] = []
    for name in files:
        full_path = f"{remote_path.rstrip('/')}/{name}" if remote_path != "/" else f"/{name}"
        mdtm_resp = ftp.sendcmd(f"MDTM {full_path}")
        modified = mdtm_resp.split()[-1]
        records.append((name, modified))
    records.sort(key=lambda item: item[1], reverse=True)
    return [name for name, _ in records[:limit]]


def save_tree_json(payload: dict[str, Any], output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    ftp = FTP()
    ftp.connect(host=HOST, port=PORT)
    ftp.login(USERNAME, PASSWORD)
    ftp.set_pasv(True)

    tree = walk_ftp(ftp, START_PATH, max_depth=MAX_DEPTH)
    payload = {
        "tree": asdict(tree),
    }
    save_tree_json(payload, OUTPUT_FILE)

    ftp.quit()
    print(f"完成：已保存 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()