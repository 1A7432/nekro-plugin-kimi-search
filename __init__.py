from typing import Dict

from openai import OpenAI
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin, SandboxMethodType
from pydantic import Field

# TODO: 插件元信息，请修改为你的插件信息
plugin = NekroPlugin(
    name="KIMI AI 搜索插件",  # TODO: 插件名称
    module_name="nekro_plugin_kimi_search",  # TODO: 插件模块名 (如果要发布该插件，需要在 NekroAI 社区中唯一)
    description="使用kimi-free-api进行联网搜索",  # TODO: 插件描述
    version="1.0.4",  # TODO: 插件版本
    author="wess09",  # TODO: 插件作者
    url="https://github.com/wess09/nekro-plugin-kimi-search",  # TODO: 插件仓库地址
)


# TODO: 插件配置，根据需要修改
@plugin.mount_config()
class kimiconfig(ConfigBase):
    """kimi搜索插件配置"""

    API_URL: str = Field(
        default="",
        title="KIMI Free API地址，后面加/v1",
        description="不能用中转站的，你自己部署",
    )
    API_KEY: str = Field(
        default="",
        title="refresh_token",
        description="ey开头的那个",
    )
    MODEL: str = Field(
        default="",
        title="refresh_token",
        description="ey开头的那个",
    )


# 获取配置实例
config: kimiconfig = plugin.get_config(kimiconfig)


@plugin.mount_sandbox_method(SandboxMethodType.AGENT, name="搜索", description="搜索关键词并返回结果")
async def searchkimi(_ctx: AgentCtx, search_data: str) -> str:
    """搜索互联网上的关键词或网页URL

    Args:
        search_data: 需要搜索的关键词或网页URL。

    Returns:
        str: 总结好的搜索结果。

    Example:
        搜索关键词:
        searchkimi(search_data="北京有什么好玩的")
        查询网页上的信息:
        searchkimi(search_data="https://url.com")
    """
    # OpenAI API参数配置，可根据实际情况调整
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
    """清理插件资源"""
    # 如果有使用数据库连接、文件句柄或其他需要释放的资源，在此处添加清理逻辑
    logger.info("kimi搜索插件已清理完毕")
