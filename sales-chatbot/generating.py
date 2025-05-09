# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/9 10:16 
@Author  : ZhangShenao 
@File    : generating.py 
@Desc    : Generating生成模块

Generating生成模块
核心功能: 接收用户提问，基于检索到的相关文档，生成最终的回答
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm import get_chat_model
from retrieving import retrieving

# RAG的Prompt模板
SYSTEM_PROMPT = """你是一位资深的房产销售经理。请根据检索到的上下文信息，回答用户关于房屋情况的问题。
        如果你不知道答案，就说:"这个问题建议直接咨询人工客服哦~"。
        最多使用三句话，保持答案简洁，语气要有亲和力。\n
        以下是相关的上下文信息：
        {context}
        """


def generate(query: str, top_k: int = 3, score_threshold: float = 0.6) -> str:
    """
    生成最终的回答
    :param query: 用户提问
    :param top_k: 检索相关文档的数量，默认为3
    :param score_threshold: 相似度分数阈值，默认为0.6
    :return: 生成的回答
    """

    # 检索相关文档
    relevant_docs = retrieving(query=query, top_k=top_k, score_threshold=score_threshold)

    # 构造Context上下文
    context = ""
    for i in range(len(relevant_docs)):
        context += f"{i + 1}. {relevant_docs[i].page_content}\n"

    # 构造Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", query)
    ])
    prompt = prompt.partial(context=context)

    # 获取LLM
    llm = get_chat_model()

    # 构造Chain
    chain = prompt | llm | StrOutputParser()

    # 执行Chain,获取结果
    return chain.invoke({"query": query})
