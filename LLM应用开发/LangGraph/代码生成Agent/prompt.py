# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/16 15:39 
@Author  : ZhangShenao 
@File    : prompt.py 
@Desc    : Prompt相关定义
"""

# 生成代码的System Prompt
SYSTEM_PROMPT = """
你是一个golang开发者, 擅长使用gin框架, 你将编写基于gin框架的web后端程序
你只需直接输出代码, 不要做任何解释和说明，不要将代码放到 ```go ``` 中
"""

# 生成Model实体类的Prompt
MODEL_PROMPT = """
生成用户模型的实体类代码
"""

# 生成Router路由的Prompt
ROUTER_PROMPT = """
#任务
生成gin的路由代码

#路由
1.Get /version 获取应用的版本
2.Get /users 获取用户列表

#规则
字符串分三段，第一段：Method，第二段：请求 PATH，第三段：代码注释

#示例
r.Get("/version", versionHandler) // 用于获取应用的版本的路由，handler函数名示例：versionHandler
"""

# 生成Handler处理器的Prompt
HANDLER_PROMPT = """
#任务
生成gin的路由所对应的handler处理函数代码

#规则
你只需要生成提供的路由代码对应的 handler 函数，不需要生成额外代码
handler函数是和路由代码一一对应的，handler函数的名称在路由代码的注释中已经给出
如果handler函数需要用到模型，则在模型代码中选择

#路由代码
{routers}

#模型代码
{models}

#路由处理函数功能
1.输出应用的版本为1.0
2.输出用户列表
"""

# 生成main函数的Prompt
MAIN_FUNCTION_PROMPT = """
请按照如下要求，结合gin框架，生成Go语言的main函数
1.创建gin对象
2.已经存在的Router相关代码: 
{routers}
handler代码已经生成，无需再进行处理
3.启动端口为8080
"""
