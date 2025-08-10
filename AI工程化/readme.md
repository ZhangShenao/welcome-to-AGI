# Python 工程化环境准备步骤

## 1. 使用 Conda 创建虚拟环境并指定 Python 版本

### 安装 Conda
如果还没有安装 Conda，可以下载 Miniconda 或 Anaconda：
- Miniconda: https://docs.conda.io/en/latest/miniconda.html
- Anaconda: https://www.anaconda.com/products/distribution

### 创建虚拟环境
```bash
# 创建新的虚拟环境，指定 Python 版本
conda create -n ai-engineering python=3.12


# 激活虚拟环境
conda activate ai-engineering

# 查看当前环境信息
conda info --envs

# 查看当前环境的 Python 版本
python --version
```

### 管理虚拟环境
```bash
# 列出所有环境
conda env list

# 删除环境
conda env remove -n ai-engineering

# 退出当前环境
conda deactivate
```

## 2. 查看 pip 安装的包版本

### 查看已安装的包
```bash
# 查看所有已安装的包及版本
pip list

# 查看特定包的版本
pip show package_name

# 查看过时的包
pip list --outdated

# 以 requirements 格式显示
pip freeze
```

### 查看包的详细信息
```bash
# 查看包的详细信息，包括依赖关系
pip show -v package_name

# 查看包的安装位置
pip show -f package_name
```

## 3. 使用 requirements.txt 文件

### 生成 requirements.txt
```bash
# 生成当前环境的所有包列表
pip freeze > requirements.txt

# 只包含直接安装的包（推荐）
pip list --format=freeze > requirements.txt
```

### 使用 requirements.txt 安装包
```bash
# 从 requirements.txt 安装所有包
pip install -r requirements.txt

# 升级所有包到 requirements.txt 指定版本
pip install -r requirements.txt --upgrade
```

### requirements.txt 文件格式示例
```
# 精确版本
numpy==1.21.0
pandas==1.3.3

# 最小版本
requests>=2.25.0

# 版本范围
matplotlib>=3.0.0,<4.0.0

# 从 Git 仓库安装
git+https://github.com/user/repo.git

# 带注释
flask==2.0.1  # Web 框架
sqlalchemy==1.4.22  # 数据库 ORM
```

### 最佳实践
```bash
# 创建开发环境的 requirements
pip freeze > requirements-dev.txt

# 创建生产环境的精简 requirements
# 手动编辑，只包含必要的包
```

## 4. 使用环境变量保存 OPENAI API KEY

### 设置环境变量

#### 临时设置（当前会话有效）
```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# Windows Command Prompt
set OPENAI_API_KEY=your-api-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"
```

#### 永久设置

##### Linux/macOS
```bash
# 编辑 ~/.bashrc 或 ~/.zshrc 文件
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc

# 或者编辑 ~/.bash_profile
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bash_profile

# 重新加载配置文件
source ~/.bashrc
```

##### Windows
```bash
# 使用 setx 命令永久设置（需要重启终端）
setx OPENAI_API_KEY "your-api-key-here"
```

### 使用 .env 文件（推荐）
```bash
# 创建 .env 文件
echo "OPENAI_API_KEY=your-api-key-here" > .env

# 安装 python-dotenv
pip install python-dotenv
```

Python 代码中使用：
```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 获取 API KEY
api_key = os.getenv('OPENAI_API_KEY')
```

### 查看环境变量的方法

#### 命令行查看
```bash
# Linux/macOS - 查看特定环境变量
echo $OPENAI_API_KEY

# Windows Command Prompt
echo %OPENAI_API_KEY%

# Windows PowerShell
echo $env:OPENAI_API_KEY

# 查看所有环境变量
# Linux/macOS
env | grep OPENAI

# Windows
set | findstr OPENAI
```

#### Python 中查看
```python
import os

# 获取特定环境变量
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {api_key}")

# 获取所有环境变量
all_env = os.environ
for key, value in all_env.items():
    if 'OPENAI' in key:
        print(f"{key}: {value}")

# 检查环境变量是否存在
if 'OPENAI_API_KEY' in os.environ:
    print("API Key 已设置")
else:
    print("API Key 未设置")
```

## 5. 完整的项目环境设置流程

### 步骤 1: 创建项目目录和虚拟环境
```bash
# 创建项目目录
mkdir my_ai_project
cd my_ai_project

# 创建虚拟环境
conda create -n my_ai_project python=3.9
conda activate my_ai_project
```

### 步骤 2: 安装必要的包
```bash
# 安装基础包
pip install openai python-dotenv requests pandas numpy

# 生成 requirements.txt
pip freeze > requirements.txt
```

### 步骤 3: 设置环境变量
```bash
# 创建 .env 文件
echo "OPENAI_API_KEY=your-actual-api-key-here" > .env

# 添加到 .gitignore（重要！）
echo ".env" >> .gitignore
```

### 步骤 4: 验证设置
```python
# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("✅ 环境变量设置成功")
    print(f"API Key 前缀: {api_key[:10]}...")
else:
    print("❌ 环境变量未设置")
```

## 6. 常用命令总结

```bash
# Conda 环境管理
conda create -n env_name python=3.9
conda activate env_name
conda deactivate
conda env list
conda env remove -n env_name

# pip 包管理
pip install package_name
pip install -r requirements.txt
pip list
pip freeze > requirements.txt
pip show package_name

# 环境变量
export VAR_NAME="value"  # Linux/macOS
set VAR_NAME=value       # Windows CMD
echo $VAR_NAME           # 查看变量
```

## 7. 安全注意事项

1. **永远不要将 API Key 提交到版本控制系统**
   - 使用 .env 文件存储敏感信息
   - 将 .env 添加到 .gitignore

2. **定期轮换 API Key**
   - 定期更新 API Key
   - 监控 API 使用情况

3. **使用环境特定的配置**
   - 开发环境、测试环境、生产环境分别配置
   - 使用不同的 API Key 和配置

4. **权限最小化原则**
   - 只给予必要的 API 权限
   - 设置使用限制和监控