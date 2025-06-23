# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:46 
@Author  : ZhangShenao 
@File    : article_agent.py
@Desc    : 内容编辑Agent
"""

from IPython.display import Image, display
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from content_node import content_node
from image_node import image_node
from state import ArticleState
from summary_node import summary_node
from title_node import title_node


def build_agent() -> CompiledStateGraph:
    """
    构造Agent
    :return: 编译好的Agent Graph
    """

    # 创建StateGraph图结构
    sg = StateGraph(ArticleState)

    #  添加节点
    sg.add_node("title_node", title_node)
    sg.add_node("content_node", content_node)
    sg.add_node("summary_node", summary_node)
    sg.add_node("image_node", image_node)

    # 添加边
    sg.add_edge(START, "title_node")
    sg.add_edge("title_node", "content_node")
    sg.add_edge("content_node", "summary_node")
    sg.add_edge("summary_node", "image_node")
    sg.add_edge("image_node", END)

    # 编译Graph并返回
    graph = sg.compile()
    return graph


def write_article(agent: CompiledStateGraph, topic: str) -> ArticleState:
    """
    撰写文章
    :param agent: 内容编辑Agent
    :param topic: 文章主题
    :return: 最终生成的文章状态
    """

    # 设置初始状态
    init_state = ArticleState(
        topic=topic,
        title="",
        content="",
        summary="",
        image_path="",
    )

    # 执行Graph,返回生成的最终状态
    return agent.invoke(init_state)


def dump_markdown(state: ArticleState) -> None:
    """
    将文章以Markdown格式保存到本地
    :param state: 最终状态
    :return: None
    """

    title = state["title"]
    with open(f"./{title}.md", "w") as f:
        # 写入标题
        f.write(f"# {state["title"]}\n\n")

        # 写入正文
        f.write(f"{state["content"]}\n\n")

        # 在末尾插入图片
        f.write(f"![{title}]({state["image_path"]})\n\n")

    print(f"文章已保存至：{title}.md")


def show_agent_structure(agent: CompiledStateGraph) -> None:
    """展示Agent 结构"""
    display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    # 保存流程图到文件
    graph_png = agent.get_graph(xray=True).draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(graph_png)


if __name__ == '__main__':
    # 构造Agent
    agent = build_agent()

    # 展示Agent结构图
    # show_agent_structure(agent)

    # 写文章
    final_state = write_article(agent=agent, topic="中国苏超联赛持续火爆")

    # 将文章导出为markdown格式
    dump_markdown(final_state)
