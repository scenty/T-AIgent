import os
import json
from openai import OpenAI
from agent_tools import functions, handle_function_call

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
)

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


def chat_with_deepseek(messages, tools=None):
    kwargs = {"model": "deepseek-chat", "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)


def process_function_call(tool_call, messages):
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print(f"\n调用函数: {function_name}")
    print(f"参数: {arguments}")

    function_response = handle_function_call(function_name, arguments)
    response_str = json.dumps(function_response, ensure_ascii=False)
    print(f"函数响应: {response_str[:500]}{'...' if len(response_str) > 500 else ''}")

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": response_str,
    })
    return response_str


def run_tool_chain(messages):
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


def process_chat():
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("警告: 未设置 DEEPSEEK_API_KEY 环境变量，API 调用将失败。")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("海洋预报 Agent 已启动！")
    print("支持：Meta 分析 | 时空统计 | 风险决策 | 简报生成")
    print("输入'退出'结束会话")

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
