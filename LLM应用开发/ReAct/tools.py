# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/23 11:09 
@Author  : ZhangShenao 
@File    : tools.py
@Desc    : 工具定义
"""

import json
import os

import requests


def search(query: str) -> str:
    """
    搜索
    :param query: 搜索关键词
    :return: 搜索结果
    """

    # 构造请求参数
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
    })
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),  # 申请api_key: https://serper.dev/api-key
        'Content-Type': 'application/json'
    }

    # 发送请求
    response = requests.request("POST", url, headers=headers, data=payload).json()

    # 解析响应结果
    if response['organic'][0]:
        return response['organic'][0]['snippet']

    return "没有搜索到相关结果"


def calculate(expression: str) -> float:
    """
    计算
    :param expression: 运算表达式
    :return: 计算结果
    """

    # 使用Python内置的eval函数进行表达式计算
    return eval(expression)
