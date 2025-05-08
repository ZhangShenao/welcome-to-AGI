# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/8 17:13 
@Author  : ZhangShenao 
@File    : embedding.py
@Desc    : Embedding嵌入模块

Embedding嵌入模块
核心功能: 将高维的原始数据(文本、图片、视频等)转化成低维的向量表示
"""
import os

import dotenv
from langchain_openai import OpenAIEmbeddings

# 使用OpenAI Embedding
dotenv.load_dotenv()
EMBEDDING = OpenAIEmbeddings(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)
