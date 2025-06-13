# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/12 20:19 
@Author  : ZhangShenao 
@File    : put_elephant.py
@Desc    : LangGraph实战——把大象装进冰箱
"""
from IPython.display import Image, display
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict


# 1. 定义状态
class ElephantInFridgeState(TypedDict):
    """
    定义状态——大象在冰箱中
    状态内的参数可以在多个节点间保存和流转
    """

    fridge_open: bool  # 冰箱门是否打开
    elephant_inside: bool  # 大象是否在冰箱内


# 2. 定义每个步骤的处理节点

def open_fridge(state: ElephantInFridgeState) -> ElephantInFridgeState:
    """第一步: 把冰箱门打开"""

    print("正在打开冰箱门...")

    # 执行当前节点业务逻辑
    print("冰箱门已打开！")

    # 更新状态
    state["fridge_open"] = True

    # 当前节点处理完成,更新状态
    return state


def put_elephant(state: ElephantInFridgeState) -> ElephantInFridgeState:
    """第二步: 把大象放进去"""

    # 获取当前状态
    if not state["fridge_open"]:
        raise ValueError("冰箱门未打开，无法放入大象！")

    # 执行当前节点业务逻辑
    print("正在把大象放入冰箱...")
    print("大象已放入冰箱！")

    # 更新状态
    state["elephant_inside"] = True

    # 当前节点处理完成,更新状态
    return state


def close_fridge(state: ElephantInFridgeState) -> ElephantInFridgeState:
    """第三步: 把冰箱门带上"""

    # 获取当前状态
    if not state["elephant_inside"]:
        print("警告：冰箱内没有大象，是否确认关闭？")

    # 执行当前节点业务逻辑
    print("正在关闭冰箱门...")
    print("冰箱门已关闭！")

    # 更新状态
    state["fridge_open"] = False

    # 当前节点处理完成,更新状态
    return state


# 3. 构建Graph工作流图
def build_graph() -> CompiledStateGraph:
    """构建"把大象装冰箱"的工作流程图"""

    # 创建图对象StateGraph
    graph = StateGraph(ElephantInFridgeState)

    # 添加节点Node
    graph.add_node("open_fridge", open_fridge)
    graph.add_node("put_elephant", put_elephant)
    graph.add_node("close_fridge", close_fridge)

    # 添加起始边
    graph.add_edge(START, "open_fridge")

    # 添加边Edge,将节点连接起来,形成工作流
    graph.add_edge("open_fridge", "put_elephant")
    graph.add_edge("put_elephant", "close_fridge")

    # 添加结束边
    graph.add_edge("close_fridge", END)

    # 返回编译好的图Graph
    return graph.compile()


# 4. 运行Graph工作流
def run_workflow():
    """运行"把大象装冰箱"的工作流"""

    # 构建图
    graph = build_graph()

    # 定义初始状态
    initial_state = ElephantInFridgeState(fridge_open=False, elephant_inside=False)

    # 运行图
    result = graph.invoke(initial_state)

    # 输出最终状态
    print("\n工作流执行完毕，最终状态:")
    print(f"冰箱门状态: {'打开' if result["fridge_open"] else '关闭'}")
    print(f"大象是否在冰箱内: {'是' if result["elephant_inside"] else '否'}")

    # 可视化工作流图
    display(Image(graph.get_graph().draw_mermaid_png()))

    return result


# 执行入口
if __name__ == "__main__":
    final_state = run_workflow()
