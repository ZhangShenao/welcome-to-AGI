# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:04 
@Author  : ZhangShenao 
@File    : state.py 
@Desc    : 状态定义
"""
from typing_extensions import TypedDict


class CodeState(TypedDict):
    models: list[str]  # models实体类定义
    routers: list[str]  # 路由定义
    handlers: list[str]  # 处理器定义
    main_function: str  # main函数
