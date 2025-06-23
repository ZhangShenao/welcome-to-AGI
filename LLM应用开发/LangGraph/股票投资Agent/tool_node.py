# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 15:13 
@Author  : ZhangShenao 
@File    : tool_node.py 
@Desc    : 工具调用节点
"""
from langchain_core.messages import ToolMessage
from langgraph.graph import MessagesState

from tools import TOOL_DICT


def tool_node(state: MessagesState) -> MessagesState:
    """工具节点: 调用获取,获取结果"""

    # 遍历工具调用列表
    result = []
    tool_calls = state["messages"][-1].tool_calls
    
    for tool_call in tool_calls:
        # 根据名称,获取需要调用的工具
        tool_name = tool_call["name"]
        tool = TOOL_DICT[tool_name]

        if tool is not None:
            # 调用工具,获取结果
            tool_call_result = tool.invoke(tool_call["args"])

            # 保存工具调用消息
            tool_msg = ToolMessage(content=tool_call_result, tool_call_id=tool_call["id"])
            result.append(tool_msg)

    # 返回工具调用后的状态
    return {"messages": result}
