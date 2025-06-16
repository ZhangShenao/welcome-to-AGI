# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:22 
@Author  : ZhangShenao 
@File    : router_node.py
@Desc    : Router路由节点
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, ROUTER_PROMPT
from state import CodeState


def router_node(state: CodeState) -> CodeState:
    """
    Router路由节点
    :param state: 当前CodeState状态
    :return: 处理后的CodeState状态
    """

    # 构造prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", ROUTER_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用Chain,获取结果
    message = chain.invoke({})

    # 更新状态
    state["routers"] += [message]

    # 返回处理后的状态
    return state
