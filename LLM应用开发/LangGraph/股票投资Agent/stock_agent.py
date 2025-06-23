# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/20 16:05 
@Author  : ZhangShenao 
@File    : stock_agent.py
@Desc    : 股票Agent执行入口
"""
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph

from condition_node import condition_node
from llm_node import llm_node
from tool_node import tool_node


def build_agent() -> CompiledStateGraph:
    """构建Agent"""

    # 创建StateGraph状态图
    agent_builder = StateGraph(MessagesState)

    # 添加节点
    agent_builder.add_node("llm_node", llm_node)
    agent_builder.add_node("environment", tool_node)

    # 添加普通边
    agent_builder.add_edge(START, "llm_node")

    # 添加条件边
    agent_builder.add_conditional_edges(
        "llm_node",
        condition_node,
        {
            # 条件返回结果 : 下一节点名称
            "environment": "environment",
            "END": END,
        },
    )

    # 添加普通边
    agent_builder.add_edge("environment", "llm_node")

    # 编译状态图,并返回
    agent = agent_builder.compile()
    return agent


def show_agent_structure(agent: CompiledStateGraph) -> None:
    """展示Agent 结构"""
    display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    # 保存流程图到文件
    graph_png = agent.get_graph(xray=True).draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(graph_png)


def run_stock_agent(agent: CompiledStateGraph, query: str) -> None:
    """运行股票Agent"""

    # 设置初始状态
    messages = [HumanMessage(content=query)]

    # 执行Agent,获取结果
    messages = agent.invoke({"messages": messages})

    # 打印执行结果
    for message in messages["messages"]:
        message.pretty_print()


if __name__ == '__main__':
    # 创建Agent
    agent = build_agent()

    # show_agent_structure(agent)

    # 执行Agent
    run_stock_agent(agent, "帮我看下宁德时代的股票行情")
