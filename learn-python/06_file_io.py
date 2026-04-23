"""
==============================================================
06 - FILE I/O: reading, writing, JSON
==============================================================

CONCEPT:
- Use `with open(...)` — automatically closes the file
- Modes: 'r' read, 'w' write (overwrites), 'a' append, 'b' binary
- For JSON, use the `json` module
"""

import json
import os

# ---------------- EXAMPLE 1: Write & read text files ----------------
print("=== Example 1: Text Files ===")

# Write
with open("sample.txt", "w") as f:
    f.write("Hello Python!\n")
    f.write("I'm learning AI engineering.\n")
    f.write("Line 3\n")

# Read entire file
with open("sample.txt", "r") as f:
    content = f.read()
    print("Full content:")
    print(content)

# Read line by line (memory efficient for big files)
with open("sample.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(f"Line {i}: {line.strip()}")

# Append
with open("sample.txt", "a") as f:
    f.write("This line was appended\n")


# ---------------- EXAMPLE 2: JSON files ----------------
print("\n=== Example 2: JSON Files ===")

# Data to save
data = {
    "name": "Mutyala",
    "skills": ["Python", "Node.js", "AI"],
    "projects": [
        {"name": "Groq Chatbot", "status": "in-progress"},
        {"name": "RAG App", "status": "planned"}
    ]
}

# Write JSON
with open("profile.json", "w") as f:
    json.dump(data, f, indent=2)      # indent for pretty-print

print("Saved profile.json")

# Read JSON
with open("profile.json", "r") as f:
    loaded = json.load(f)

print(f"Loaded name: {loaded['name']}")
print(f"Skills: {loaded['skills']}")
print(f"First project: {loaded['projects'][0]['name']}")


# ---------------- Cleanup (optional) ----------------
# os.remove("sample.txt")
# os.remove("profile.json")


# ---------------- TRY IT YOURSELF ----------------
# 1. Save a list of your favorite movies to a JSON file and read it back
# 2. Write a function to count lines in any text file
# 3. Read sample.txt and print only lines containing the word "Python"
