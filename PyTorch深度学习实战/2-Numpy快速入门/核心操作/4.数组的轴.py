# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/19 15:45 
@Author  : ZhangShenao 
@File    : 4.数组的轴.py 
@Desc    : 数组的轴

数组的轴即数组的维度,它是从0开始的
针对二维数组,共有两个轴: 分别是代表行的0轴与代表列的1轴

当axis=i时,就是按照第i个轴的方向进行计算的
或者可以理解为: 第i个轴的数据将会被折叠或聚合到一起
"""

import numpy as np

# 创建一个随机的4x3维的数组
# 代表4名同学、针对3门课程的分数
scores = np.random.randint(low=0, high=101, size=(4, 3))
print(scores)

# 按照课程维度,统计每门课程的平均分
# 需要按照X轴的方向统计,即0轴
course_avg_scores = np.average(scores, axis=0)
print(f"【课程平均分】: {course_avg_scores}")

# 按照学生维度,统计每名学生的平均分
# 需要按照Y轴的方向统计,即1轴
student_avg_scores = np.average(scores, axis=1)
print(f"【学生平均分】: {student_avg_scores}")
