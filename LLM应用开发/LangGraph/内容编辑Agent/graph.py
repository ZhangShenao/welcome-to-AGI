# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:46 
@Author  : ZhangShenao 
@File    : graph.py 
@Desc    : 构造Graph并执行
"""
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from content_node import content_node
from image_node import image_node
from state import ArticleState
from summary_node import summary_node
from title_node import title_node


def write_article(topic: str) -> ArticleState:
    """
    撰写文章
    :param topic: 文章主题
    :return: 最终生成的文章状态
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

    # 编译生成图
    graph = sg.compile()

    # 设置初始状态
    init_state = ArticleState(
        topic=topic,
        title="",
        content="",
        summary="",
        image_path="",
    )

    # 执行Graph,返回生成的最终状态
    return graph.invoke(init_state)


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


if __name__ == '__main__':
    final_state = write_article("大模型底层的Transformer架构")
    dump_markdown(final_state)
