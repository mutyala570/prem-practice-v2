import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="messages"),#here name what it put in the messages placeholder
    ("human", "{input}")
])

chain = prompt | llm 
chat_history = []

def chat(user_input: str):
    response = chain.invoke({"messages": chat_history, "input": user_input})# here need to pass the same
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))
    return response.content

print(chat("tell me about india"))
print("\n\n------------------------\n\n")
print(chat("What is the capital of india?"))
   