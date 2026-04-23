import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

response1 = llm.invoke("tell me about india i want in 10 words")
print("Response 1:---------", response1.content)

response2 = llm.invoke("tell me about its capital city")
print("Response 2:---------", response2.content)