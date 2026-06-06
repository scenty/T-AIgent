import os
import re
import json
import base64
import ctypes
from pathlib import Path
from typing import Any
from datetime import datetime
from ctypes import POINTER, byref, cast, c_char, windll
from ctypes import wintypes
from openai import OpenAI
from agent_tools import functions, handle_function_call
from meta.catalog import nc_catalog
from risk.assessor import session_context

DEFAULT_API_KEY_FILE = Path(".secrets/deepseek_api_key.bin")
MEMORY_FILE = Path("memory.md")
MEMORY_RECENT_TOOL_LIMIT = 5


class DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", POINTER(c_char))]


def _dpapi_decrypt(encrypted: bytes) -> bytes:
    in_buffer = ctypes.create_string_buffer(encrypted, len(encrypted))
    in_blob = DataBlob(len(encrypted), cast(in_buffer, POINTER(c_char)))
    out_blob = DataBlob()
    success = windll.crypt32.CryptUnprotectData(byref(in_blob), None, None, None, None, 0, byref(out_blob))
    if not success:
        raise RuntimeError("DPAPI 解密失败")
    decrypted = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    windll.kernel32.LocalFree(out_blob.pbData)
    return decrypted


def get_api_key_file() -> Path:
    file_from_env = os.environ.get("DEEPSEEK_API_KEY_FILE", "").strip()
    if file_from_env:
        return Path(file_from_env)
    return DEFAULT_API_KEY_FILE


def decode_api_key(value: bytes) -> str:
    if value.startswith(b"dpapi:"):
        encrypted = base64.urlsafe_b64decode(value.removeprefix(b"dpapi:"))
        return _dpapi_decrypt(encrypted).decode("utf-8")
    return value.decode("utf-8").strip()


def load_api_key() -> str:
    api_key_file = get_api_key_file()
    if api_key_file.exists():
        value = api_key_file.read_bytes()
        return decode_api_key(value)
    return ""


API_KEY_FILE = get_api_key_file()
API_KEY = load_api_key()

client = OpenAI(
    api_key=API_KEY,
    base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)


def save_memory_markdown(meta_result: dict[str, Any]) -> None:
    summary = meta_result.get("summary", {})
    by_element = summary.get("by_element", {})
    by_product = summary.get("by_product", {})

    element_lines = ["- 无"]
    if by_element:
        element_lines = [f"- `{k}`: {v}" for k, v in by_element.items()]

    product_lines = ["- 无"]
    if by_product:
        product_lines = [f"- `{k}`: {v}" for k, v in by_product.items()]

    structured_cache = json.dumps(
        {
            "file_count": meta_result.get("file_count", 0),
            "catalog_path": meta_result.get("catalog_path", ""),
            "summary": summary,
            "reused_count": meta_result.get("reused_count"),
            "new_count": meta_result.get("new_count"),
        },
        ensure_ascii=False,
        indent=2,
    )

    section_lines = [
        f"- 更新时间: {datetime.now().isoformat(timespec='seconds')}",
        f"- 文件总数: {meta_result.get('file_count', 0)}",
        f"- 索引路径: {meta_result.get('catalog_path', '')}",
        "",
        "### 要素分布",
        *element_lines,
        "",
        "### 产品分布",
        *product_lines,
        "",
        "### 结构化缓存（供程序读取）",
        "```json",
        structured_cache,
        "```",
    ]
    upsert_memory_section("文件状态", "\n".join(section_lines))


def upsert_memory_section(section_title: str, section_content: str) -> None:
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
    else:
        content = "# Meta 分析记忆\n"

    if not content.strip():
        content = "# Meta 分析记忆\n"
    if not content.startswith("# Meta 分析记忆"):
        content = f"# Meta 分析记忆\n\n{content.lstrip()}"

    normalized_body = section_content.strip()
    replacement = f"## {section_title}\n{normalized_body}\n"
    pattern = rf"(?ms)^## {re.escape(section_title)}\n.*?(?=^## |\Z)"

    if re.search(pattern, content):
        updated = re.sub(pattern, lambda _: replacement, content)
    else:
        updated = f"{content.rstrip()}\n\n{replacement}"

    MEMORY_FILE.write_text(f"{updated.rstrip()}\n", encoding="utf-8")


def append_tool_call_memory(function_name: str, arguments: dict[str, Any], function_response: Any) -> None:
    record_time = datetime.now().isoformat(timespec="seconds")
    arguments_text = json.dumps(arguments, ensure_ascii=False, indent=2)
    response_text = json.dumps(function_response, ensure_ascii=False, indent=2)
    entry = (
        f"\n### {record_time} | {function_name}\n"
        f"- 参数:\n"
        f"```json\n{arguments_text}\n```\n"
        f"- 响应:\n"
        f"```json\n{response_text}\n```\n"
    )
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
    else:
        content = "# Meta 分析记忆\n"
    if "## 工具调用记录" not in content:
        content = f"{content.rstrip()}\n\n## 工具调用记录\n"
    MEMORY_FILE.write_text(f"{content.rstrip()}\n{entry}", encoding="utf-8")


def read_memory_file() -> str:
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return ""


def extract_memory_section(content: str, section_title: str) -> str:
    if not content:
        return ""
    pattern = rf"(?ms)^## {re.escape(section_title)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else ""


def parse_structured_cache(content: str) -> dict[str, Any] | None:
    section = extract_memory_section(content, "文件状态") or content
    match = re.search(r"```json\n(.*?)\n```", section, re.DOTALL)
    if not match:
        return None
    data = json.loads(match.group(1))
    return data if isinstance(data, dict) and "file_count" in data else None


def _summarize_tool_response(function_name: str, response: Any) -> str:
    if not isinstance(response, dict):
        return str(response)[:120]
    parts = []
    if "success" in response:
        parts.append(f"success={response['success']}")
    for key in ("file_count", "error_count", "message"):
        if key in response:
            parts.append(f"{key}={response[key]}")
    comp = response.get("comprehensive")
    if isinstance(comp, dict) and comp.get("level_name"):
        parts.append(f"level={comp['level_name']}")
    if parts:
        return ", ".join(parts)
    return json.dumps(response, ensure_ascii=False)[:120]


def extract_tool_call_section(content: str) -> str:
    marker = "## 工具调用记录"
    idx = content.find(marker)
    if idx == -1:
        return ""
    return content[idx + len(marker):].lstrip()


def extract_recent_tool_summaries(content: str, limit: int = MEMORY_RECENT_TOOL_LIMIT) -> list[str]:
    section = extract_tool_call_section(content)
    blocks = [block for block in re.split(r"(?m)^### ", section) if block.strip()]
    lines = []
    for block in blocks[-limit:]:
        header_line, _, body = block.partition("\n")
        if " | " not in header_line:
            continue
        ts, name = header_line.split(" | ", 1)
        ts = ts.strip()
        name = name.strip()
        resp_match = re.search(r"- 响应:\n```json\n(.+?)\n```", body, re.DOTALL)
        if resp_match:
            response = json.loads(resp_match.group(1))
            summary = _summarize_tool_response(name, response)
            lines.append(f"- [{ts}] {name}: {summary}")
        else:
            lines.append(f"- [{ts}] {name}")
    return lines


def format_session_snapshot() -> list[str]:
    lines = []
    summary = session_context.get("last_catalog_summary")
    if summary:
        by_element = summary.get("by_element", {})
        by_product = summary.get("by_product", {})
        if by_element:
            lines.append(f"- 索引要素: {json.dumps(by_element, ensure_ascii=False)}")
        if by_product:
            lines.append(f"- 索引产品: {json.dumps(by_product, ensure_ascii=False)}")

    risk = session_context.get("last_risk")
    if isinstance(risk, dict) and risk.get("success"):
        comp = risk.get("comprehensive") or {}
        loc = risk.get("location") or ""
        time_label = risk.get("time") or ""
        suffix = f" ({loc} {time_label})".strip()
        lines.append(f"- 最近风险评估: {comp.get('level_name', '未知')}{suffix}")

    stats = session_context.get("last_stats") or []
    if stats:
        lines.append(f"- 最近统计记录: {len(stats)} 条")
        for item in stats[-3:]:
            query = item.get("query") or {}
            result = item.get("result") or item.get("data") or {}
            value = result.get("value") if isinstance(result, dict) else None
            if value is not None:
                lines.append(f"  - {query.get('variable', '?')}: {value}")
    return lines


def build_memory_context() -> str:
    content = read_memory_file()
    cache = parse_structured_cache(content)
    catalog_lines = extract_memory_section(content, "文件状态")
    if not catalog_lines:
        legacy = re.search(r"(?ms)^# Meta 分析记忆\n+(.*?)(?=^## |\Z)", content)
        if legacy:
            catalog_lines = legacy.group(1).strip()

    parts = [
        "## 持久化记忆（memory.md）",
        "",
        "### 数据索引状态",
    ]

    if cache:
        parts.append(f"- 文件总数: {cache.get('file_count', 0)}")
        parts.append(f"- 索引路径: {cache.get('catalog_path', '')}")
        summary = cache.get("summary") or {}
        if summary.get("by_element"):
            parts.append(f"- 要素分布: {json.dumps(summary['by_element'], ensure_ascii=False)}")
        if summary.get("by_product"):
            parts.append(f"- 产品分布: {json.dumps(summary['by_product'], ensure_ascii=False)}")
    elif catalog_lines:
        trimmed = re.sub(r"### 结构化缓存.*?```.*?```", "", catalog_lines, flags=re.DOTALL).strip()
        for line in trimmed.splitlines():
            if line.strip():
                parts.append(line if line.startswith("-") else f"- {line}")
    else:
        parts.append("- 尚无索引记录，需先调用 build_nc_catalog")

    session_lines = format_session_snapshot()
    if session_lines:
        parts.extend(["", "### 当前会话上下文", *session_lines])

    recent_tools = extract_recent_tool_summaries(content)
    if recent_tools:
        parts.extend(["", f"### 近期工具调用（最近 {len(recent_tools)} 条）", *recent_tools])

    parts.extend([
        "",
        "说明：以上来自 memory.md 与会话状态，供避免重复扫描和延续上下文；具体数值以本次工具实时返回为准。",
    ])
    return "\n".join(parts)


def build_system_prompt(memory_context: str) -> str:
    return f"{SYSTEM_PROMPT.strip()}\n\n---\n\n{memory_context.strip()}"


def refresh_system_prompt(messages: list[dict[str, Any]]) -> None:
    prompt = build_system_prompt(build_memory_context())
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = prompt
    else:
        messages.insert(0, {"role": "system", "content": prompt})


def print_available_tools_and_examples() -> None:
    print("\n可用工具：")
    for tool in functions:
        print(f"- {tool['name']}: {tool.get('description', '')}")

    print("\n简单示例：")
    examples = [
        "1) 先扫描并建索引：请扫描 NC 目录并构建索引。",
        "2) 查询可用性：请分析 wave 在 118-123E, 24-29N、未来48小时的数据可用性。",
        "3) 统计分析：打开某个 NC 文件后，提取某点位浪高时间序列。",
        "4) 风险评估：基于统计结果评估综合海况风险。",
    ]
    for line in examples:
        print(line)


def initialize_meta_memory() -> None:
    print("小助手初始化中...")
    has_cache = nc_catalog.load_cache()
    memory_cache = parse_structured_cache(read_memory_file())
    if has_cache:
        mem_count = memory_cache.get("file_count") if memory_cache else None
        msg = f"  已加载索引缓存 {len(nc_catalog.entries)} 个文件"
        if mem_count is not None:
            msg += f"（memory 记录 {mem_count}）"
        print(msg + "，检查新增/变更...")
    build_result = nc_catalog.build()
    if build_result.get("success"):
        reused = build_result.get("reused_count", 0)
        new_count = build_result.get("new_count", 0)
        if build_result.get("incremental"):
            print(f"  索引就绪：复用 {reused}，新增/更新 {new_count}，合计 {build_result.get('file_count', 0)}")
        save_memory_markdown(build_result)
        session_context["last_catalog_summary"] = build_result.get("summary")

SYSTEM_PROMPT = """你是一个专业的海洋预报 Agent，具备以下四类能力：

1. **NC 数据 Meta 分析**：扫描本地目录、构建索引、分析数据可用性
   - 工作流：lookup_station（按站名） → scan_nc_directories → build_nc_catalog → analyze_data_availability / get_nc_file_detail

2. **时空统计分析**：打开 NC 文件后进行单点、区域、时序、极端值等分析
   - 工作流：open_nc_file → 查看 layout_mode → query_by_datetime（如需） → extract_* 系列函数
   - layout_mode=time_series（海浪单点 swh）：变量仅 time 维，直接 extract_point_series，勿按网格取点
   - layout_mode=grid_1x1（风暴潮单点）：变量含 1×1 空间维
   - layout_mode=grid（时空场）：按经纬度取点或区域统计

3. **灾害风险决策**：基于统计数据，按中国海洋预警标准评估风险等级
   - 工作流：必须先获取统计数据，再调用 assess_sea_state 或 assess_comprehensive_risk
   - 不得臆造数值或等级；可调用 get_risk_criteria 解释依据

4. **自动化简报**：基于风险评估结果生成 Markdown 预览和 Word 正式稿
   - 工作流：generate_briefing_preview → generate_briefing_docx

规则：
- 只能使用提供的函数，不要编造函数名
- 本地 NC 数据根目录、站点映射、layout、变量均在 `config/data_roots.yaml`；未指定 directories 时，scan_nc_directories / build_nc_catalog 默认按该文件扫描
- 按站名分析时先调用 lookup_station；例如「新竹站海浪」对应 file_code=46757B（新竹浮标），不是 46694A（龙洞浮标）
- 打开文件后检查 layout_mode 与 root_variables，选用正确变量名（单点海浪用 swh，时空场用 hs_torch）
- 风险评估必须基于工具返回的真实数据
- 简报中的数值必须与统计/评估结果一致
- 若数据不可用，明确说明原因并建议下一步
- 参考系统提示末尾「持久化记忆」了解已有索引与近期操作，避免不必要的重复扫描；数值以本次工具返回为准
"""


def chat_with_deepseek(messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> Any:
    kwargs = {
        "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro"),
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)


def process_function_call(tool_call: Any, messages: list[dict[str, Any]]) -> str:
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    function_response = handle_function_call(function_name, arguments)
    if function_name == "build_nc_catalog" and function_response.get("success"):
        save_memory_markdown(function_response)
    append_tool_call_memory(function_name, arguments, function_response)
    refresh_system_prompt(messages)
    response_str = json.dumps(function_response, ensure_ascii=False)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": response_str,
    })
    return response_str


def run_tool_chain(messages: list[dict[str, Any]]) -> str:
    """多轮 tool 链：直到 assistant 不再返回 tool_calls"""
    refresh_system_prompt(messages)
    tool_specs = [{"type": "function", "function": func} for func in functions]
    max_rounds = 10
    for _ in range(max_rounds):
        response = chat_with_deepseek(messages, tools=tool_specs)
        assistant_message = response.choices[0].message

        if not getattr(assistant_message, "tool_calls", None):
            return assistant_message.content

        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in assistant_message.tool_calls
            ],
        })
        for tool_call in assistant_message.tool_calls:
            process_function_call(tool_call, messages)

    return "已达到最大工具调用轮数，请简化查询后重试。"


def process_chat() -> None:
    initialize_meta_memory()
    print_available_tools_and_examples()
    messages = [{"role": "system", "content": build_system_prompt(build_memory_context())}]

    while True:
        user_input = input("\n您: ")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("感谢使用，再见！")
            break

        messages.append({"role": "user", "content": user_input})
        result = run_tool_chain(messages)
        messages.append({"role": "assistant", "content": result})
        print(f"\n助手: {result}")


if __name__ == "__main__":
    process_chat()
