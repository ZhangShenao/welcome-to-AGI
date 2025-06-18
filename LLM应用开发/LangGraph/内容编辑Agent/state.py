# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:04 
@Author  : ZhangShenao 
@File    : state.py 
@Desc    : 文章状态定义
"""
from typing_extensions import TypedDict


class ArticleState(TypedDict):
    """文章状态"""

    topic: str  # 主题
    title: str  # 标题
    content: str  # 正文
    summary: str  # 摘要
    image_path: str  # 插图路径
