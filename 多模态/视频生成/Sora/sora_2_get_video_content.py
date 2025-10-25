# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/24 10:00
@Author  : ZhangShenao
@File    : sora_2_gen_video.py
@Desc    : 使用Sora 2生成视频
"""

import os


import dotenv

dotenv.load_dotenv()

from openai import OpenAI

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")
# )

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
video_id = "video_68fb135c32bc8191a483111e60e0360c0b6110960f30988b"
response = client.videos.download_content(video_id=video_id)
response.write_to_file(file="sora.mp4")
