# Learning Status

**Purpose:** tracks Python + AI learning progress only. Agent build status lives in `03-status.md`.

**Read this file first when the user asks about learning or says "I'm studying X now".** Update at the end of every learning session.

---

## Current phase
- **Phase:** P0 — Python core — **NOT STARTED YET**
- **Last updated:** 2026-04-16
- User will signal when they begin. Do not push P1+ topics until P0 is underway.

---

## P0 — Python core (prerequisite for everything else)
Source: `AI_ENGINEER_ROADMAP.md` Phase 1, Week 1.

### Day 1–2: Python Basics
- [ ] Variables, data types (int, float, str, bool, None)
- [ ] Lists, tuples, sets, dictionaries
- [ ] Control flow: `if/elif/else`, `for`, `while`, comprehensions
- [ ] Functions: args, `*args`, `**kwargs`, default values, lambda
- [ ] f-strings
- [ ] Exception handling: `try/except/finally`, custom exceptions
- [ ] File I/O, `with` context manager
- [ ] Modules, imports, `pip`, `venv`

### Day 3–4: OOP in Python
- [ ] Classes, `__init__`, `self`
- [ ] Instance vs class vs static methods
- [ ] Inheritance, `super()`, MRO
- [ ] Dunder methods: `__str__`, `__repr__`, `__eq__`, `__len__`
- [ ] `@property`, getters/setters
- [ ] Abstract classes (`abc`)
- [ ] Dataclasses (`@dataclass`)
- [ ] Type hints (`typing`): `List`, `Dict`, `Optional`, `Union`, `Callable`

### Day 5–6: Async Python
- [ ] Sync vs async (transfers from Node.js)
- [ ] `async def`, `await`, coroutines
- [ ] `asyncio.run()`, `asyncio.gather()`, `asyncio.create_task()`
- [ ] `aiohttp` / `httpx` for async HTTP
- [ ] Async iterators, `async for`, `async with`

### Day 7: Python for AI ecosystem
- [ ] `pydantic` (critical for LLMs)
- [ ] `python-dotenv`
- [ ] `requests` / `httpx`
- [ ] Decorators & generators (used heavily in LangChain)

**P0 exit criteria:** can read and write a class with type hints, use `async/await`, and define a Pydantic model without looking at docs. Then P1 starts.

---

## P1 — Python for AI ecosystem (unblocks M1)
- [ ] Pydantic v2: `BaseModel`, `Field`, validators, `BaseSettings`
- [ ] FastAPI: routing, request/response models, dependencies, streaming
- [ ] `httpx.AsyncClient` patterns
- [ ] `structlog` structured logging
- [ ] Type hints: `Literal`, `TypedDict`, `Annotated`

---

## P2 — LangChain / LangGraph (unblocks M2–M5)
- [ ] LangChain LCEL recap (`|`, `RunnablePassthrough.assign`, `RunnableLambda`, `StrOutputParser`) — already seen in exercises
- [ ] `ChatPromptTemplate.from_messages` with system + few-shot
- [ ] `PydanticOutputParser` / `JsonOutputParser`
- [ ] `llm.bind_tools([...])` + tool-calling loop
- [ ] `@tool` decorator / `StructuredTool`
- [ ] LangGraph `StateGraph` — nodes, edges, conditional edges, checkpointers
- [ ] `trim_messages`, conversation summarization

---

## P3 — RAG (unblocks M3)
- [ ] What embeddings are + cosine similarity intuition
- [ ] OpenAI `text-embedding-3-small` vs local `bge-small` trade-off
- [ ] Chunking strategies: fixed-size, semantic, header-based, overlap
- [ ] Vector DBs: Chroma (dev), Qdrant/Pinecone (prod)
- [ ] Hybrid search (BM25 + dense)
- [ ] Reranking with cross-encoder
- [ ] Citations / chunk metadata

---

## P4 — Agent patterns (unblocks M5)
- [ ] ReAct (Thought → Action → Observation → repeat)
- [ ] Plan-and-Execute
- [ ] When to let LLM decide vs hard-code flow
- [ ] Stop conditions (max iterations, confidence thresholds)

---

## P5 — Security / Guardrails (unblocks M7)
- [ ] Prompt-injection defences (input quoting, dual-LLM)
- [ ] PII detection & scrubbing (Presidio or regex)
- [ ] Rate limiting (`slowapi` + Redis)
- [ ] Per-session cost caps
- [ ] JWT pass-through pattern for customer auth

---

## P6 — Evaluation (unblocks M8)
- [ ] Golden-set design
- [ ] LLM-as-judge prompts
- [ ] RAGAS metrics (faithfulness, context precision, answer relevance)
- [ ] Regression testing tied to prompt versions

---

## P7 — Observability (unblocks M8)
- [ ] LangSmith trace structure (spans, runs, datasets)
- [ ] Token / cost accounting per layer
- [ ] Latency percentiles per node

---

## P8 — Deploy (unblocks M9)
- [ ] Multi-stage Python Dockerfile
- [ ] Uvicorn + Gunicorn for prod
- [ ] Streaming responses (SSE / WebSocket)

---

## Exposure so far (ran examples, not studied yet)
- Ran prompt-chaining scripts: Groq, OpenAI, Ollama → `week-one/day-two/*.py`
- Ran multi-turn chat example → `week-one/day-two/prompt-multiturn.py`
- Seen `ChatPromptTemplate`, `RunnablePassthrough`, `RunnableLambda`, `StrOutputParser` in action

---

## How to update this file
- When the user says "started X" / "finished X" / "currently learning X", move the relevant boxes.
- When a phase is complete, note the date next to the phase header.
- If a topic is skipped (e.g. decided not to use LangSmith), strike it through and note why.
- Keep phase order — don't skip P0 to P2 without flagging it.
