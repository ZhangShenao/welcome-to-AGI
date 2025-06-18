# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 14:28
@Author  : ZhangShenao
@File    : deepseek.py
@Desc    : 获取DeepSeek客户端
"""

import os

import dotenv
from langchain_openai import ChatOpenAI

# 加载环境变量
dotenv.load_dotenv()


def get_deepseek() -> ChatOpenAI:
    """
    获取DeepSeek客户端
    :return: DeepSeek客户端
    """
    return ChatOpenAI(
        model="deepseek-chat",  # 使用DeepSeek-V3 Chat Model
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE"),
    )
