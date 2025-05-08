# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/16 15:19 
@Author  : ZhangShenao 
@File    : video_process.py
@Desc    : 视频处理
"""
import base64
import os
from typing import List

import cv2


def extract_frames(video_path: str, interval: int = 1) -> List:
    """
    视频抽帧
    :param video_path: 视频文件路径
    :param interval: 采样率,即每N秒抽取一帧
    :return: 抽取的视频帧列表
    """
    extracted_frames = []
    file_name, _ = os.path.splitext(video_path)

    video_capture = cv2.VideoCapture(video_path)
    total_frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frames_interval = int(frame_rate * interval)
    current_frame = 0

    # 循环遍历视频并以指定的采样率提取帧
    while current_frame < total_frame_count - 1:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        success, frame = video_capture.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        extracted_frames.append(base64.b64encode(buffer).decode("utf-8"))
        current_frame += frames_interval
    video_capture.release()

    print(f"视频抽帧完成！共抽取了 {len(extracted_frames)} 帧")
    return extracted_frames
