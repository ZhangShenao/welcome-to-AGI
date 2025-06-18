# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 16:04 
@Author  : ZhangShenao 
@File    : model_node.py 
@Desc    : Model实体类节点
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from deepseek import get_deepseek
from prompt import SYSTEM_PROMPT, MODEL_PROMPT
from state import CodeState


@tool  # 使用LangChain的@tools 装饰器,将函数封装成一个Tool工具
def model_tool(model_name: str) -> str:
    """
    该工具用于生成Go语言的实体类代码
    :param model_name: 实体类名称
    :return: 最终生成的实体类代码
    """

    print("调用工具: model_tool")
    model_name = model_name.lower()

    # Mock UserModel实体类
    if "user" or "用户" in model_name:
        return """
type UserModel struct {
    UserID int64 `json:"user_id"`
    UserName string `json:"user_name"`
    UserEmail string `json:"user_email"`
}        
"""
    return ""


# 定义工具列表
tools = [model_tool]
tool_map = {tool.name: tool for tool in tools}


def model_node(state: CodeState) -> CodeState:
    """
    Model实体类节点
    :param state: 当前状态
    :return: 更新后的状态
    """

    # 构造Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", MODEL_PROMPT)
    ])

    # 获取DeepSeek客户端
    deepseek = get_deepseek()

    # 绑定工具,进行Function Calling
    deepseek = deepseek.bind_tools(tools)

    # 构造Chain
    chain = prompt | deepseek

    # 调用chain,生成main函数
    message = chain.invoke({})

    # 解析工具调用信息
    for tool_call in message.tool_calls:
        tool_name = tool_call["name"]
        tool = tool_map[tool_name]
        if tool is not None:
            # 调用工具,获取结果
            tool_args = tool_call["args"]
            tool_call_result = tool.invoke(tool_args)

            # 更新状态
            state["models"].append(tool_call_result)

    # 返回更新后的状态
    return state
