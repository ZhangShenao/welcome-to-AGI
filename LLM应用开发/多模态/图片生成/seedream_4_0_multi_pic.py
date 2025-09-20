# 使用豆包Seedream 4.0模型，将4张图片按照2x2的四宫格样式，拼接在一起，保证每张图片的完整性。
# -*- coding: utf-8 -*-
"""
@Time    : 2025/9/18 10:00
@Author  : ZhangShenao
@File    : seedream_4_0_multi_pic.py
@Desc    : 使用豆包Seedream 4.0模型，将4张图片按照2x2的四宫格样式，拼接在一起，保证每张图片的完整性。
"""
import os

# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions

import dotenv

# 加载环境变量
dotenv.load_dotenv()

# 创建Ark客户端
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url=os.getenv("ARK_API_BASE"),
    api_key=os.getenv("ARK_API_KEY"),
)

# 四宫格拼接图片
imagesResponse = client.images.generate(
    model="doubao-seedream-4-0-250828",
    prompt="将这4张参考图，按照合理的布局，合并成一张2x2的四宫格图片，保证每张图片的完整性。",
    image=[
        os.getenv("IMAGE_URL_1", "https://example.com/image1.jpg"),
        os.getenv("IMAGE_URL_2", "https://example.com/image2.jpg"),
    ],
    size="2K",
    sequential_image_generation="auto",
    sequential_image_generation_options=SequentialImageGenerationOptions(max_images=1),
    response_format="url",
    watermark=False,
)

# 遍历所有图片数据
for image in imagesResponse.data:
    # 输出当前图片的url和size
    print(f"URL: {image.url}, Size: {image.size}")