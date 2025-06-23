# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 16:00 
@Author  : ZhangShenao 
@File    : condition_node.py 
@Desc    : 条件节点
"""
from typing import Literal

from langgraph.graph import MessagesState


def condition_node(state: MessagesState) -> Literal["environment", "END"]:
    """条件节点: 根据当前状态,决定Agent是继续迭代,还是结束执行"""

    # 获取最后一条消息
    last_msg = state["messages"][-1]

    # 如果最后一条消息是工具调用消息,则需要继续迭代
    # 否则终止执行
    if len(last_msg.tool_calls) > 0:
        return "environment"

    return "END"
