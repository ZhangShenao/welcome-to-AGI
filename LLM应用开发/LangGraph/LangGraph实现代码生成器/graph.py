# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:46 
@Author  : ZhangShenao 
@File    : graph.py 
@Desc    : 构造Graph并执行
"""
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from handler_node import handler_node
from main_node import main_node
from model_node import model_node
from router_node import router_node
from state import CodeState

if __name__ == '__main__':
    # 创建StateGraph图结构
    sg = StateGraph(CodeState)

    #  添加节点
    sg.add_node("model_node", model_node)
    sg.add_node("router_node", router_node)
    sg.add_node("handler_node", handler_node)
    sg.add_node("main_node", main_node)

    # 添加边
    sg.add_edge(START, "model_node")
    sg.add_edge("model_node", "router_node")
    sg.add_edge("router_node", "handler_node")
    sg.add_edge("handler_node", "main_node")
    sg.add_edge("main_node", END)

    # 编译生成图
    graph = sg.compile()

    # 设置初始状态
    init_state = CodeState(
        models=[],
        handlers=[],
        main_function="",
        routers=[]
    )

    # 执行Graph,获取结果
    generated_code = graph.invoke(init_state)

    # 打印生成的代码
    # 将generated_code中的内容保存到文件中
    with open("./models.go", "w") as f:
        f.write(generated_code["models"][0])
    print("成功生成Models代码，已保存到 models.go 文件中！")

    with open("./main.go", "w") as f:
        f.write(generated_code["main_function"])
        f.write("\n")
        for handler in generated_code["handlers"]:
            f.write(handler)

    print("成功生成main代码，已保存到 main.go 文件中！")
