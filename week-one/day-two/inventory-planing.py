import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import gradio as gr


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY")

)

# Chain 0: Extract inventory parameters from natural language
extract_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a parameter extraction assistant. Extract inventory parameters from the user's natural language query.

Return ONLY a JSON object with these four keys (no other text):
{{"current_stock": <number>, "lead_time": <number>, "avg_daily_demand": <number>, "service_level": <number>}}

- current_stock: units currently on hand
- lead_time: days to receive a new shipment
- avg_daily_demand: average units sold/consumed per day
- service_level: target service level as a percentage (e.g. 95 for 95%)

If any parameter is missing or unclear, set its value to null."""),
    ("human", "{user_message}")
])

extract_chain = extract_prompt | llm | StrOutputParser()

# Chain 1: Compute desired stock level
compute_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an inventory planning expert. Given inventory parameters, compute the desired stock level.

Use this formula:
- Safety Stock = Z-score(service_level) * sqrt(lead_time) * average_daily_demand
- Desired Stock = (average_daily_demand * lead_time) + Safety Stock

Common Z-scores: 90% -> 1.28, 95% -> 1.65, 99% -> 2.33

Show your step-by-step calculation. End your response with a line:
DESIRED_STOCK: <number>"""),
    ("human", """Current Stock: {current_stock}
Lead Time (days): {lead_time}
Average Daily Demand: {avg_daily_demand}
Service Level: {service_level}%""")
])

compute_chain = compute_prompt | llm | StrOutputParser()

# Chain 2: Determine reorder quantity and provide recommendation
reorder_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an inventory planning advisor. Given the computation below and the current stock,
determine the reorder quantity and provide a clear recommendation.

Reorder Quantity = max(0, Desired Stock - Current Stock)

Provide:
1. The reorder quantity
2. Whether an immediate reorder is needed
3. A brief justification"""),
    ("human", """Current Stock: {current_stock}

Stock Computation:
{computation}""")
])

reorder_chain = reorder_prompt | llm | StrOutputParser()



def extract_params(user_message):
    """Use the LLM to extract inventory parameters from natural language."""
    raw = extract_chain.invoke({"user_message": user_message})
    params = json.loads(raw)
    missing = [k for k, v in params.items() if v is None]
    if missing:
        friendly = [k.replace("_", " ") for k in missing]
        raise ValueError(f"Could not determine: {', '.join(friendly)}")
    return params

def run_inventory_agent(user_message):
    """Run the three-step inventory planning chain."""
    # Step 1: Extract parameters from natural language
    params = extract_params(user_message)

    # Step 2: Compute desired stock
    computation = compute_chain.invoke({
        "current_stock": params["current_stock"],
        "lead_time": params["lead_time"],
        "avg_daily_demand": params["avg_daily_demand"],
        "service_level": params["service_level"],
    })

    # Step 3: Determine reorder quantity
    recommendation = reorder_chain.invoke({
        "current_stock": params["current_stock"],
        "computation": computation,
    })

    extracted = (
        f"**Extracted Parameters:** Current Stock = {params['current_stock']}, "
        f"Lead Time = {params['lead_time']} days, "
        f"Avg Daily Demand = {params['avg_daily_demand']}, "
        f"Service Level = {params['service_level']}%"
    )

    return f"{extracted}\n\n---\n\n## Step 1: Stock Computation\n\n{computation}\n\n---\n\n## Step 2: Reorder Recommendation\n\n{recommendation}"


def chat_handler(message, history):
    """Handle natural language inventory queries."""
    try:
        return run_inventory_agent(message)
    except ValueError as e:
        return (
            f"I couldn't extract all the needed parameters: {e}\n\n"
            "Please make sure your message includes:\n"
            "- **Current stock** (units on hand)\n"
            "- **Lead time** (days to receive new shipment)\n"
            "- **Average daily demand** (units sold per day)\n"
            "- **Service level** (e.g. 95%)"
        )
    except Exception as e:
        return (
            f"Something went wrong: {e}\n\n"
            "Try describing your inventory situation naturally, for example:\n\n"
            "*\"I have 500 units in stock, lead time is 7 days, we sell about 50 per day, "
            "and I need 95% service level. How much should I reorder?\"*"
        )

demo = gr.ChatInterface(
    fn=chat_handler,
    title="Inventory Planning Agent",
    description="Describe your inventory situation in plain English and get a reorder recommendation.",
    examples=[
        "I have 500 units in my warehouse. It takes 7 days to get a new shipment, we sell about 50 units per day, and I want 95% service level. How much should I reorder?",
        "We're running low — only 100 items left! Supplier takes 14 days, demand is 30 units/day, and we need 99% availability. What should I do?",
        "We have 1000 pieces, daily consumption is 20 units, lead time is 3 days, and 90% service level is fine. Do I need to order more?",
    ],
)
demo.launch()
