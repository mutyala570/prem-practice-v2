# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate

# load_dotenv()

# llm = ChatGroq(
#     model="openai/gpt-oss-120b",
#     api_key=os.environ.get("GROQ_API_KEY")
# )

# prompt = PromptTemplate(
#     template="Tell me about {topic} in 10 words",
#     input_variables=["topic"]
# )

# chain = prompt | llm

# response = chain.invoke({"topic": "roger federer"})
# print("Response:---------", response.content)


import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

prompt =PromptTemplate(
    template="Tell me about {topic} in 10 words",
    input_variables=["topic"]
)

chain = prompt | llm

response = chain.invoke({"topic": "roger federer"})
print("Response:---------", response.content)
