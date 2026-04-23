"""
==============================================================
03 - CONTROL FLOW: if/else, for, while, comprehensions
==============================================================

CONCEPT:
Python uses INDENTATION (4 spaces) instead of braces {}.
No parentheses needed around conditions.
`elif` instead of `else if`.
"""

# ---------------- EXAMPLE 1: if / elif / else ----------------
print("=== Example 1: Conditionals ===")

score = 75

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")

# Ternary operator (one-line if/else)
status = "Pass" if score >= 60 else "Fail"
print(f"Status: {status}")


# ---------------- EXAMPLE 2: For loops ----------------
print("\n=== Example 2: For Loops ===")

# Loop over a list
for fruit in ["apple", "banana", "mango"]:
    print(f"Fruit: {fruit}")

# Range
for i in range(5):              # 0 to 4
    print(f"i = {i}")

for i in range(2, 10, 2):       # 2, 4, 6, 8
    print(f"even: {i}")

# Enumerate — get index + value
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")


# ---------------- EXAMPLE 3: While loop + break/continue ----------------
print("\n=== Example 3: While, break, continue ===")

count = 0
while count < 10:
    count += 1
    if count == 3:
        continue        # skip this iteration
    if count == 7:
        break           # exit loop
    print(f"count: {count}")


# ---------------- EXAMPLE 4: List comprehension (VERY Pythonic) ----------------
print("\n=== Example 4: List Comprehensions ===")

numbers = [1, 2, 3, 4, 5, 6]

# Traditional way
squared = []
for n in numbers:
    squared.append(n ** 2)

# Pythonic way
squared_v2 = [n ** 2 for n in numbers]
print(f"Squared: {squared_v2}")

# With condition
evens = [n for n in numbers if n % 2 == 0]
print(f"Evens: {evens}")

# Dict comprehension
squared_dict = {n: n ** 2 for n in numbers}
print(f"Dict: {squared_dict}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Print FizzBuzz for 1-20 (Fizz if div by 3, Buzz if div by 5, FizzBuzz if both)
# 2. Using comprehension: get squares of only odd numbers from 1-10
# 3. Count vowels in a string using a loop
