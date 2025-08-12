from ast import main
import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

# 加载环境变量
load_dotenv()

# 创建OpenAI Embedding模型
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

VECTOR_STORE_DIR = "./faiss_db"  # 向量库的存储路径


def build_vector_store() -> None:
    """构造向量库"""

    # 校验向量库是否已存在
    if os.path.exists(VECTOR_STORE_DIR):
        print("向量数据库已经构建完成，跳过该步骤。")
        return

    # 加载原始Document
    with open("./sales_datas.txt", encoding="utf8") as f:
        contents = f.read()

    # 把Document数据切割成一个个Chunk
    text_splitter = CharacterTextSplitter(
        separator=r"\d+\.\n",
        is_separator_regex=True,
        chunk_size=100,
        chunk_overlap=0,
        length_function=len,
    )
    chunks = text_splitter.create_documents([contents])
    print(f"文档切割完成，共 {len(chunks)} 个chunk")

    # 基于Faiss构造向量数据库,将数据保存到本地
    db = FAISS.from_documents(chunks, EMBEDDINGS)
    db.save_local(VECTOR_STORE_DIR)

    print(f"向量数据库构建完成，已保存到: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    build_vector_store()
