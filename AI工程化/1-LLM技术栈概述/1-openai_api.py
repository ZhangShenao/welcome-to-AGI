import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建DeepSeek客户端,兼容openai的api接口
deepseek = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL"), api_key=os.getenv("DEEPSEEK_API_KEY")
)

# 调用DeepSeek API,获取结果
response = deepseek.chat.completions.create(
    model="deepseek-chat", messages=[{"role": "user", "content": "下午好呀"}]
)
print(response.choices[0].message.content)

# 下午好呀！☀️ 今天过得怎么样？有什么想聊的或者需要帮忙的吗？ （悄悄说，我这儿还有冷笑话库存哦~）
