# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/12 17:04 
@Author  : ZhangShenao 
@File    : langgraph_quickstart.py 
@Desc    : LangGraph快速入门

使用LangGraph的状态图,模拟烹饪过程

以烹饪牛排为例,完整流程如下:
1. 食材采购: 前往超市选购新鲜羊排
2. 方法查询: 查看菜谱,学习烹饪流程
3. 烹饪实施: 按照教程完成料理过程
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class CookingState(TypedDict):
    """
    自定义烹饪状态
    状态内的参数可以在多个节点间保存和流转
    """

    ingredients: str  # 原材料
    method: str  # 烹饪方法
    steps: list[str]  # 执行步骤


def supermarket(state: CookingState) -> CookingState:
    """定义supermarket节点"""

    print("[supermarket]节点执行")

    # 从State状态中获取当前节点所需的参数
    ingredients = state["ingredients"]
    last_steps = state["steps"]

    # 当前节点处理
    steps = last_steps + [f"从超市中买到了{ingredients}"]

    # 当前节点处理完成后,更新状态
    return {"ingredients": ingredients, "method": state["method"], "steps": steps}


def receipt(state: CookingState) -> CookingState:
    """定义receipt节点"""

    print("[receipt]节点执行")

    # 从State状态中获取当前节点所需的参数
    ingredients = state["ingredients"]
    last_steps = state["steps"]
    method = state["method"]

    # 当前节点处理
    steps = last_steps + [f"找到了菜谱: {method}{ingredients}"]

    # 当前节点处理完成后,更新状态
    return {"ingredients": ingredients, "method": method, "steps": steps}


def cooking(state: CookingState) -> CookingState:
    """定义cooking节点"""

    print("[cooking]节点执行")

    # 从State状态中获取当前节点所需的参数
    ingredients = state["ingredients"]
    last_steps = state["steps"]
    method = state["method"]

    # 当前节点处理
    steps = last_steps + [f"{method}{ingredients}烹饪完成"]

    # 当前节点处理完成后,更新状态
    return {"ingredients": ingredients, "method": method, "steps": steps}


if __name__ == "__main__":
    # 定义状态图
    sg = StateGraph(CookingState)

    # 创建节点
    sg.add_node("supermarket", supermarket)
    sg.add_node("receipt", receipt)
    sg.add_node("cooking", cooking)

    # 添加起始边
    sg.add_edge(START, "supermarket")

    # 添加普通边
    sg.add_edge("supermarket", "receipt")
    sg.add_edge("receipt", "cooking")

    # 添加结束边
    sg.add_edge("supermarket", END)

    # 编译StateGraph,得到状态图
    graph = sg.compile()

    # 定义初始状态
    init_state = CookingState(ingredients="牛排", method="", steps=[])

    #  调用状态图
    result = graph.invoke(init_state)

    print(result)
