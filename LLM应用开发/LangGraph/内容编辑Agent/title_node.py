# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/18 14:33 
@Author  : ZhangShenao 
@File    : title_node.py 
@Desc    : 文章标题节点
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, TITLE_PROMPT
from state import ArticleState


def title_node(state: ArticleState) -> ArticleState:
    """
    文章标题节点
    :param state: 当前文章状态
    :return: 处理后的文章状态
    """

    # 从当前状态中获取所需信息
    if not state["topic"]:
        raise ValueError("未指定文章主题！")
    topic = state["topic"]

    # 构造prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", TITLE_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用Chain,获取结果
    title = chain.invoke({"topic": topic})

    # 更新状态
    state["title"] = title
    print(f"文章标题生成完成：{title}")

    # 返回处理后的状态
    return state
