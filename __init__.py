from typing import Dict

from openai import OpenAI
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin, SandboxMethodType
from pydantic import Field

# 插件元信息
plugin = NekroPlugin(
    name="AI 智慧搜索",  # TODO: 插件名称
    module_name="nekro_plugin_kimi_search",  # TODO: 插件模块名 (如果要发布该插件，需要在 NekroAI 社区中唯一)
    description="使用 类OpenAI接口 进行联网搜索",  # TODO: 插件描述
    version="1.1.5",  # TODO: 插件版本
    author="wess09",  # TODO: 插件作者
    url="https://github.com/wess09/nekro-plugin-kimi-search",  # TODO: 插件仓库地址
)


# 插件配置，根据需要修改
@plugin.mount_config()
class kimiconfig(ConfigBase):
    """kimi搜索插件配置"""

    API_URL: str = Field(
        default="",
        title="OpenAI API地址，后面加/v1",
        description="支持全部OpenAI格式的API 建议使用 Kimi FREE API 进行联网搜索，或其他有联网搜索的API",
    )
    API_KEY: str = Field(
        default="",
        title="refresh_token",
        description="API KEY 或 refresh_token",
    )
    MODEL: str = Field(
        default="",
        title="模型名",
        description="进行搜索总结的模型",
    )


# 获取配置实例
config: kimiconfig = plugin.get_config(kimiconfig)


@plugin.mount_sandbox_method(SandboxMethodType.AGENT, name="搜索", description="搜索关键词并返回结果")
async def search_ai(_ctx: AgentCtx, search_data: str) -> str:
    """搜索互联网上的关键词或网页URL

    Args:
        search_data: 需要搜索的关键词或网页URL。

    Returns:
        str: 总结好的搜索结果。

    Example:
        搜索关键词:
        search_ai(search_data="北京有什么好玩的")
        查询网页上的信息:
        search_ai(search_data="https://url.com")
    """
    # OpenAI API参数配置
    api_key = config.API_KEY
    api_base = config.API_URL
    model = config.MODEL
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        messages = [
            {"role": "system", "content": "你是一个智能搜索助手，能够根据用户输入的关键词或网址，返回简明、准确的摘要信息。"},
            {"role": "user", "content": search_data}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        result = f"搜索结果: {response.choices[0].message.content}\n"
        logger.info(f"已完成搜索: {search_data}")
        return result
    except Exception as e:
        logger.exception(f"搜索 '{search_data}' 时发生未知错误: {e}", exc_info=True)
        return f"搜索 '{search_data}' 时发生内部错误。"


@plugin.mount_cleanup_method()
async def clean_up():
    logger.info("AI智慧搜索插件已清理完毕")
