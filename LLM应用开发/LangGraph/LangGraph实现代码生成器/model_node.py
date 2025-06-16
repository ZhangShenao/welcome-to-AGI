# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 16:04 
@Author  : ZhangShenao 
@File    : model_node.py 
@Desc    : Model实体类节点
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, MODEL_PROMPT
from state import CodeState


def model_node(state: CodeState) -> CodeState:
    """
    Model实体类节点
    :param state: 当前状态
    :return: 更新后的状态
    """

    # 构造Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", MODEL_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用chain,生成main函数
    message = chain.invoke({})

    # 更新状态
    state["models"] += [message]

    # 返回更新后的状态
    return state
