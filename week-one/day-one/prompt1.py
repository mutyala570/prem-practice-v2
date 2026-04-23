import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    # model="llama-3.1-8b-instant",
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

response = llm.invoke("Who is Albert Einstein?")
print(response.content)
