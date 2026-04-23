"""
==============================================================
09 - DATACLASSES & TYPE HINTS
==============================================================

CONCEPT:
- @dataclass auto-generates __init__, __repr__, __eq__
- Less boilerplate vs regular classes
- Perfect for data containers (like TS interfaces + classes)
- Type hints: `from typing import List, Dict, Optional, Union`
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict

# ---------------- EXAMPLE 1: Basic dataclass ----------------
print("=== Example 1: Basic Dataclass ===")

@dataclass
class User:
    name: str
    email: str
    age: int = 0                       # default value
    is_active: bool = True

# Auto-generated __init__
u1 = User(name="Mutyala", email="m@example.com", age=30)
u2 = User(name="Alice", email="a@example.com")

print(u1)                               # auto __repr__
print(u2)
print(f"Are equal: {u1 == User('Mutyala', 'm@example.com', 30)}")


# ---------------- EXAMPLE 2: Dataclass with lists/dicts ----------------
print("\n=== Example 2: Complex Dataclass ===")

@dataclass
class Product:
    id: int
    name: str
    price: float
    tags: List[str] = field(default_factory=list)     # mutable default needs factory
    metadata: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None                 # None or str

    def apply_discount(self, percent: float) -> float:
        return self.price * (1 - percent / 100)


p = Product(
    id=1,
    name="Laptop",
    price=50000,
    tags=["electronics", "computer"],
    description="Gaming laptop"
)

print(p)
print(f"Price after 10% off: {p.apply_discount(10)}")

p.tags.append("sale")
p.metadata["color"] = "silver"
print(f"Updated: {p}")


# ---------------- EXAMPLE 3: Type hints in functions ----------------
print("\n=== Example 3: Type Hints ===")

def get_active_users(users: List[User]) -> List[User]:
    return [u for u in users if u.is_active]

def find_user(users: List[User], email: str) -> Optional[User]:
    for u in users:
        if u.email == email:
            return u
    return None

users = [
    User("A", "a@x.com", 25, True),
    User("B", "b@x.com", 30, False),
    User("C", "c@x.com", 35, True),
]

active = get_active_users(users)
print(f"Active: {[u.name for u in active]}")

found = find_user(users, "b@x.com")
print(f"Found: {found}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Create a `Book` dataclass: title, author, pages, genres (list)
# 2. Create `Order` dataclass with items: List[Product], total: float
# 3. Function `filter_by_price(products, max_price) -> List[Product]`
