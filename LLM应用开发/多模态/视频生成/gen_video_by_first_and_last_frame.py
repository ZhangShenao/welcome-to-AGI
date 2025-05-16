# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/16 16:48 
@Author  : ZhangShenao 
@File    : gen_video_by_first_and_last_frame.py 
@Desc    : 基于首尾帧图片生成视频
"""
import base64
import os

import dotenv
from volcenginesdkarkruntime import Ark

if __name__ == "__main__":
    # 加载环境变量
    dotenv.load_dotenv()

    # 创建ARK客户端
    client = Ark(api_key=os.environ.get("VOLCENGINE_API_KEY"))

    # 对首尾帧图片进行Base64编码
    with open("./first_frame.png", "rb") as image_file:
        first_frame = base64.b64encode(image_file.read()).decode('utf-8')

    with open("./last_frame.png", "rb") as image_file:
        last_frame = base64.b64encode(image_file.read()).decode('utf-8')

    # 创建视频生成任务
    resp = client.content_generation.tasks.create(
        model="wan2-1-14b-flf2v-250417",
        content=[
            {
                "type": "text",
                "text": "这只可爱的小猪在天上飞累了，它呼扇着翅膀，慢慢降落到下面的小河里，痛快地洗了个澡，又惬意地搭了个哈欠。--rs 720p  --dur 10"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{first_frame}",
                },
                "role": "first_frame"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{last_frame}",
                },
                "role": "last_frame"
            }
        ],
    )

    print(resp)


def get_result() -> None:
    # 获取视频生成任务结果
    resp = client.content_generation.tasks.get(
        task_id="cgt-20250516172858-97jp9",
    )
    print(resp)
