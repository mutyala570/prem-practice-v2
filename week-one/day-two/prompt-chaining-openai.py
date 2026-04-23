import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY")
)

summary_chain = ChatPromptTemplate.from_template(
    "Summarize the following customer review into a single sentence:\n\n{review}\n\nSummary:"
) | llm | StrOutputParser()

sentiment_chain = ChatPromptTemplate.from_template(
    "Classify the sentiment of the following review as positive, negative, or neutral:\n\n{summary}\n\nSentiment:"
) | llm | StrOutputParser()

suggestion_chain = ChatPromptTemplate.from_template(
    "Based on the sentiment below, provide a suggestion for how the business should respond:\n\n{sentiment}\n\nSuggestion:"
) | llm | StrOutputParser()


def run_chain(review: str):
    summary = summary_chain.invoke({"review": review})
    sentiment = sentiment_chain.invoke({"summary": summary})
    suggestion = suggestion_chain.invoke({"sentiment": sentiment})
    return {
        "summary": summary,
        "sentiment": sentiment,
        "suggestion": suggestion,
    }


if __name__ == "__main__":
    review = (
        "I ordered a pair of headphones from this store last week. "
        "The sound quality is amazing and the battery lasts all day, "
        "but the delivery took much longer than promised."
    )
    result = run_chain(review)
    print("Summary:\n", result["summary"], "\n")
    print("Sentiment:\n", result["sentiment"], "\n")
    print("Suggestion:\n", result["suggestion"])
