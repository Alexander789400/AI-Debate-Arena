import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# PRO AGENT
pro_llm = ChatGroq(
    model="openai/gpt-oss-20b", # 
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
)

# CON AGENT
con_llm = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",# 
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
)

# JUDGE AGENT
judge_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY"),
)

# FINAL RESULT AGENT
result_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY"),
)