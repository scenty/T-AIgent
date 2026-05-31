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
    build_result = nc_catalog.build()
    if build_result.get("success"):
        save_memory_markdown(build_result)
        session_context["last_catalog_summary"] = build_result.get("summary")

SYSTEM_PROMPT = """你是一个专业的海洋预报 Agent，具备以下四类能力：

1. **NC 数据 Meta 分析**：扫描本地目录、构建索引、分析数据可用性
   - 工作流：scan_nc_directories → build_nc_catalog → analyze_data_availability / get_nc_file_detail

2. **时空统计分析**：打开 NC 文件后进行单点、区域、时序、极端值等分析
   - 工作流：open_nc_file → query_by_datetime（如需） → extract_* 系列函数

3. **灾害风险决策**：基于统计数据，按中国海洋预警标准评估风险等级
   - 工作流：必须先获取统计数据，再调用 assess_sea_state 或 assess_comprehensive_risk
   - 不得臆造数值或等级；可调用 get_risk_criteria 解释依据

4. **自动化简报**：基于风险评估结果生成 Markdown 预览和 Word 正式稿
   - 工作流：generate_briefing_preview → generate_briefing_docx

规则：
- 只能使用提供的函数，不要编造函数名
- 风险评估必须基于工具返回的真实数据
- 简报中的数值必须与统计/评估结果一致
- 若数据不可用，明确说明原因并建议下一步
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
    append_tool_call_memory(function_name, arguments, function_response)
    response_str = json.dumps(function_response, ensure_ascii=False)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": response_str,
    })
    return response_str


def run_tool_chain(messages: list[dict[str, Any]]) -> str:
    """多轮 tool 链：直到 assistant 不再返回 tool_calls"""
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
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

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
