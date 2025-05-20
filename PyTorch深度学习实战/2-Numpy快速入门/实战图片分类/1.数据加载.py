# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/20 17:03 
@Author  : ZhangShenao 
@File    : 1.数据加载.py 
@Desc    : 数据加载
"""

import cv2
import numpy as np
from PIL import Image


def load_image_by_pillow() -> None:
    """
    使用Pillow加载图片
    在PyTorch中,很多图片的操作都是基于Pillow的
    所以当使用PyTorch编程出现问题,或者要思考、解决一些图片相关问题时,要从 Pillow 的角度出发
    """

    img = Image.open("./geektime.jpg")
    print("使用Pillow加载图片成功")
    print(img.size)  # (318, 116)

    # Pillow 是以二进制形式读入保存的
    # 可以利用NumPy的asarray方法,将Pillow的数据转换为NumPy的数组格式

    img_arr = np.asarray(img)
    print(img_arr.shape)  # (116, 318, 3)


def load_image_by_opencv() -> None:
    """
    使用OpenCV加载图片
    """

    # OpenCV加载图片后,直接回返回NumPy的数组格式
    # 无需再进行转换
    img_cv2 = cv2.imread("./geektime.jpg")
    print("使用OpenCV加载图片成功")
    print(type(img_cv2))  # <class 'numpy.ndarray'>
    print(img_cv2.shape)  # (116, 318, 3)


if __name__ == '__main__':
    load_image_by_pillow()
    load_image_by_opencv()
