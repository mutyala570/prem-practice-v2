import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm =ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

template = """
You are a helpful assistant that generates creative stories.

Subject: {subject}
Story: {story} in 10 words
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["subject", "story"]
)

chain = prompt | llm

user_message="I have 500 units in stock and I sell 50 units per day.and I need 95% service level"

response = chain.invoke({"subject": " Once upon a time", "story": user_message})
print("Response:---------", response.content)
