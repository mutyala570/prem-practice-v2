"""
==============================================================
02 - COLLECTIONS: List, Tuple, Set, Dict
==============================================================

CONCEPT:
- LIST: ordered, mutable, allows duplicates — like JS arrays    []
- TUPLE: ordered, IMMUTABLE, allows duplicates                  ()
- SET: unordered, unique values only                            {}
- DICT: key-value pairs — like JS objects                       {key: val}
"""

# ---------------- EXAMPLE 1: List operations ----------------
print("=== Example 1: Lists ===")

fruits = ["apple", "banana", "mango"]
fruits.append("orange")         # add to end
fruits.insert(0, "grape")       # add at index
fruits.remove("banana")         # remove by value

print(f"Fruits: {fruits}")
print(f"First: {fruits[0]}")
print(f"Last: {fruits[-1]}")
print(f"Slice [1:3]: {fruits[1:3]}")
print(f"Length: {len(fruits)}")
print(f"Sorted: {sorted(fruits)}")


# ---------------- EXAMPLE 2: Dictionaries ----------------
print("\n=== Example 2: Dictionaries ===")

person = {
    "name": "Mutyala",
    "age": 30,
    "skills": ["Node.js", "Python", "AI"],
    "is_active": True
}

# Access
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")           # safer — returns None if missing
print(f"Email: {person.get('email', 'N/A')}")  # with default

# Modify
person["role"] = "AI Engineer"      # add new key
person["age"] = 31                  # update

# Iterate
for key, value in person.items():
    print(f"  {key} -> {value}")

# Keys & values
print(f"Keys: {list(person.keys())}")
print(f"Values: {list(person.values())}")


# ---------------- EXAMPLE 3: Sets & Tuples ----------------
print("\n=== Example 3: Sets & Tuples ===")

# Set — auto removes duplicates
numbers = [1, 2, 2, 3, 3, 4]
unique = set(numbers)
print(f"Unique: {unique}")

# Tuple — can't change
coordinates = (10.5, 20.3)
print(f"Coordinates: {coordinates}")
# coordinates[0] = 99  # ERROR — tuples are immutable


# ---------------- TRY IT YOURSELF ----------------
# 1. Create a list of 5 programming languages, sort them alphabetically
# 2. Build a dict representing yourself (name, age, skills)
# 3. Find unique words in: "the quick brown fox jumps over the lazy dog the fox"
