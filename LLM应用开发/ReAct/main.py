# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/23 15:17 
@Author  : ZhangShenao 
@File    : main.py 
@Desc    : 执行入口
"""
import dotenv

from agent_executor import AgentExecutor
from react_agent import ReActAgent
from tools import search, calculate

if __name__ == '__main__':
    # 加载环境变量
    dotenv.load_dotenv()

    # 创建工具列表
    tools = {"search": search, "calculate": calculate, }

    # 创建ReAct Agent
    agent = ReActAgent()

    # 创建AgentExecutor执行器
    executor = AgentExecutor(agent=agent, tools=tools, max_epochs=10)

    # 执行
    result = executor.execute(goal="世界上第1高的山比第2高的山高多少米？")
    print(result)
