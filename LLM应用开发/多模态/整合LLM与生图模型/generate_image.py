# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/15 18:31 
@Author  : ZhangShenao 
@File    : generate_image.py 
@Desc    : 生成图片
"""
import os
from io import BytesIO

import dotenv
import requests
from PIL import Image
from openai import OpenAI

# 加载环境变量
dotenv.load_dotenv()

# 创建OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)


def generate_image_by_dalle(prompt: str, client: OpenAI, height: int = 1024, width: int = 1024, ) -> str:
    """
    通过OpenAI Dall-E模型生成图片
    :param prompt: 生图Prompt
    :param client: OpenAI 客户端
    :param height: 图片高度,默认为1024
    :param width: 图片宽度,默认为1024
    :return: 生成图片的url
    """

    # 调用Dall-E-3模型,生成图片
    resp = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=f"{height}x{width}",
        quality="standard",
        n=1,
    )

    # 返回图片url
    return resp.data[0].url


def generate_image_by_sd(prompt, height=1024, width=1024):
    """
     通过Stable Diffusion模型生成图片
    :param prompt: 生图Prompt
    :param height: 图片高度,默认为1024
    :param width: 图片宽度,默认为1024
    """
    engine_id = "stable-diffusion-v1-6"
    api_host = 'https://api.stability.ai'

    # 发送 POST 请求生成图像
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv("SD_API_KEY")}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt,  # 使用传入的提示词
                }
            ],
            "cfg_scale": 7,  # 配置比例，影响生成图像的多样性
            "height": height,  # 图像高度
            "width": width,  # 图像宽度
            "samples": 1,  # 生成图像的数量
            "steps": 30,  # 生成图像的步数
        },
    )

    # 检查响应状态码，如果不是 200，抛出异常
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # 解析 JSON 响应数据
    data = response.json()
    return data['artifacts'][0]['base64']  # 返回生成的图像的 base64 编码


def display_image(image_url: str):
    """
    展示图片
    :param image_url: 图片url
    """
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image.show()


generate_image_by_sd(prompt="图灵是如何为现代计算机奠定基础的?")
