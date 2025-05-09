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

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


def get_embedding_model() -> Embeddings:
    """
    获取Embedding模型
    """

    # 使用OpenAI Embedding
    return OpenAIEmbeddings(
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )
