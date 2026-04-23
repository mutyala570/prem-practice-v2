"""
==============================================================
05 - EXCEPTIONS: try/except/finally, custom exceptions
==============================================================

CONCEPT:
- Similar to try/catch in JavaScript
- `except` instead of `catch`
- You can catch specific exception types
- Always use specific exceptions, not bare `except:`
"""

# ---------------- EXAMPLE 1: Basic try/except ----------------
print("=== Example 1: Basic try/except ===")

def divide(a: float, b: float) -> float:
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Can't divide by zero")
        return 0
    except TypeError as e:
        print(f"Type error: {e}")
        return 0
    finally:
        print("Division attempt finished")

print(divide(10, 2))
print(divide(10, 0))
print(divide(10, "abc"))


# ---------------- EXAMPLE 2: Custom exceptions ----------------
print("\n=== Example 2: Custom Exceptions ===")

class InvalidAgeError(Exception):
    """Raised when age is invalid."""
    pass

class UserNotFoundError(Exception):
    """Raised when user doesn't exist."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


def register_user(name: str, age: int) -> dict:
    if age < 0 or age > 150:
        raise InvalidAgeError(f"Invalid age: {age}")
    return {"name": name, "age": age}


def get_user(user_id: int) -> dict:
    users = {1: "Alice", 2: "Bob"}
    if user_id not in users:
        raise UserNotFoundError(user_id)
    return {"id": user_id, "name": users[user_id]}


# Using them
try:
    user = register_user("Mutyala", -5)
except InvalidAgeError as e:
    print(f"Caught: {e}")

try:
    user = get_user(999)
except UserNotFoundError as e:
    print(f"Caught: {e} (id was {e.user_id})")


# ---------------- TRY IT YOURSELF ----------------
# 1. Write a function that reads an int from user input with try/except
# 2. Create a custom `InsufficientBalanceError` for a bank withdraw function
# 3. Chain multiple exceptions: catch FileNotFoundError AND PermissionError
