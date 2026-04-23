# My Requirements — Skill Audit + Full Layer List

This file is *my* (Prem's) view of the project: what I bring, what I need to learn, and the complete layer list we've agreed on. Read alongside `01-what-we-build.md` (spec), `02-patterns-and-code-quality.md` (standards), `03-status.md` (progress).

---

## 1. Project target (one line)
Build an **Order & Logistics Support Agent** for Qwipo B2B customers — handles order status, tracking, cancellation, policy Q&A. Full spec in `01-what-we-build.md`.

---

## 2. My existing skills (what I bring to the project)

### Strong
- **Node.js / TypeScript** — primary language, several years
- **Microservices architecture** — built & operate 20+ services (`bms-*`) at Qwipo
- **REST API design** — I've designed most of our service contracts
- **PostgreSQL + DB modelling**
- **Git / CI-CD (Azure Pipelines) / Docker**
- **Angular / React** — full-stack frontend
- **ONDC integration** — deep domain knowledge of B2B commerce
- **Production debugging** — logs, traces, on-call

### Exposure so far (ran example scripts only — not yet studied)
- Ran prompt-chaining examples with Groq / OpenAI / Ollama (`week-one/day-two/*.py`)
- Saw `ChatPromptTemplate`, `RunnablePassthrough`, `RunnableLambda`, `StrOutputParser` in action
- Used `python-dotenv` for the `.env`
- Seen multi-turn with `MessagesPlaceholder` + `chat_history`
- *Not* yet worked through Python syntax/idioms properly — will start soon

### Transfers from Node/TS (same concept, new syntax)
- Async programming (Python `async/await` ≈ Node Promises)
- HTTP clients (`httpx` ≈ `axios`)
- JSON handling, env-based config
- Dependency management (`pip`/`requirements.txt` ≈ `npm`/`package.json`)

---

## 3. Skills I need to acquire (what we'll learn as we build)

Mapped to the layer that needs it.

### Foundations — Python itself (BLOCKS EVERYTHING — not started)
- Python core: variables, data types, lists/dicts/sets, control flow
- Functions (args, `*args`, `**kwargs`, lambda)
- OOP: classes, `__init__`, inheritance, dataclasses
- Modules, imports, virtual envs (`venv`)
- Exception handling, file I/O, `with` context manager
- Decorators & generators (used heavily in LangChain)
- Follow `AI_ENGINEER_ROADMAP.md` Phase 1 (Week 1) before anything else

### Foundations — Python ecosystem for AI (blocks M1, after Python basics)
- **Pydantic v2** — `BaseModel`, `Field`, validators, `BaseSettings` → *every boundary*
- **FastAPI** — routing, dependencies, request/response models, streaming
- **Async Python** — `asyncio`, `asyncio.gather`, `httpx.AsyncClient`
- **structlog** — structured JSON logging
- **Type hints** — `Literal`, `TypedDict`, `Union`, `Optional`, `Annotated`

### LangChain / LangGraph (blocks M2–M5)
- `LangGraph.StateGraph` — nodes, edges, conditional edges, checkpointers
- `llm.bind_tools([...])` + tool-calling loop
- `@tool` decorator / `StructuredTool` with Pydantic args
- `PydanticOutputParser` / `JsonOutputParser`
- `trim_messages`, conversation summarization

### RAG concepts (blocks M3)
- Embeddings — cosine similarity, `text-embedding-3-small` vs `bge-small`
- Chunking strategies — fixed-size, semantic, header-based, overlap
- Vector DBs — Chroma (dev), Qdrant/Pinecone (prod)
- Hybrid search (BM25 + dense)
- Reranking (cross-encoder)
- Citation / chunk-metadata plumbing

### Agent patterns (blocks M5)
- **ReAct** — Thought → Action → Observation → repeat
- **Plan-and-Execute** — full plan first, then execute
- When to let the LLM decide vs hard-code flow
- Stop conditions (max iterations, confidence)

### Security / Guardrails (blocks M7)
- Prompt-injection defences — input quoting, dual-LLM pattern
- PII detection & scrubbing (Presidio or simple regex first)
- Rate limiting (`slowapi` + Redis)
- Per-session cost caps
- **Auth pass-through** — customer JWT → tool calls → downstream services *(I know the Qwipo side; need the Python glue)*

### Evaluation (blocks M8)
- Golden-set design (input → expected intent/tool/reply)
- LLM-as-judge prompts
- RAGAS metrics — faithfulness, context precision, answer relevance
- Regression testing tied to prompt versions

### Observability (blocks M8)
- LangSmith trace structure — spans, runs, datasets
- Token/cost accounting per layer
- Latency percentiles per node

### Deploy (blocks M9)
- Multi-stage Python Dockerfile
- Uvicorn + Gunicorn for prod
- Streaming responses (SSE / WebSocket)

---

## 4. Complete agent-layer list (final — superset of `01-what-we-build.md`)

Following our discussion, adding **Auth** and **Human Escalation** as distinct layers, and splitting **Evaluation** from **Observability**.

| # | Layer | Why distinct | Covered in `01-what-we-build.md`? |
|---|-------|--------------|-----------------------------------|
| 1 | **Auth / Identity / Authorization** | Security-critical. Must verify customer owns order #X before any tool call. | Missing — ADD |
| 2 | **Input Guardrails** | PII scrub, injection check, length + rate limit on raw input | Yes (§2.7) |
| 3 | **Intent / Routing** | Classify message → branch cheaply | Yes (§2.1) |
| 4 | **Memory** | Conversation history + session state | Yes (§2.5) |
| 5 | **Retrieval / RAG** | Ground policy Q&A in docs | Yes (§2.2) |
| 6 | **Tooling** | Real Qwipo service calls | Yes (§2.3) |
| 7 | **Reasoning / Planning** | Orchestrate intent → retrieve → tools → reply | Yes (§2.4) |
| 8 | **LLM Core** | Model choice + prompting | Yes (§2.6) |
| 9 | **Output Guardrails** | Schema validation, PII-leak scrub, tone | Yes (§2.7) |
| 10 | **Human Escalation / Handoff** | Fallback for low-confidence / high-stakes / "talk to human" | Missing — ADD |
| 11 | **Observability (tracing)** | Live-traffic traces, token/cost/latency logging | Yes (§2.8 — split) |
| 12 | **Evaluation (offline)** | Golden-set + LLM-as-judge regression tests | Yes (§2.8 — split) |

**Deferred to v2:** caching (LLM response + embedding), long-term cross-session memory, multi-language, voice, vendor-side queries.

---

## 5. Tech stack (proposed — needs sign-off)

| Concern | Choice | Notes |
|---------|--------|-------|
| Language | Python 3.11+ | matches roadmap |
| Agent framework | LangChain + LangGraph | LangGraph for the state machine |
| Validation | Pydantic v2 | every boundary |
| API | FastAPI + Uvicorn | async by default |
| HTTP client | `httpx.AsyncClient` | async tool calls |
| Logging | `structlog` | JSON lines |
| Vector DB (dev) | **DECIDE:** Chroma vs Qdrant | — |
| Vector DB (prod) | **DECIDE:** Qdrant vs Pinecone | — |
| Primary LLM (synthesis) | **DECIDE:** Groq vs OpenAI vs Claude | — |
| Classifier LLM | Groq (cheap, fast) | default |
| Embeddings | **DECIDE:** OpenAI vs local bge | — |
| Tracing | **DECIDE:** LangSmith vs Langfuse | — |
| State / rate limit | Redis | v1.5 |
| Containerization | Docker + docker-compose | matches your stack |
| CI/CD | Azure Pipelines | matches Qwipo pattern |

---

## 6. Realistic timeline (given my skill gap)

Part-time (~2 hrs/day):

| Phase | Duration | Focus |
|-------|----------|-------|
| **P0 — Python core** | 1–2 weeks | Phase 1 of `AI_ENGINEER_ROADMAP.md` — NOT STARTED YET |
| **P1 — Python for AI** | 3–4 days | Pydantic v2, FastAPI, async, structlog |
| P2 — M1 skeleton + M2 intent | 3–4 days | LangChain structured output + FastAPI endpoint |
| P3 — M3 RAG | ~1 week | Embeddings, chunking, Chroma |
| P4 — M4 single tool + M5 agent loop | ~1 week | Async httpx, LangGraph, tool-calling |
| P5 — M6 memory + M7 guardrails + Auth | ~1 week | Redis, PII scrub, JWT pass-through |
| P6 — M8 obs + eval + M9 deploy | ~1 week | LangSmith, RAGAS, Docker, Uvicorn |

**~6–7 weeks part-time** including Python ramp-up. ~4 weeks full-time.

> Agent work (P1 onward) does **not** start until Python core (P0) is done. No point writing Pydantic models without understanding classes first.

---

## 7. Pre-reads (do before writing M1 code, ~3 hrs total)

- [ ] Pydantic v2 migration + `BaseSettings` docs — 30 min
- [ ] FastAPI tutorial "First steps" + "Request body" — 45 min
- [ ] LangGraph quickstart + one example — 60 min
- [ ] LangChain "tool calling" guide — 30 min
- [ ] Skim "Prompt Injection Primer" (Simon Willison) — 20 min

---

## 8. Still-open questions (copied from `03-status.md` so this file is self-contained)

- [ ] Dev/staging access to `bms-order-service` and `logistics-*`, or mock HTTP for M4?
- [ ] Shared auth pattern across Qwipo services for passing `customer_id` token?
- [ ] Where do policy docs live today — Confluence, markdown, PDFs, Notion?
- [ ] Primary LLM choice (OpenAI billing needs to be sorted if we pick it)
- [ ] Vector DB choice for dev
- [ ] Tracing tool choice

---

## 9. What "success" looks like for me personally

Beyond the agent working, by the end of this project I want to be able to:
- Design a multi-layer agent from scratch for a new use case
- Debug a bad agent output by reading traces & eval results, not by guessing
- Choose the right LLM / vector DB / framework for a given problem, with reasons
- Explain prompt-injection + PII risks to a non-technical PM
- Own end-to-end: spec → code → eval → deploy → observe → iterate
