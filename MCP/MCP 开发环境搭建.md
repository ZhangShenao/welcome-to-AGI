# 1. 安装 uv 环境

## 打开终端，运⾏以下命令（uv 是⼀个极速的 Python 包管理器。）

curl -LsSf https://astral.sh/uv/install.sh | sh

## 查看 uv 安装结果

uv version

# 2. 初始化项目

## 为项目创建一个名为 weather 的新目录

uv init weather
cd weather 

## 创建并激活虚拟环境 (用于隔离项目依赖)

uv venv
source .venv/bin/activate 

## 安装项目所需的依赖包

uv add "mcp[cli]" httpx

## 开发 MCP Server 代码
