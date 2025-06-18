# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:33 
@Author  : ZhangShenao 
@File    : main_node.py 
@Desc    : Main函数代码节点
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, MAIN_FUNCTION_PROMPT
from state import CodeState


def main_node(state: CodeState) -> CodeState:
    """
    Main函数节点
    :param state: 当前状态
    :return: 更新后的状态
    """

    # 获取已经生成的Router代码
    routers = state["routers"]

    # 构造Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", MAIN_FUNCTION_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用chain,生成main函数
    main_function = chain.invoke({"routers": routers})

    # 更新状态
    state["main_function"] += main_function

    # 返回更新后的状态
    return state
