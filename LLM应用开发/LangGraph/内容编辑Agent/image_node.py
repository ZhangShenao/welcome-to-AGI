# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/18 14:33 
@Author  : ZhangShenao 
@File    : title_node.py 
@Desc    : 文章插图节点
"""

import os

import dotenv
import requests
from openai import OpenAI

from state import ArticleState

# 加载环境变量
dotenv.load_dotenv()

# 创建豆包Seedream客户端
seedream = OpenAI(
    base_url=os.getenv("VOLCENGINE_API_BASE"),
    api_key=os.environ.get("VOLCENGINE_API_KEY"),
)


def image_node(state: ArticleState) -> ArticleState:
    """
    文章插图节点
    :param state: 当前文章状态
    :return: 处理后的文章状态
    """

    # 从当前状态中获取所需信息
    if not state["summary"]:
        raise ValueError("未生成文章摘要！")

    summary = state["summary"]

    # 使用豆包的Seedream模型生成图片
    response = seedream.images.generate(
        model="doubao-seedream-3-0-t2i-250415",
        prompt=summary,
        size="1024x1024",
        response_format="url"
    )
    if len(response.data) == 0:
        raise ValueError("生成图片失败！")
    print(f"文章插图生成成功！url: {response.data[0].url}")

    # 从url下载图片，并以png格式保存到本地
    image_path = f"./{state["title"]}.png"
    download_image(response.data[0].url, image_path)

    # 更新状态
    state["image_path"] = image_path
    print(f"文章插图生成完成，已保存至：{image_path} ")

    # 返回更新后的状态
    return state


def download_image(url: str, file_path: str) -> None:
    """
    下载图片
    :param url: 图片url
    :param file_path: 图片保存路径
    :return: None
    """

    # 下载图片
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
