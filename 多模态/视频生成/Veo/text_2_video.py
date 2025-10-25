# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : text_2_video.py
@Desc    : 根据文本生成视频
"""

import time
from google import genai
from google.genai import types

import dotenv

import os

# 加载环境变量
dotenv.load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(base_url=os.getenv("GOOGLE_API_BASE")),
# )

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
# A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

prompt = "Elon Musk is sitting in a chair, smoking"

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        resolution="720p",
        duration_seconds=8,
        aspect_ratio="16:9",
    ),
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(1)
    operation = client.operations.get(operation)


# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("veo.mp4")

print("Generated video saved to veo.mp4")
