import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=1,
    api_key=os.environ.get('GROQ_API_KEY')
)

response=llm.invoke("what is safety stock in inventory management?")
print(response.content)


