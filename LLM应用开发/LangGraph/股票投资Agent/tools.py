# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 15:11 
@Author  : ZhangShenao 
@File    : tools.py 
@Desc    : 工具定义

pip install akshare --upgrade

AKShare API文档
https://akshare.akfamily.xyz/data/stock/stock.html#id11
"""

import akshare as ak
from langchain_core.tools import tool


# 定义股票信息查询工具
@tool
def get_stock_info(code: str = "", name: str = "") -> str:
    """可以根据传入的股票代码或股票名称获取股票信息
    Args:
        code: 股票代码
        name: 股票名称
    """

    empty_code = (code == "" or len(code) <= 2)
    empty_name = (name == "" or len(name) <= 2)

    if empty_code and empty_name:
        return "未查询到相关股票信息"

    # 调用AKShare API,获取创业板股票列表
    # 返回DataFrame数据结构
    df = ak.stock_cy_a_spot_em()

    # 基于DataFrame数据结构进行过滤
    if empty_code and not empty_name:  # 根据股票名称查询
        result = df[df["名称"].str.contains(name)]
    elif not empty_code and empty_name:  # 根据股票代码查询
        result = df[df["代码"].str.contains(code)]
    else:  # 同时根据股票代码和股票名称查询
        result = df[df["代码"].str.contains(code) & df["名称"].str.contains(name)]

    # 返回股票信息
    return str(result.to_dict(orient="records"))


# 定义工具列表
TOOLS = [get_stock_info]
TOOL_DICT = {tool.name: tool for tool in TOOLS}
