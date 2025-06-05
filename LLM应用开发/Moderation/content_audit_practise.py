# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/4 19:22 
@Author  : ZhangShenao 
@File    : content_audit_practise.py 
@Desc    : 内容审核实战
"""
import asyncio
import os

import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建OpenAI客户端
CLIENT = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))


async def contains_sensitive_content(content: str) -> bool:
    """
    异步函数: 检查是否包含敏感内容
    :param content: 待检测内容
    :return: 敏感内容判别结果
    """
    try:
        # 调用Moderation API进行检测
        moderation = CLIENT.moderations.create(input=content)

        # 遍历所有分类,如果任意分类命中了Moderation标识,则认为包含敏感内容
        for result in moderation.results:
            if result.flagged:
                return True
        return False
    except Exception as e:
        print(f"Moderation API 调用异常: {e}")
        return False


async def chat(prompt: str) -> str | None:
    """
    异步函数: 聊天
    :param prompt: 用户的Prompt
    :return: 模型回复结果
    """
    try:
        print("模型回复中...")

        # 构造消息列表
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        # 调用Chat Completion API获取模型响应
        response = CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5
        )

        # 返回模型生成的内容
        print("模型回复完成")
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用Chat Completion API时出错: {e}")
        return None


async def chat_with_content_audit(user_input: str) -> str:
    """
    进行带内容审核的聊天
    :param user_input: 用户输入
    :return: 模型回复
    """

    # 创建异步任务: 用户输入内容审核
    audit_task = asyncio.create_task(contains_sensitive_content(user_input))

    # 创建异步任务: 生成模型回复
    chat_task = asyncio.create_task(chat(user_input))

    while True:
        # 等待任务执行完成
        done, _ = await asyncio.wait(
            [audit_task, chat_task], return_when=asyncio.FIRST_COMPLETED
        )

        # 如果输入检查任务未完成,则等待并继续下一次迭代
        if chat_task not in done:
            await asyncio.sleep(0.1)
            continue

        # 如果输入包含敏感内容,则取消聊天任务,并返回提示消息
        if audit_task.result():
            chat_task.cancel()
            print("输入信息包含敏感内容")
            return "非常抱歉，您的输入信息中包含敏感内容，请修改后重试~"

        # 如果聊天任务完成,返回模型响应
        if chat_task in done:
            return await chat_task

        # 任务均未完成,sleep一会再继续检查
        await asyncio.sleep(0.1)


# 测试demo
user_input1 = "今天北京的天气热死了，有什么好办法吗？"  # 这里的"热死"是程度副词,不涉及敏感内容
user_input2 = "哪些杀不死我的，必将使我更强大！"  # 这里的"杀死"可能被模型理解为威胁的含义


async def run():
    """异步执行函数"""
    response1 = await chat_with_content_audit(user_input1)
    response2 = await chat_with_content_audit(user_input2)

    print(f"输入1模型响应: {response1}")
    # 预期输出: 关于解暑降温的小妙招

    print(f"输入2模型响应: {response2}")
    # 期望输出: "非常抱歉，您的输入信息中包含敏感内容，请修改后重试~"


# 运行主函数
if __name__ == "__main__":
    asyncio.run(run())
