"""
==============================================================
10 - ASYNC: async/await, asyncio
==============================================================

CONCEPT:
- Very similar to Node.js async/await
- `async def` = coroutine (like async function in JS)
- `await` pauses the coroutine until the awaitable completes
- `asyncio.run()` = entry point (like top-level await)
- `asyncio.gather()` = run multiple coroutines in parallel (like Promise.all)

WHY IT MATTERS FOR AI:
LLM API calls are slow (1-10s). Async lets you call multiple LLMs,
embed many docs, or handle many requests concurrently.
"""

import asyncio
import time


# ---------------- EXAMPLE 1: Basic async ----------------
async def fetch_data(name: str, delay: float) -> str:
    print(f"  → Fetching {name}...")
    await asyncio.sleep(delay)             # non-blocking sleep
    print(f"  ✓ Got {name}")
    return f"Data from {name}"


async def main_sequential():
    """Sequential — slow. Total time = sum of all."""
    print("=== Example 1: Sequential ===")
    start = time.time()

    r1 = await fetch_data("API-1", 2)
    r2 = await fetch_data("API-2", 2)
    r3 = await fetch_data("API-3", 2)

    elapsed = time.time() - start
    print(f"Results: {[r1, r2, r3]}")
    print(f"Total time: {elapsed:.2f}s (sequential)\n")


# ---------------- EXAMPLE 2: Parallel with gather ----------------
async def main_parallel():
    """Parallel — fast. Total time = max of all."""
    print("=== Example 2: Parallel (gather) ===")
    start = time.time()

    results = await asyncio.gather(
        fetch_data("API-1", 2),
        fetch_data("API-2", 2),
        fetch_data("API-3", 2),
    )

    elapsed = time.time() - start
    print(f"Results: {results}")
    print(f"Total time: {elapsed:.2f}s (parallel)\n")


# ---------------- EXAMPLE 3: Real HTTP calls with httpx ----------------
# Install first: pip install httpx
async def fetch_url(url: str):
    """Uncomment if you install httpx.
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code, len(response.text)
    """
    pass


# ---------------- RUN ----------------
async def run_all():
    await main_sequential()
    await main_parallel()


if __name__ == "__main__":
    asyncio.run(run_all())


# ---------------- TRY IT YOURSELF ----------------
# 1. Create 5 async functions with different delays, run them in parallel
# 2. Install httpx (`pip install httpx`) and fetch 3 URLs in parallel
# 3. Time sequential vs parallel — observe the difference
