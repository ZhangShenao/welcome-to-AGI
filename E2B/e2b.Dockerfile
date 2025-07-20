# 基础镜像
FROM e2bdev/code-interpreter:latest

# 复制你的 Python 脚本到容器中
COPY run.py /workspace/run.py

# （可选）设置默认工作目录
WORKDIR /workspace

# （可选）设置容器启动时的默认命令
CMD ["python", "run.py"]