# Agent Layers — Reference Guide

Quick-lookup doc for *me* (Prem). Read when I need to recall what each layer does, why it exists, and which milestone builds it. Not the spec — just the mental map.

Authoritative spec: `01-what-we-build.md`. Standards: `02-patterns-and-code-quality.md`. This file is learning-oriented.

---

## 1. The mapping table

| # | Layer | Built in | What that milestone adds |
|---|-------|----------|--------------------------|
| 1 | **Auth / Identity / Authorization** | **M7** | Customer JWT pass-through; verify order ownership before tool calls |
| 2 | **Input Guardrails** | **M7** | PII scrub, injection check, length + rate limits |
| 3 | **Intent / Routing** | **M2** | Classifier → branches to retrieve / tool / small-talk |
| 4 | **Memory** | **M6** | Session-scoped conversation history |
| 5 | **Retrieval / RAG** | **M3** | Embed + retrieve policy docs with citations |
| 6 | **Tooling** | **M4 → M5** | M4 = first tool (`get_order_status`); M5 = multi-tool loop |
| 7 | **Reasoning / Planning** | **M5** | LangGraph state machine orchestrates the flow |
| 8 | **LLM Core** | **M1 → grows in every milestone** | M1 wires Groq; later milestones add per-task routing |
| 9 | **Output Guardrails** | **M7** | Reply schema validation, PII-leak scrub |
| 10 | **Human Escalation / Handoff** | **M7** | Fallback for low-confidence or high-stakes intents |
| 11 | **Observability (tracing)** | **M8** | LangSmith traces + token/cost/latency metrics |
| 12 | **Evaluation (offline)** | **M8** | Golden set + LLM-as-judge + RAGAS |

**Plumbing (not a layer):**
- **M1 Skeleton** — FastAPI + config + `structlog`. The scaffold everything plugs into.
- **M9 Deploy** — Dockerfile + Uvicorn + streaming. Packaging, not logic.

---

## 2. Data flow through the layers (top-down)

```
user HTTP request
     ↓
[1] Auth — is this a real customer? what's their customer_id?
     ↓
[2] Input Guardrails — strip PII, block injection, rate-limit
     ↓
[3] Intent classifier — which branch?
     ↓
[4] Memory — load this session's history
     ↓
[7] Reasoning loop (LangGraph) — decides: retrieve? tools? both?
     ├─ [5] RAG — pulls relevant policy chunks
     └─ [6] Tools — calls real Qwipo services (with customer_id from step 1)
     ↓
[8] LLM Core — synthesizes reply from retrieved context + tool outputs
     ↓
[9] Output Guardrails — reply matches schema? no leaked PII?
     ↓
[10] Escalation check — confidence low? high-stakes action? → human handoff
     ↓
[11] Observability — log trace, tokens, cost, latency
     ↓
reply
```
*(Evaluation (#12) is offline — runs separately, not on live traffic.)*

---

## 3. Layer-by-layer explanation

### [1] Auth / Identity / Authorization *(M7)*
**What:** Figure out *who* is asking and *what they're allowed to see*.
**Why it matters:** A customer asking about order #12345 — is that their order? Without this check, any logged-in user can read anyone's orders. This is not a "nice to have"; it's a data-leak risk.
**Key ideas:** JWT validation, `customer_id` extraction, pass-through to downstream Qwipo services, row-level authorization (is this order owned by this customer?).
**Will live in:** FastAPI dependency + `tools/*` (each tool checks ownership).

### [2] Input Guardrails *(M7)*
**What:** Clean and validate the raw user message before the LLM sees it.
**Why it matters:** Users can paste 50KB of text, try prompt injections ("ignore previous instructions…"), or accidentally include PII in the message. Filtering at the boundary is cheaper than filtering after the LLM.
**Key ideas:** length cap, rate limit per user, simple injection heuristics, PII scrub (emails, phone numbers) before logging.
**Will live in:** `guardrails/input.py` — runs before the graph.

### [3] Intent / Routing *(M2)*
**What:** Classify the user's message into one of our known intents so downstream layers know what to do.
**Why it matters:** Running RAG + 5 tool calls for every "hi" is wasteful. Classifying first lets us short-circuit: greetings skip retrieval, policy questions skip tools, etc.
**Key ideas:** Few-shot classification prompt, Pydantic enum output, confidence score, entity extraction (pull order_id out of the message).
**Will live in:** `intent.py` with a `classify_intent()` function returning `IntentResult`.

### [4] Memory *(M6)*
**What:** Keep track of what's been said in this conversation.
**Why it matters:** "When will it arrive?" only makes sense if the agent remembers which order we were discussing. Without memory, every turn is independent — bad UX.
**Key ideas:** Short-term (`MessagesPlaceholder` + `trim_messages`), auto-summarize when long, separate store for long-term facts (deferred to v2).
**Will live in:** `memory.py` — in-memory dev, Redis for staging/prod.

### [5] Retrieval / RAG *(M3)*
**What:** When the user asks a policy/FAQ question, fetch relevant chunks from indexed docs so the LLM can quote them instead of hallucinating.
**Why it matters:** LLMs will confidently make up SLAs, return windows, policies. RAG forces answers to come from *your* docs — with citations.
**Key ideas:** Chunk the docs → embed → store in vector DB (Chroma) → at query time, embed the question → top-k nearest chunks → stuff into prompt.
**Will live in:** `rag/ingest.py` (one-time indexing) + `rag/retrieve.py` (runtime lookup).

### [6] Tooling *(M4 → M5)*
**What:** Let the LLM call real functions — `get_order_status()`, `get_tracking()`, `initiate_cancellation()` — to fetch/write real data.
**Why it matters:** Without tools, the agent only knows what's in its prompt. Tools connect it to live Qwipo services.
**Key ideas:** Pydantic schemas for tool inputs/outputs (so the LLM knows the shape), `@tool` decorator, async HTTP, structured error returns (`{ok: False, error, retryable}`), auth pass-through.
**Will live in:** `tools/orders.py`, `tools/logistics.py`, `tools/cancellation.py`.

### [7] Reasoning / Planning *(M5)*
**What:** The "agent brain." Decides: which tools to call, in what order, when to stop, how to combine tool outputs + RAG chunks into the final reply.
**Why it matters:** Multi-step tasks ("check status AND tracking AND answer a policy question in one turn") can't be hard-coded — the LLM has to plan.
**Key ideas:** LangGraph state machine with typed `AgentState`. ReAct pattern (Thought → Action → Observation → repeat). Stop conditions (max 5 iterations).
**Will live in:** `graph.py` — the nodes & edges that form the agent's flow.

### [8] LLM Core *(M1, grows throughout)*
**What:** The actual LLM that generates text. Plus the prompt-engineering around it.
**Why it matters:** Model choice = big lever on cost, latency, quality. Using GPT-4 for intent classification is wasteful; using Groq for nuanced customer replies may feel robotic.
**Key ideas:** `get_llm(task=...)` factory returns the right model. Temperature per task (0 for classify, 0.3 for synthesis). System prompts in yaml, versioned.
**Will live in:** `llm.py` + `prompts/*.yaml`.

### [9] Output Guardrails *(M7)*
**What:** Validate the LLM's reply before sending it to the user.
**Why it matters:** The LLM might leak a raw error message, echo PII it pulled from a tool, or answer in wrong JSON shape. Catch it at the exit.
**Key ideas:** Pydantic schema enforcement on the reply, PII-leak scrub (don't repeat customer's phone # back to them), tone/length checks.
**Will live in:** `guardrails/output.py` — runs after the graph, before HTTP response.

### [10] Human Escalation / Handoff *(M7)*
**What:** When the agent shouldn't or can't answer — route to a human.
**Why it matters:** Agents that try to handle *everything* end up hallucinating in edge cases. A clean fallback is safer.
**Key ideas:** Triggers = low intent-classification confidence, explicit "talk to human", high-stakes actions (e.g. cancel order > ₹50K), tool repeat-failures.
**Will live in:** `graph.py` as a terminal node that posts to your support queue + replies "connecting you to a human."

### [11] Observability (tracing) *(M8)*
**What:** See inside every agent run — what was the input, which branches taken, which tools called with what args, what tokens/cost per step.
**Why it matters:** Debugging a "bad answer" without traces = impossible. With LangSmith, you see exactly which prompt, which retrieval, which tool call produced it.
**Key ideas:** LangSmith auto-traces LangChain chains if env vars set. Custom spans for non-LangChain code. Tag every run with `session_id`, `customer_tier`, `intent`.
**Will live in:** `.env` config + minor wiring in `app.py`.

### [12] Evaluation (offline) *(M8)*
**What:** Run the agent against a frozen test set of Q&A pairs, score pass/fail. Regression-test prompts before shipping.
**Why it matters:** If you tweak a prompt and don't eval, you won't know it broke 5 other intents until users complain. Evals turn "vibes-based" iteration into data-driven.
**Key ideas:** Golden-set = 50 curated Q&A pairs with expected intent, expected tools, ideal reply. LLM-as-judge scores each reply. RAGAS for retrieval quality (faithfulness, context precision).
**Will live in:** `eval/golden_set.yaml` + `eval/run_eval.py`. Run on every PR.

---

## 4. Milestone-by-milestone explanation

### M1 — Skeleton *(plumbing, builds Layer 8 basic)*
FastAPI app with `POST /chat`. Config via Pydantic `BaseSettings` (reads `.env`). `structlog` JSON logging. Endpoint passes user message to Groq, returns the reply. **No agent logic yet** — just scaffolding.

### M2 — Intent classifier *(builds Layer 3)*
Add an `intent.py` module. `/chat` now classifies the message first, returns `{intent, confidence, entities, reply}`. Covers all 5 intents with few-shot examples.

### M3 — RAG on policies *(builds Layer 5)*
Ingest policy markdown → Chroma vector DB. When intent is `policy_qa`, retrieve top-k chunks and stuff them into the prompt. Replies include citations.

### M4 — Single tool *(builds Layer 6 — part 1)*
Implement `get_order_status(order_id)` as an async httpx call to `bms-order-service`. Wire it so `order_status` intent triggers the tool. Handle 404, 500, timeout as structured errors.

### M5 — Multi-tool agent loop *(builds Layers 6 + 7)*
Convert the flow into LangGraph. Add `get_tracking`, `initiate_cancellation`. The LLM decides which tools to call via `bind_tools`. Loop until no more tool_calls. Typed `AgentState` throughout.

### M6 — Memory *(builds Layer 4)*
Add session memory. Multi-turn works: "where's order 123?" → "when will it arrive?" resolves correctly. Auto-summarize when history exceeds N turns.

### M7 — Guardrails + Auth + Escalation *(builds Layers 1, 2, 9, 10)*
Four protective layers in one milestone:
- **Auth:** FastAPI dependency extracts `customer_id` from JWT; tool calls pass it through; ownership check per tool.
- **Input guardrails:** length cap, rate limit, injection check, PII scrub.
- **Output guardrails:** Pydantic schema on reply, PII-leak scrub.
- **Escalation:** fallback node triggers on low confidence / high-stakes / "talk to human."

### M8 — Observability + Evaluation *(builds Layers 11 + 12)*
- **Obs:** LangSmith integration, traces every run, metrics dashboard.
- **Eval:** 50-pair golden set + `run_eval.py` with LLM-as-judge + RAGAS.

### M9 — Deploy *(plumbing)*
Multi-stage Dockerfile, Uvicorn config, streaming responses. Push to staging, verify end-to-end.

---

## 5. Quick mental model

If you can remember just three things:

1. **The 4 protective layers (1, 2, 9, 10)** all land in M7 — they surround the "thinking" layers.
2. **The 4 thinking layers (3, 5, 6, 7)** map to M2, M3, M4–M5, M5 — this is the core agent work (M2–M5).
3. **LLM Core (8) is everywhere**, Memory (4) is M6, Obs + Eval (11, 12) are M8.

```
M1  = scaffold
M2–M5 = think (intent, RAG, tools, reasoning)
M6    = remember
M7    = protect (auth, in-guard, out-guard, escalate)
M8    = observe + evaluate
M9    = ship
```

---

## 6. Related files
- `01-what-we-build.md` — full spec (layers described in more depth)
- `02-patterns-and-code-quality.md` — how to implement each layer cleanly
- `03-status.md` — which milestones are done
- `04-learning-status.md` — which topics I've studied
- `my-req.md` — my skill gap against each layer
