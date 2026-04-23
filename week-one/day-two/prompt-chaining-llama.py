from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.2",
    # base_url="http://localhost:11434",   # default, uncomment if different
)

summary_chain = ChatPromptTemplate.from_template(
    "Summarize the following customer review into a single sentence:\n\n{review}\n\nSummary:"
) | llm

sentiment_chain = ChatPromptTemplate.from_template(
    "Classify the sentiment of the following review as positive, negative, or neutral:\n\n{summary}\n\nSentiment:"
) | llm

suggestion_chain = ChatPromptTemplate.from_template(
    "Based on the sentiment, provide a suggestion for the following review:\n\n{sentiment}\n\nSuggestion:"
) | llm

review = "The headphones sound amazing and battery lasts all day, but delivery took much longer than promised."

summary = summary_chain.invoke({"review": review}).content
sentiment = sentiment_chain.invoke({"summary": summary}).content
suggestion = suggestion_chain.invoke({"sentiment": sentiment}).content

print("Summary:\n", summary)
print("\nSentiment:\n", sentiment)
print("\nSuggestion:\n", suggestion)
