import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建OpenAI客户端
llm = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))

# 调用API,获取结果
response = llm.chat.completions.create(
    model="gpt-4o-mini", messages=[{"role": "user", "content": "下午好呀"}]
)
print(response.choices[0].message.content)

# 下午好！有什么我可以帮助你的吗？
