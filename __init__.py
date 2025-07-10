from typing import Dict

import json

from openai import OpenAI
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin, SandboxMethodType
from pydantic import Field

# 插件元信息
plugin = NekroPlugin(
    name="AI 智慧搜索",  # TODO: 插件名称
    module_name="nekro_plugin_kimi_search",  # TODO: 插件模块名 (如果要发布该插件，需要在 NekroAI 社区中唯一)
    description="通过 Kimi API 的 $web_search 内置函数进行联网搜索",  # TODO: 插件描述
    version="1.0.0",  # TODO: 插件版本
    author="dirac",  # TODO: 插件作者
    url="https://github.com/1A7432/nekro-plugin-kimi-search",  # TODO: 插件仓库地址
)


# 插件配置，根据需要修改
@plugin.mount_config()
class kimiconfig(ConfigBase):
    """kimi搜索插件配置"""

    API_URL: str = Field(
        default="",
        title="OpenAI API地址，后面加/v1",
        description="支持全部OpenAI格式的API 建议使用 Kimi API 进行联网搜索，或其他有联网搜索的API",
    )
    API_KEY: str = Field(
        default="",
        title="refresh_token",
        description="API KEY",
    )
    MODEL: str = Field(
        default="moonshot-v1-auto",
        title="模型名",
        description='进行搜索总结的模型。推荐使用 moonshot-v1-auto 以自动适应不同长度的搜索结果，避免报错。',
    )


# 获取配置实例
config: kimiconfig = plugin.get_config(kimiconfig)


@plugin.mount_sandbox_method(SandboxMethodType.AGENT, name="搜索", description="搜索关键词并返回结果")
async def search_ai(_ctx: AgentCtx, query: str) -> str:
    """根据用户提供的关键词进行联网搜索，并返回总结后的结果。

    Args:
        query: 需要搜索的关键词。

    Returns:
        str: Kimi总结的搜索结果。

    Example:
        search_ai(query="Kimi 是什么")
    """
    api_key = config.API_KEY
    api_base = config.API_URL
    model = config.MODEL

    if not all([api_key, api_base, model]):
        missing_configs = [name for name, value in [('API_KEY', api_key), ('API_URL', api_base), ('MODEL', model)] if not value]
        error_msg = f"插件配置不完整，请检查以下配置项: {', '.join(missing_configs)}"
        logger.error(error_msg)
        return error_msg

    try:
        client = OpenAI(api_key=api_key, base_url=api_base)
        messages = [
            {"role": "system", "content": "你是 Kimi，一个由 Moonshot AI 提供的人工智能助手。你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为你提供了互联网搜索的能力，你应当在需要时使用联网搜索来回答问题。"},
            {"role": "user", "content": query}
        ]

        logger.info(f"Kimi 开始处理查询: '{query}'")

        while True:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[
                    {
                        "type": "builtin_function",
                        "function": {
                            "name": "$web_search",
                        },
                    }
                ],
                temperature=0.3,
            )

            choice = response.choices[0]
            if choice.finish_reason == "tool_calls":
                logger.info("Kimi 请求调用工具: $web_search")
                messages.append(choice.message)  # 添加 assistant 的回复
                for tool_call in choice.message.tool_calls:
                    if tool_call.function.name == "$web_search":
                        # 解析参数以记录 token 使用情况
                        try:
                            tool_arguments = json.loads(tool_call.function.arguments)
                            search_tokens = tool_arguments.get("usage", {}).get("total_tokens")
                            if search_tokens:
                                logger.info(f"Kimi 搜索结果消耗 Tokens: {search_tokens}")
                        except json.JSONDecodeError:
                            logger.warning("无法解析 Kimi 工具调用参数中的 Tokens 信息")

                        # Kimi 的 $web_search 工具，我们只需将参数原样返回
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_call.function.name,
                                "content": tool_call.function.arguments,
                            }
                        )
            else:
                logger.info(f"Kimi 处理完成，最终原因: {choice.finish_reason}")
                return choice.message.content

    except Exception as e:
        logger.exception(f"搜索 '{query}' 时发生错误: {e}", exc_info=True)
        return f"搜索 '{query}' 时发生严重错误，请检查插件日志。"


@plugin.mount_cleanup_method()
async def clean_up():
    logger.info("AI智慧搜索插件已清理完毕")
