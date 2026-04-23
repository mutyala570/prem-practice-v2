"""
==============================================================
04 - FUNCTIONS: def, *args, **kwargs, lambda, type hints
==============================================================

CONCEPT:
- Functions defined with `def`
- Type hints are optional but HIGHLY recommended (like TypeScript)
- *args = variable positional args  (like ...rest in JS)
- **kwargs = variable keyword args
- lambda = anonymous function (like arrow functions)
"""

# ---------------- EXAMPLE 1: Basic function with type hints ----------------
print("=== Example 1: Basic Function ===")

def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting message."""
    return f"{greeting}, {name}!"

print(greet("Mutyala"))
print(greet("Alice", greeting="Hi"))
print(greet(name="Bob", greeting="Hey"))


# ---------------- EXAMPLE 2: *args and **kwargs ----------------
print("\n=== Example 2: *args and **kwargs ===")

def sum_all(*numbers: int) -> int:
    """Sum any number of integers."""
    return sum(numbers)

print(f"Sum: {sum_all(1, 2, 3)}")
print(f"Sum: {sum_all(10, 20, 30, 40, 50)}")


def print_info(**details) -> None:
    """Print any key-value pairs."""
    for key, value in details.items():
        print(f"  {key}: {value}")

print_info(name="Mutyala", age=30, role="Engineer")


# Combine both
def flexible(*args, **kwargs):
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

flexible(1, 2, 3, name="Alice", active=True)


# ---------------- EXAMPLE 3: Lambda (anonymous functions) ----------------
print("\n=== Example 3: Lambda ===")

# Like arrow functions in JS
square = lambda x: x ** 2
print(f"Square of 5: {square(5)}")

# Common use: sorting
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

# Sort by age
sorted_people = sorted(people, key=lambda p: p["age"])
for p in sorted_people:
    print(p)

# map & filter with lambda
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda n: n * 2, numbers))
evens = list(filter(lambda n: n % 2 == 0, numbers))
print(f"Doubled: {doubled}")
print(f"Evens: {evens}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Write a function `calculate(op, a, b)` that does +, -, *, / based on op
# 2. Write a function that accepts any number of strings and returns them joined
# 3. Sort a list of dicts by name alphabetically using lambda
