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
    prompt="把这4张图按照2x2的四宫格样式，拼接在一起，保证每张图片的完整性。",
    image=[
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png",
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png",
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png",
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png",
    ],
    size="2K",
    sequential_image_generation="auto",
    sequential_image_generation_options=SequentialImageGenerationOptions(max_images=3),
    response_format="url",
    watermark=True,
)

# 遍历所有图片数据
for image in imagesResponse.data:
    # 输出当前图片的url和size
    print(f"URL: {image.url}, Size: {image.size}")
