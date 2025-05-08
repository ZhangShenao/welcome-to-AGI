# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/16 16:02 
@Author  : ZhangShenao 
@File    : main.py 
@Desc    : 入口程序
"""
from video_process import extract_frames
from video_understanding import introduction

if __name__ == '__main__':
    frames = extract_frames(video_path="./乡村爱情.mp4", interval=1)

    intro = introduction(frames)
    print(f"视频内容介绍: {intro}")
