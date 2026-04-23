from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    # base_url="http://localhost:11434",   # default, uncomment if different
)

response = llm.invoke("Who is Albert Einstein?")
print(response.content)
