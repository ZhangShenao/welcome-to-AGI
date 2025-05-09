# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/9 10:27 
@Author  : ZhangShenao 
@File    : chatbot.py 
@Desc    : 聊天机器人执行程序
"""
import dotenv

from generating import generate

if __name__ == '__main__':
    # 加载环境变量
    dotenv.load_dotenv()

    # 获取用户提问
    query = "这个小区是在哪座城市？"

    # 执行RAG过程
    result = generate(query=query, top_k=3, score_threshold=0.8)
    print(result)
