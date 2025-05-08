# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/16 15:59 
@Author  : ZhangShenao 
@File    : video_understanding.py 
@Desc    : 视频理解
"""
import os
from typing import List

import dotenv
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE")
                )


def introduction(frames: List) -> str:
    """
    生成视频介绍
    :param frames: 视频帧列表
    :return: 视频内容介绍
    """

    # 使用GPT-4o模型,生成视频介绍
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "你是一位资深的内容编辑。请以Markdown格式，生成视频的介绍。"},
            {"role": "user", "content": [
                "下面是视频的图像帧",
                *map(lambda x: {"type": "image_url",
                                "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}},
                     frames)
            ]},
        ],
        temperature=0,
    )
    return response.choices[0].message.content
