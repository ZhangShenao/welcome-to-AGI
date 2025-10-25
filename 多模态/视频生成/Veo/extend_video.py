# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : extend_video.py
@Desc    : 扩展(延长)视频
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
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 设置第一段视频的提示词
prompt1 = "这只小猫睁开眼睛，打了个哈欠，伸了个懒腰，然后跳下沙发，走到猫抓板前，用力地磨了几下爪子。"

# 设置参考图片
ref_pic = types.VideoGenerationReferenceImage(
    image=Image.from_file(location="./cat.png"),
    reference_type="asset",
)

# 基于参考图片,生成第一段视频
print("开始生成第一段视频...")
operation1 = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt1,
    config=types.GenerateVideosConfig(
        resolution="720p",
        duration_seconds=8,
        reference_images=[ref_pic],
    ),
)

# 轮询生成状态,直到视频生成完成
while not operation1.done:
    print("Waiting for video generation to complete...")
    time.sleep(1)
    operation1 = client.operations.get(operation1)

# 获取第一段视频
video1 = operation1.response.generated_videos[0]
client.files.download(file=video1.video)
video1.video.save("cat_1.mp4")
print("第一段视频生成完成！")

# 设置第二段视频的提示词
prompt2 = (
    "磨完了爪子，小猫漫步走到窗前，看见窗外树枝上有一只小麻雀，他冲着麻雀喵喵叫了起来。"
)

print("开始生成最终视频...")
operation2 = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    video=video1.video,
    prompt=prompt2,
    config=types.GenerateVideosConfig(number_of_videos=1, resolution="720p"),
)

while not operation2.done:
    print("Waiting for video generation to complete...")
    time.sleep(1)
    operation2 = client.operations.get(operation2)

# 获取第二段视频
video2 = operation2.response.generated_videos[0]
client.files.download(file=video2.video)
video2.video.save("cat.mp4")
print("视频生成完成！")
