# -*- coding: utf-8 -*-
"""
@Time    : 2025/10/25 10:00
@Author  : ZhangShenao
@File    : seedance_gen_video.py
@Desc    : 使用SeeDance生成视频
"""

import os
import time

# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
from volcenginesdkarkruntime import Ark
import base64

# 加载环境变量
import dotenv

import os

# 加载环境变量
dotenv.load_dotenv()

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=os.getenv("ARK_API_KEY"),
)

if __name__ == "__main__":
    print("----- create request -----")
    with open("musk.png", "rb") as image_file:
        ref_pic = base64.b64encode(image_file.read()).decode("utf-8")
    create_result = client.content_generation.tasks.create(
        model="doubao-seedance-1-0-pro-250528",  # 模型 Model ID 已为您填入
        content=[
            {
                # 文本提示词与参数组合
                "type": "text",
                "text": "这个男人走到车门口，打开车门，坐进了车里，点燃一支香烟，吸了一口，然后吐出一口烟雾。最后看向镜头，露出自信的微笑。  --resolution 1080p  --duration 12 --camerafixed false --watermark true",
            },
            {  # 若仅需使用文本生成视频功能，可对该大括号内的内容进行注释处理，并删除上一行中大括号后的逗号。
                # 首帧图片URL
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{ref_pic}"},
            },
        ],
    )
    print(create_result)

    # 轮询查询部分
    print("----- polling task status -----")
    task_id = create_result.id
    while True:
        get_result = client.content_generation.tasks.get(task_id=task_id)
        status = get_result.status
        if status == "succeeded":
            print("----- task succeeded -----")
            print(get_result)
            break
        elif status == "failed":
            print("----- task failed -----")
            print(f"Error: {get_result.error}")
            break
        else:
            print(f"Current status: {status}, Retrying after 3 seconds...")
            time.sleep(3)

# 更多操作请参考下述网址
# 查询视频生成任务列表：https://www.volcengine.com/docs/82379/1521675
# 取消或删除视频生成任务：https://www.volcengine.com/docs/82379/1521720
