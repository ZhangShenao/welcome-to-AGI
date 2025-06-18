# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:22 
@Author  : ZhangShenao 
@File    : router_node.py
@Desc    : Handler处理器节点
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, HANDLER_PROMPT
from state import CodeState


def handler_node(state: CodeState) -> CodeState:
    """
    Handler处理器节点
    :param state: 当前CodeState状态
    :return: 处理后的CodeState状态
    """

    # 从当前状态中获取models和routers信息
    models = state["models"]
    routers = state["routers"]

    # 构造prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", HANDLER_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用Chain,获取结果
    message = chain.invoke({"models": models, "routers": routers})

    # 更新状态
    state["handlers"] += [message]

    # 返回处理后的状态
    return state
