# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/22 18:33 
@Author  : ZhangShenao 
@File    : 2.Pipeline智能问答.py 
@Desc    : 使用Pipeline API,实战智能问答
"""

from transformers import pipeline  # 导入Transforms Pipeline API

# 创建Pipeline
# 任务类型为question-answering问答
# 不指定模型,默认使用distilbert/distilbert-base-cased-distilled-squad(不推荐)
qa = pipeline(task="question-answering")

# 进行智能问答
answer = qa(
    question="What is the capital of China?",  # 设置问题
    context="On 1 October 1949,CCP Chairman Mao Zedong formally proclaimed the People's Republic of China in "
            "Tiananmen Square,Beijing.",  # 设置上下文
)

# 打印结果
print(f"score: {answer["score"]:.2f}")
print(f"answer: {answer["answer"]}")
print(f"start: {answer["start"]}")
print(f"end: {answer["end"]}")

# score: 0.95
# answer: Beijing
# start: 113
# end: 120
