# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/24 10:00
@Author  : ZhangShenao
@File    : sora_2_gen_video.py
@Desc    : 使用Sora 2生成视频
"""

import os
import time

import dotenv

dotenv.load_dotenv()

from openai import OpenAI

# prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
# A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

prompt = "Elon Musk is sitting in a chair, smoking"

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")
# )

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 记录开始时间
start_time = time.time()
print(f"开始生成视频")
video = client.videos.create(
    prompt=prompt,
    seconds="8",
    size="720x1280",
)
video_id = video.id
print(f"视频任务创建成功，视频ID: {video_id}")

status = client.videos.retrieve(video_id).status
while status != "completed":
    time.sleep(1)
    video = client.videos.retrieve(video_id)
    print(video)
    status = video.status
    print(f"视频生成中... 状态: {status}")


# 记录结束时间并计算耗时
end_time = time.time()
total_time = end_time - start_time

print(f"视频生成完成！视频ID: {video_id}")
print(f"总耗时: {total_time:.2f} 秒 ({total_time/60:.2f} 分钟)")
