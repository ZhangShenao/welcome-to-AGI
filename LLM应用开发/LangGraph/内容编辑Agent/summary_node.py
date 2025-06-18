# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/18 14:33 
@Author  : ZhangShenao 
@File    : title_node.py 
@Desc    : 文章摘要节点
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, SUMMARY_PROMPT
from state import ArticleState


def summary_node(state: ArticleState) -> ArticleState:
    """
    文章摘要节点
    :param state: 当前文章状态
    :return: 处理后的文章状态
    """

    # 从当前状态中获取所需信息
    if not state["topic"]:
        raise ValueError("未指定文章主题！")
    if not state["title"]:
        raise ValueError("文章标题缺失！")
    if not state["content"]:
        raise ValueError("文章正文内容缺失！")

    topic = state["topic"]
    title = state["title"]
    content = state["content"]

    # 构造prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", SUMMARY_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 构造Chain
    chain = prompt | deepseek | StrOutputParser()

    # 调用Chain,获取结果
    summary = chain.invoke({"topic": topic, "title": title, "content": content})

    # 更新状态
    state["summary"] = summary
    print(f"文章摘要生成完成：共 {len(summary)} 字")

    # 返回处理后的状态
    return state
