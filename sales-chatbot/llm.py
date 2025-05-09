# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/9 10:23 
@Author  : ZhangShenao 
@File    : llm.py 
@Desc    : LLM大模型模块
"""
import os

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_chat_model() -> BaseChatModel:
    """
    获取聊天模型
    :return: 聊天模型
    """

    # 使用OpenAI的gpt-4o-mini模型
    return ChatOpenAI(
        model="gpt-4o-mini",
        base_url=os.getenv("OPENAI_API_BASE"),
        temperature=0.1
    )
