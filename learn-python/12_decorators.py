"""
==============================================================
12 - DECORATORS & GENERATORS
==============================================================

CONCEPT:
DECORATORS:
- A function that wraps another function
- Used EVERYWHERE in Python (Flask/FastAPI routes, @property, @dataclass)
- Syntax: @decorator_name above a function

GENERATORS:
- Functions using `yield` that produce values lazily
- Memory efficient for large data
- LangChain uses these for streaming LLM responses
"""

import time
from functools import wraps


# ---------------- EXAMPLE 1: Simple decorator ----------------
print("=== Example 1: Timing Decorator ===")

def timer(func):
    """Measure how long a function takes."""
    @wraps(func)                                # preserves original function name
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  ⏱  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


@timer
def slow_function(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


result = slow_function(1_000_000)
print(f"Result: {result}")


# ---------------- EXAMPLE 2: Decorator with arguments ----------------
print("\n=== Example 2: Retry Decorator ===")

def retry(max_attempts: int = 3):
    """Retry a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator


attempt_count = 0

@retry(max_attempts=3)
def flaky_api_call():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionError("Network error")
    return "Success!"


print(flaky_api_call())


# ---------------- EXAMPLE 3: Generators ----------------
print("\n=== Example 3: Generators ===")

def count_up_to(n: int):
    """Generator that yields numbers one at a time."""
    i = 1
    while i <= n:
        yield i
        i += 1

# Lazy — values produced only when requested
gen = count_up_to(5)
print(f"Type: {type(gen)}")

for num in gen:
    print(f"  Got: {num}")


# Generator expression (like list comprehension but lazy)
squares_gen = (x ** 2 for x in range(10))
print(f"Gen sum: {sum(squares_gen)}")


# Real-world: reading huge files line by line
def read_large_file(path: str):
    """Won't load entire file into memory."""
    with open(path) as f:
        for line in f:
            yield line.strip()


# ---------------- EXAMPLE 4: Streaming LLM-like example ----------------
print("\n=== Example 4: Streaming (LLM-style) ===")

def stream_response(text: str):
    """Simulate streaming tokens like an LLM."""
    words = text.split()
    for word in words:
        yield word
        time.sleep(0.1)


print("  Streaming: ", end="")
for token in stream_response("Hello I am an AI assistant"):
    print(token, end=" ", flush=True)
print()


# ---------------- TRY IT YOURSELF ----------------
# 1. Write a `@log_calls` decorator that logs function name + args
# 2. Generator: yield Fibonacci numbers up to N
# 3. Decorator `@cache_result` that caches function results
