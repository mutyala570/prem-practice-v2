"""
==============================================================
11 - PYDANTIC: Data validation (CRITICAL for AI/LLM apps)
==============================================================

CONCEPT:
- Pydantic validates data automatically based on type hints
- Used EVERYWHERE in LangChain, FastAPI, OpenAI SDK
- Think of it as "TypeScript at runtime" or class-validator + class-transformer

Install: pip install pydantic
"""

from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional
from datetime import datetime


# ---------------- EXAMPLE 1: Basic model ----------------
print("=== Example 1: Basic Pydantic Model ===")

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = 0
    is_active: bool = True

# Valid
user = User(id=1, name="Mutyala", email="m@example.com", age=30)
print(user)
print(f"Name: {user.name}")
print(f"Dict: {user.model_dump()}")         # to dict
print(f"JSON: {user.model_dump_json()}")    # to JSON string

# Auto type coercion
user2 = User(id="5", name="Alice", email="a@x.com", age="25")   # strings!
print(f"Converted: {user2.id} ({type(user2.id)})")              # int


# ---------------- EXAMPLE 2: Validation errors ----------------
print("\n=== Example 2: Validation Errors ===")

try:
    bad = User(id="not_a_number", name="Bob", email="b@x.com")
except ValidationError as e:
    print("Caught validation error:")
    print(e.json(indent=2))


# ---------------- EXAMPLE 3: Advanced — nested, constraints, optional ----------------
print("\n=== Example 3: Advanced Model ===")

class Address(BaseModel):
    street: str
    city: str
    country: str = "India"


class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)                  # greater than 0
    quantity: int = Field(default=1, ge=1)           # greater-equal 1
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Order(BaseModel):
    order_id: int
    customer: User                     # nested model
    shipping_address: Address
    items: List[Product]
    total: float = Field(..., gt=0)


order = Order(
    order_id=101,
    customer=User(id=1, name="Mutyala", email="m@x.com", age=30),
    shipping_address=Address(street="MG Rd", city="Hyderabad"),
    items=[
        Product(id=1, name="Laptop", price=50000, tags=["electronics"]),
        Product(id=2, name="Mouse", price=500, quantity=2),
    ],
    total=51000
)

print(f"Order ID: {order.order_id}")
print(f"Customer: {order.customer.name}")
print(f"Items: {len(order.items)}")
print(f"JSON:\n{order.model_dump_json(indent=2)}")


# ---------------- WHY THIS MATTERS FOR AI ----------------
# LLMs often return messy/unstructured data.
# Pydantic lets you FORCE structured outputs:
#
# class Answer(BaseModel):
#     summary: str
#     confidence: float
#     sources: List[str]
#
# Then tell your LLM: "return JSON matching this schema"
# Parse with: Answer.model_validate_json(llm_response)


# ---------------- TRY IT YOURSELF ----------------
# 1. Create a `Movie` model with title, year (must be > 1900), rating (0-10)
# 2. Make a `BlogPost` with nested `Author` and list of comments
# 3. Try invalid data and see the clear error messages
