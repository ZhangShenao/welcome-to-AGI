# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/8 16:51 
@Author  : ZhangShenao 
@File    : indexing.py 
@Desc    : Indexing索引模块

Indexing索引模块
核心功能: 加载原始问答文档,进行解析和切割,经过Embedding处理后,存储到向量数据库中,用于构建索引
"""
import os

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

from embedding import EMBEDDING

# 向量存储路径
VECTOR_STORE_DIR = "./data/vector_store"


def indexing() -> None:
    """索引过程"""

    # 校验索引数据是否已存在
    if os.path.exists(VECTOR_STORE_DIR):
        print("索引数据已存在,跳过索引过程")
        return

    # 加载原始文档内容
    with open("./data/sales_data.txt", "r") as f:
        docs = f.read()

    # 创建文本分割器,将原始文档内容进行切割
    splitter = CharacterTextSplitter(
        separator=r"\d+\.\n",  # 按照正则表达式进行切割
        is_separator_regex=True,
        chunk_size=100,  # 每个chunk的最大长度为100
        chunk_overlap=0,  # 每个chunk间无关联,overlap为0
        length_function=len  # 使用默认的length函数计算长度
    )
    chunks = splitter.create_documents([docs])
    print(f"原始文档切割完成,共{len(chunks)}个chunk")

    # 创建Faiss向量数据库
    # 将chunk进行embedding处理后,存储到向量数据库中
    vector_store = FAISS.from_documents(chunks, EMBEDDING)

    # 将数据保存到本地磁盘
    vector_store.save_local(VECTOR_STORE_DIR)

    print("Indexing执行完成")
