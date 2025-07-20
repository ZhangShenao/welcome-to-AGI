from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# 加载环境变量
load_dotenv()

# 创建Sandbox实例
# 默认Sandbox存活时间为5分钟
sbx = Sandbox(template="cy0ptg5pnftu0xtgnuja")

# 在Sandbox中执行Python代码
execution = sbx.run_code("print('hello world')")


# 打印执行结果
# Logs(stdout: ['hello world\n'], stderr: [])
print(execution.logs)

# 列出Sandbox中的文件
files = sbx.files.list("/")
print(files)
