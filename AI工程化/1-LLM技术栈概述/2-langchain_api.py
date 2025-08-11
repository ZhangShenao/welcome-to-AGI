import datetime
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


from langchain_core.output_parsers import StrOutputParser


# 加载环境变量
load_dotenv()

# 创建LL
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.7,
)


def chain_demo() -> str:
    """
    演示 LLMChain: 支持变量注入与模板复用的核心组件
    LangChain 特点: 模板化提示词管理,支持变量替换
    """
    print("=" * 50)
    print("🔗 LLMChain 演示: Prompt → LLM → OutputParser")
    print("=" * 50)

    # 创建提示词模板 - LangChain 特点: 模板复用
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个助手，请根据用户的问题给出回答"),
            (
                "human",
                """
            请以{style}的风格，写一段关于{topic}的介绍。
            要求: 简洁明了，不超过100字。
            """,
            ),
        ]
    )

    # 构造Chain
    # LangChain 0.3 推荐使用 LCEL (LangChain Expression Language)
    chain = prompt | llm | StrOutputParser()

    # 调用Chain,并注入变量
    result = chain.invoke({"topic": "区块链", "style": "通俗生动"})
    print(f"📝 LLMChain 输出：\n{result}\n")

    return result


if __name__ == "__main__":
    print(chain_demo())
