# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/9 10:05 
@Author  : ZhangShenao 
@File    : retrieving.py 
@Desc    : Retrieving检索模块

Retrieving检索模块
核心功能: 根据用户的提问,去向量数据库中进行相似性检索,获取检索结果
"""
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from embedding import get_embedding_model
from indexing import VECTOR_STORE_DIR


def retrieving(query: str, top_k: int = 3, score_threshold: float = 0.6) -> List[Document]:
    """
    检索过程
    :param query: 用户提问
    :param top_k: 检索相关文档的数量，默认为3
    :param score_threshold: 相似度分数阈值，默认为0.6
    :return: 检索到的相关文档
    """
    # 加载向量数据库
    vector_store = FAISS.load_local(VECTOR_STORE_DIR,
                                    get_embedding_model(),
                                    allow_dangerous_deserialization=True
                                    )

    # 执行相似度检索
    return vector_store.similarity_search(query, k=top_k, kwargs={"score_threshold": score_threshold})
