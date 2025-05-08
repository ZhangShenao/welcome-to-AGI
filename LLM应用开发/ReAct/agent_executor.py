# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/23 14:14 
@Author  : ZhangShenao 
@File    : agent_executor.py 
@Desc    : Agent执行器
"""
import re

from react_agent import ReActAgent

# 匹配Action的正则表达式
ACTION_REGEX = re.compile(r'^Action: (\w+): (.*)$')


class AgentExecutor:
    """Agent执行器"""

    def __init__(self, agent: ReActAgent, tools: dict[str, callable], max_epochs: int = 5):
        """
        构造函数
        :param agent: Agent
        :param tools: 可用的工具列表
        :param max_epochs: 最大执行轮数,防止死循环
        """

        self.agent = agent
        self.tools = tools
        self.max_epochs = max_epochs

    def execute(self, goal: str) -> str:
        """
         执行Agent
        :param goal: 执行目标
        :return: 返回执行结果
        """

        i = 0
        prompt = goal
        print(f"[执行目标] {goal}")

        # 循环执行Agent
        # ReAct的本质就是一个 Thought->Action->Observation 的循环
        while i < self.max_epochs:
            # 更新执行轮数
            i += 1
            print(f"[第{i}轮]")

            # 执行Agent
            result = self.agent(prompt=prompt)
            print(f"[中间结果] {result}")

            # 匹配需要调用的工具
            actions = [ACTION_REGEX.match(a) for a in result.split('\n') if ACTION_REGEX.match(a)]

            # 如果无需执行Action,则返回最终结果
            if len(actions) == 0:
                result = self.agent.result()
                print(f"[最终结果] {result}")
                return result

            # 解析Action及参数
            action, action_input = actions[0].groups()
            if action not in self.tools:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(f"[Execute Action]: {action} {action_input}")

            # 执行工具调用
            observation = self.tools[action](action_input)
            print(f"[Observation] {observation}")
            prompt = f"Observation: {observation}"

        return "超出最大轮数，终止执行"
