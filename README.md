# Nekro Kimi 搜索插件

这是一个为 Nekro Agent 开发的插件，通过调用官方 Kimi API 实现联网搜索功能。它利用了 Kimi 强大的 `$web_search` 内置函数，以获取准确、实时的搜索结果。

## 功能特性

- **官方 API**：直接与官方 Kimi API 集成，稳定可靠。
- **内置函数**：使用官方推荐的 `$web_search` 内置函数，以处理复杂的、可能需要多步骤的搜索任务。
- **自动处理**：插件会自动处理与模型的工具调用循环，简化了使用流程。
- **智能模型选择**：默认并推荐使用 `moonshot-v1-auto` 模型，以动态适应不同长度的搜索结果，避免因超出上下文窗口而导致的错误。

## 配置

要在 Nekro Agent 中使用此插件，您需要在插件配置页面填入以下信息：

1.  **API_URL**: 您的 Kimi API 地址。通常是 `https://api.moonshot.cn/v1`。
2.  **API_KEY**: 您在 [Kimi 开放平台](https://platform.moonshot.cn/) 获取的 API 密钥。
3.  **MODEL**: 使用的模型名称。强烈推荐使用 `moonshot-v1-auto`。

## 安装

1.  将本项目克隆或下载到本地。
2.  将 `nekro_plugin_kimi_search` 文件夹放入 Nekro Agent 的 `plugins` 目录中。
3.  重启 Nekro Agent。
4.  在插件市场页面启用“AI 智慧搜索”插件，并完成上述配置。

## 使用

配置完成后，当您向 Agent 提出需要访问互联网才能回答的问题时，它将自动调用此插件进行搜索，并为您提供总结后的答案。

## 鸣谢

本项目 fork 自 [wess09/nekro-plugin-kimi-search](https://github.com/wess09/nekro-plugin-kimi-search)，并在此基础上进行修改。