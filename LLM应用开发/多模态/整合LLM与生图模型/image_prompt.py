# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/15 16:56 
@Author  : ZhangShenao 
@File    : image_prompt.py 
@Desc    : 使用Claude模型,生成生图Prompt
"""
import re

from openai import OpenAI

# 定义生图Prompt
image_prompt = """你是一个乐于助人的AI助手。这次对话的一个特点是你可以访问图像生成API,所以如果用户要求你创建图像,或者你有一个特别相关或深刻的图像创意,你就可以创建图像。
                   请写'<img_prompt>(提示词)</img_prompt>',将提示词替换为你想要创建的图像描述。

为获得尽可能好的图像,请遵循以下5条原则:

1. 简洁明了:使用简洁、具体的词语描述图像,避免抽象或模棱两可的表达。
2. 丰富细节:在不影响简洁性的前提下,适度添加细节,使图像更生动、更有说服力。
3. 合理构图:考虑图像的整体构图,如主体、背景、色彩搭配等,力求协调、平衡。
4. 情感表达:根据图像的主题和目的,适当加入情感元素,以引发共鸣、思考或美感体验。
5. 创新独特:鼓励创新和独特的表现方式,避免陈词滥调,努力创造令人眼前一亮的视觉效果。

例如,如果我问"爱因斯坦是如何提出相对论的?",你可以这样生成一个图像:

<img_prompt>年轻的爱因斯坦坐在书桌前,周围散落着满是计算和公式的纸张,他全神贯注地凝视前方,仿佛在思考宇宙的奥秘。房间里光线昏暗,只有一束光照亮了他的侧脸,突出了他专注、智慧的神情。</img_prompt>

"""


def gen_image_prompt(query: str, client: OpenAI) -> str:
    """
    生成生图的Prompt
    :param query: 用户提问
    :param client: OpenAI 客户端
    :return: 生图Prompt
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": image_prompt},
            {"role": "user", "content": query}
        ],
    )
    content = resp.choices[0].message.content

    # 解析响应结果
    matched = re.search(r'<img_prompt>(.*?)</img_prompt>', content)
    if matched is not None:
        result = matched.group(1)
    else:
        result = content

    # 将中文Prompt翻译成英文
    return translate_prompt(result, client)


def translate_prompt(chinese_prompt: str, client: OpenAI) -> str:
    """
    将中文的prompt翻译成英文
    :param chinese_prompt: 中文Prompt
    :param client: OpenAI 客户端
    :return: 翻译后的英文Prompt
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": f"Translate the following Chinese text to English: {chinese_prompt}"}
        ]
    )
    translation = response.choices[0].message.content
    return translation.strip()
