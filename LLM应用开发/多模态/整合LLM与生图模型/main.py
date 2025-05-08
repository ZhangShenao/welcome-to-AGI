# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/15 18:34 
@Author  : ZhangShenao 
@File    : main.py 
@Desc    : 入口函数
"""

import os

import dotenv
from openai import OpenAI

from generate_image import generate_image_by_sd, display_image
from image_prompt import gen_image_prompt

if __name__ == '__main__':
    # 加载环境变量
    dotenv.load_dotenv()

    # 创建OpenAI客户端
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    # 生成图片Prompt
    image_prompt = gen_image_prompt(query="图灵是如何为现代计算机奠定基础的?", client=client)
    print(f"图片Prompt: \n{image_prompt}")

    # 生成图片
    sd_image_url = generate_image_by_sd(prompt=image_prompt)
    print(f"Stable Diffusion 生成图片结果: \n{sd_image_url}")
    display_image(sd_image_url)
    #
    # dalle_image_url = generate_image_by_dalle(prompt=image_prompt,
    #                                           client=client,
    #                                           height=1024,
    #                                           width=1024)
    # print(f"Dall-E 生成图片结果: \n{dalle_image_url}")
    # display_image(dalle_image_url)
