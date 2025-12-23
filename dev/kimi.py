from openai import OpenAI
from dotenv import load_dotenv
import os

# 从 .env 文件加载环境变量
load_dotenv(dotenv_path="../.env")  # 指定文件名为 .env

# 读取 API key 和模型名
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL_ID")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
    ],
    temperature=0.6,
)

print(completion.choices[0].message.content)