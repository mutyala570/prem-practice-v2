import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0,
    api_key=os.environ.get('GROQ_API_KEY')
)


extract_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a parameter extraction assistant. Extract inventory parameters from the user's natural language query.

Return ONLY a JSON object with these four keys (no other text):
{{"current_stock": <number>, "lead_time": <number>, "avg_daily_demand": <number>, "service_level": <number>}}

- current_stock: units currently on hand
- lead_time: days to receive a new shipment
- avg_daily_demand: average units sold/consumed per day
- service_level: target service level as a percentage (e.g. 95 for 95%)

If any parameter is missing or unclear, set its value to null.
"""),
    ("human", "{user_message}")
])

# chain = extract_prompt | llm | StrOutputParser()
chain = extract_prompt | llm


# response = chain.invoke({"user_message": "I have 500 units in stock and,lead time is 5 days,I sell 50 units per day.and I need 95% service level"})
response = chain.invoke({"user_message": "my name is prem"})
# print(response)
print(response.content)
