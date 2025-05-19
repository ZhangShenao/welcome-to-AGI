# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/19 10:57 
@Author  : ZhangShenao 
@File    : 1.pytorch_quick_start.py 
@Desc    : PyTorch环境搭建

安装PyTorch环境
pip install --upgrade torch torchvision torchaudio

PyTorch是一款深度学习计算框架
它能够利用GPU环境,帮助我们高效完成一些列深度学习的复杂计算

想要用好PyTorch这个工具
我们就得设计好整个任务的流程、整个网络架构
这样PyTorch才能实现各种各样复杂的计算功能

因为GPU作矩阵运算比较快,因此PyTorch首选GPU环境
"""

import torch

# 验证本地是否有可用的CUDA环境
is_cuda = torch.cuda.is_available()
print(f"【CUDA是否可用】{is_cuda}")
