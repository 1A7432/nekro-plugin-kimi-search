# Kimi搜索插件
## 教程
请先自行部署KIMI free项目
https://github.com/LLM-Red-Team/kimi-free-api

懒得看直接运行

sudo docker run -it -d --init --name kimi-free-api -p 8000:8000 -e TZ=Asia/Shanghai vinlic/kimi-free-api:latest

## 获取key
## ey开头的
https://github.com/LLM-Red-Team/kimi-free-api?tab=readme-ov-file#%E6%8E%A5%E5%85%A5%E5%87%86%E5%A4%87

从 kimi.moonshot.cn 获取refresh_token

进入kimi随便发起一个对话，然后F12打开开发者工具，从Application > Local Storage中找到refresh_token的值，这将作为Authorization的Bearer Token值：Authorization: Bearer TOKEN


如果你看到的refresh_token是一个数组，请使用.拼接起来再使用。

## 调整
吧容器超时时间调大点

## 警告
请勿吧kimi free用于na本体
不要用太狠
有概率会封号