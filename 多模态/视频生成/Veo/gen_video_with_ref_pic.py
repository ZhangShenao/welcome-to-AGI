# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : gen_video_with_ref_pic.py
@Desc    : 使用参考图片生成视频
"""

import time
from google import genai
from google.genai import types

import dotenv

import os
from google.genai.types import Image

# 加载环境变量
dotenv.load_dotenv()


# 创建VEO客户端
# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(base_url=os.getenv("GOOGLE_API_BASE")),
# )

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = (
    "这只小猫睡醒了，它睁开眼睛，伸了个懒腰，然后跳下沙发，走到窗前，看着外面的世界。"
)

# 设置参考图片
ref_pic = types.VideoGenerationReferenceImage(
    image=Image.from_file(location="./cat.png"),
    reference_type="asset",
)

# 基于参考图片生成视频
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        resolution="1080p",
        duration_seconds=8,
        aspect_ratio="16:9",
        reference_images=[ref_pic],
    ),
)

# 轮询生成状态,直到视频生成完成
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(1)
    operation = client.operations.get(operation)

# 下载生成视频
# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("cat.mp4")

print("视频生成完成！")
