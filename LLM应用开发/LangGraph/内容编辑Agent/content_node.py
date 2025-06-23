# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/18 14:33 
@Author  : ZhangShenao 
@File    : title_node.py 
@Desc    : 文章正文内容节点
"""
import json
import os

import dotenv
import requests
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, CONTENT_PROMPT
from state import ArticleState

dotenv.load_dotenv()


# 定义检索工具
@tool
def search(query: str) -> str:
    """根据关键词，在互联网上检索相关信息
    Args:
        query: 检索关键词
    """

    print(f"调用工具: [search], 调用参数: {query}")

    # 构造请求参数
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
    })
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),  # 在Serper官网申请api_key
        'Content-Type': 'application/json'
    }

    # 发送请求
    response = requests.request("POST", url, headers=headers, data=payload).json()

    # 解析响应结果
    if response['organic'][0]:
        return response['organic'][0]['snippet']

    return "没有搜索到相关结果"


# 定义工具列表
TOOLS = [search]
TOOL_DICT = {tool.name: tool for tool in TOOLS}


def content_node(state: ArticleState) -> ArticleState:
    """
    文章正文内容节点
    :param state: 当前文章状态
    :return: 处理后的文章状态
    """

    # 从当前状态中获取所需信息
    if not state["topic"]:
        raise ValueError("未指定文章主题！")
    if not state["title"]:
        raise ValueError("文章标题缺失！")

    topic = state["topic"]
    title = state["title"]

    # 构造消息列表
    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(topic=topic)),
        HumanMessage(content=CONTENT_PROMPT.format(title=title)),
    ]

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 将DeepSeek绑定工具列表
    deepseek = deepseek.bind_tools(TOOLS)

    # 调用DeepSeek,获取结果
    while True:
        # 调用LLM,并保存结果
        reply = deepseek.invoke(messages)
        messages.append(reply)

        # 未返回工具调用参数,说明模型直接生成了回复,则更新状态后返回
        if len(reply.tool_calls) == 0:
            content = reply.content
            state["content"] = content
            print(f"文章正文生成完成：共 {len(content)} 字")
            return state

        # 解析工具调用参数
        for tool_call in reply.tool_calls:
            # 根据名称,获取需要调用的工具
            tool_name = tool_call["name"]
            tool = TOOL_DICT[tool_name]

            if tool is not None:
                # 调用工具,获取结果
                tool_call_result = tool.invoke(tool_call["args"])
                print(f"工具调用结果: {tool_call_result}")

                # 保存工具调用结果
                tool_msg = ToolMessage(content=tool_call_result, tool_call_id=tool_call["id"])
                messages.append(tool_msg)
