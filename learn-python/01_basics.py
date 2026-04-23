"""
==============================================================
01 - PYTHON BASICS: Variables, Data Types, Operators
==============================================================

CONCEPT:
Python is dynamically typed — you don't declare types like in TypeScript.
Common types: int, float, str, bool, None

Variables are just labels pointing to values.
Use snake_case (not camelCase like JavaScript).
"""

# ---------------- EXAMPLE 1: Basic data types ----------------
print("=== Example 1: Data Types ===")

name = "Mutyala"          # str
age = 30                  # int
height = 5.9              # float
is_engineer = True        # bool
salary = None             # None (like null)

print(f"Name: {name}, Type: {type(name)}")
print(f"Age: {age}, Type: {type(age)}")
print(f"Height: {height}, Type: {type(height)}")
print(f"Is Engineer: {is_engineer}, Type: {type(is_engineer)}")
print(f"Salary: {salary}, Type: {type(salary)}")


# ---------------- EXAMPLE 2: Operators & f-strings ----------------
print("\n=== Example 2: Operators & String Formatting ===")

a = 10
b = 3

print(f"a + b = {a + b}")      # 13
print(f"a - b = {a - b}")      # 7
print(f"a * b = {a * b}")      # 30
print(f"a / b = {a / b}")      # 3.333... (float division)
print(f"a // b = {a // b}")    # 3 (integer division)
print(f"a % b = {a % b}")      # 1 (modulo)
print(f"a ** b = {a ** b}")    # 1000 (power)

# String operations
first = "Hello"
second = "World"
combined = first + " " + second
repeated = first * 3

print(f"Combined: {combined}")
print(f"Repeated: {repeated}")
print(f"Length: {len(combined)}")
print(f"Upper: {combined.upper()}")
print(f"Contains 'World': {'World' in combined}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Create a variable for your favorite language
# 2. Calculate the area of a rectangle (length * width)
# 3. Print your name 5 times using *
