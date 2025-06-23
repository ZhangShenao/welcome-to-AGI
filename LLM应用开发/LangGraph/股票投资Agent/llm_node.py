# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 15:00 
@Author  : ZhangShenao 
@File    : llm_node.py 
@Desc    : LLM节点
"""
import os

import dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from tools import TOOLS

# 加载环境变量
dotenv.load_dotenv()

# 定义SystemPrompt
SYSTEM_PROMPT = SystemMessage(content="""
你是一位智能的股票助手，精通股票投资领域的各类知识。
请从专业角度，回答用户提出的问题。
如果用户询问股票代码或股票名称，请直接给出股票代码或名称，不要回答其它额外信息。
如有需要，可以调用相关工具。
""")

# 创建DeepSeek客户端
llm = ChatOpenAI(
    model="deepseek-chat",  # 使用DeepSeek-V3 Chat Model
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_BASE"),
)

# 将LLM绑定Tools
llm = llm.bind_tools(TOOLS)


def llm_node(state: MessagesState) -> MessagesState:
    """LLM节点: 调用LLM,生成结果"""

    # 创建消息列表
    messages = [SYSTEM_PROMPT] + state["messages"]

    # 调用LLM
    response = llm.invoke(messages)

    # 返回最新的消息状态
    return {"messages": [response]}
