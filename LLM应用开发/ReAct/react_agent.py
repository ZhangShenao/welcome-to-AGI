# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/23 13:43 
@Author  : ZhangShenao 
@File    : react_agent.py 
@Desc    : ReAct Agent
"""
import os

from openai import OpenAI

from prompt import REACT_PROMPT


class ReActAgent:
    """ReAct 智能体"""

    def __init__(self):
        """
        构造函数
        """

        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

        # 初始化消息列表
        # System Prompt设置为ReAct的Prompt
        self.messages = [{"role": "system", "content": REACT_PROMPT}]

    def __call__(self, prompt: str) -> str:
        """
        执行
        (__call__是Python的魔法函数,可以使得类的实例向函数一样被调用)
        :param prompt: 最新的Prompt
        :return: 执行结果
        """

        # 保存消息列表
        self.messages.append({"role": "user", "content": prompt})

        # 调用模型,生成结果
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.1,
        )
        content = resp.choices[0].message.content

        # 保存结果
        self.messages.append({"role": "assistant", "content": content})

        # 返回结果
        return content

    def result(self) -> str:
        """
        返回最终执行结果
        :return: 最终执行结果
        """
        return self.messages[-1]["content"]
