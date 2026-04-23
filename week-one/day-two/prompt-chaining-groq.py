import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)

summary_chain = ChatPromptTemplate.from_template(
    "Summarize the following customer review into a single sentence:\n\n{review}\n\nSummary:"
) | llm | StrOutputParser()

sentiment_chain = ChatPromptTemplate.from_template(
    "Classify the sentiment of the following review as positive, negative, or neutral:\n\n{summary}\n\nSentiment:"
) | llm | StrOutputParser()

suggestion_chain = ChatPromptTemplate.from_template(
    "Based on the sentiment, provide a suggestion for the following review:\n\n{sentiment}\n\nSuggestion:"
) | llm | StrOutputParser()

full_chain = (
    summary_chain
    | RunnableLambda(lambda x: {"summary": x})
    | sentiment_chain
    | RunnableLambda(lambda x: {"sentiment": x})
    | suggestion_chain
)

review = "The product was okay, but the delivery was slow."

result = full_chain.invoke({"review": review})

print(result)
