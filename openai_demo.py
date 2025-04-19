from openai import OpenAI

# 自定义配置
api_key = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc1MjMzMDMzNiwiaWF0IjoxNzQ0NTU0MzM2LCJqdGkiOiJjdnRzaW80YmNkcnBjbWIyNWdzMCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3FzczBkMmxubDk2NDRmMDQ4NjAiLCJzcGFjZV9pZCI6ImNxc3MwZDJsbmw5NjQ0ZjA0ODUwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNxc3MwZDJsbmw5NjQ0ZjA0ODRnIn0.xYeS54nmWAp0RAcQ2HTTYqe2yLECffWY9JZTCIlkX1l3VaM8kBHZyKtW3URe30yDnYMIAbOsjj6q08KTZDFqwQ"
api_base = "http://10.31.1.23:8000/v1"
model = "kimi-search"

# 创建客户端实例
client = OpenAI(
    api_key=api_key,
    base_url=api_base
)

# 使用新版API发送请求
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "你是什么模型？"}
    ]
)

# 打印完整响应和思维链
print("=== 完整响应 ===")
print(response)
print("\n=== 思维链分析 ===")
print(f"模型: {response.model}")
print(f"完成原因: {response.choices[0].finish_reason}")
print(f"使用token数: 输入={response.usage.prompt_tokens}, 输出={response.usage.completion_tokens}")
print("\n=== 最终回答 ===")
print(response.choices[0].message.content)