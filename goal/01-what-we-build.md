# Order & Logistics Support Agent — Build Plan

This is the authoritative spec for what we're building. When anything changes (scope, model, layers), update this file.

---

## 1. Goal & Success Criteria

### Use case
A customer-facing chat agent for Qwipo B2B customers. It handles:
- Order status ("where is my order #12345?")
- Delivery tracking ("when will it arrive?")
- Cancellation requests ("I want to cancel this order")
- Policy questions ("what's the return window?")
- Small-talk / greetings

### Inputs
- Natural-language text from the customer
- Implicit context: `customer_id` / auth token, `session_id`, conversation history

### Outputs
- Natural-language reply
- Structured metadata: intent classified, tools called, cost/tokens, citations
- Side-effects when required (e.g., initiate cancellation in `bms-order-service`)

### Success criteria — done when:
- [ ] Correctly routes ≥85% of a 50-query test set to the right intent
- [ ] Grounds every factual claim (order IDs, SLAs) in either a tool response or a RAG citation — **no hallucinated order data**
- [ ] Refuses out-of-scope and adversarial requests (account takeover attempts, PII fishing, prompt injection)
- [ ] Median latency < 3s, p95 < 8s
- [ ] Every turn is traced (LangSmith/Langfuse) with tokens + cost attached
- [ ] Offline eval harness runs 50 golden Q&A pairs and reports pass/fail
- [ ] Dockerized, deployable to staging

### Scope — v1
**In:** status lookup, tracking, cancellation *initiation*, policy Q&A, session-scoped memory.
**Out (deferred to v2+):** payments/refunds, vendor-side queries, multi-language, voice, long-term cross-session memory.

---

## 2. Architecture Layers

### Flow diagram (top-down)
```
user message
     ↓
[Guardrails — input]   PII scrub, prompt-injection check, rate limit
     ↓
[Intent / Routing]     classify → order_status | cancellation | policy_qa | small_talk | out_of_scope
     ↓
[Memory — retrieve]    conversation history (+ user profile, later)
     ↓
[Reasoning Loop — LangGraph/ReAct]
     ├─ [RAG]           policy docs (returns, shipping, SLA)
     └─ [Tooling]       order-service, logistics-service, customer-service
     ↓
[LLM Core]             synthesize reply from retrieved context + tool outputs
     ↓
[Guardrails — output]  validate schema, strip PII leaks, enforce tone
     ↓
[Observability]        log turn: intent, tools, tokens, cost, latency, trace_id
     ↓
reply
```

### 2.1 Intent / Routing Layer
**Purpose:** Classify the user's message into a known intent so downstream layers know what to do. Skip expensive retrieval/tool calls when not needed.

**Topics to learn:**
- Classification prompts (zero-shot, few-shot)
- Structured output with Pydantic (intent enum + confidence + extracted entities)
- When an LLM classifier is enough vs when to fine-tune a small model
- Handling ambiguous / multi-intent messages

**What we build:**
- `agent/agents/order_support/intent.py` — `classify_intent(message, history) -> IntentResult`
- Pydantic `IntentResult(intent: Literal[...], confidence: float, entities: dict)`
- Few-shot examples in `prompts/intent_few_shot.yaml`

---

### 2.2 Retrieval / RAG Layer
**Purpose:** Ground policy-type answers (shipping SLAs, return windows) in actual docs. No hallucinated policies.

**Topics to learn:**
- Embeddings — OpenAI `text-embedding-3-small` vs local `bge-small`
- Chunking strategies — fixed-size, semantic, header-based
- Vector DB — Chroma (local, easy) → Qdrant/Pinecone (prod)
- Hybrid search (dense + BM25)
- Reranking (cross-encoder)
- Context-window budgeting
- Citation tracking — so every claim links back to a chunk

**What we build:**
- `agent/agents/order_support/rag/ingest.py` — chunk & embed `data/policies/*.md` → Chroma
- `agent/agents/order_support/rag/retrieve.py` — `retrieve(query, k=4) -> list[DocChunk]`
- Eval: `eval/retrieval_eval.py` — precision@k on a labelled test set

---

### 2.3 Tooling Layer
**Purpose:** Call real Qwipo services. Without tools, the agent is a chat wrapper.

**Topics to learn:**
- LangChain `@tool` / `StructuredTool`
- Pydantic schemas for tool input & output
- Async tools (`httpx.AsyncClient`)
- Auth pass-through (customer token → downstream)
- Error handling: 4xx, 5xx, timeouts, retries
- Output size control — paginate or summarise before returning to the LLM

**What we build:**
- `tools/orders.py` — `get_order_status(order_id)`, `list_recent_orders(customer_id, limit)`
- `tools/logistics.py` — `get_tracking(order_id)`
- `tools/cancellation.py` — `initiate_cancellation(order_id, reason)` *(writes — guarded)*
- All inputs/outputs are Pydantic models. Tool errors are structured (`{ok, error, retryable}`), never raw exceptions.

---

### 2.4 Reasoning / Planning Layer
**Purpose:** Orchestrate the multi-step reasoning: read intent → decide tools → call them → reflect → reply.

**Topics to learn:**
- ReAct (Thought → Action → Observation → repeat)
- Plan-and-execute (full plan then execute)
- LangGraph state machines — typed state, nodes per stage
- LangChain `bind_tools()` + tool-calling loop
- Stop conditions: max iterations, confidence threshold
- When to hard-code flow vs let the LLM decide

**What we build:**
- `agent/agents/order_support/graph.py` — LangGraph `StateGraph` with nodes:
  - `classify_intent` → branches to `retrieve_context` / `call_tools` / `small_talk`
  - `call_tools` loops until the LLM emits no more tool_calls
  - `synthesize` produces the final reply
- Typed `AgentState` (Pydantic): `messages`, `intent`, `tool_outputs`, `retrieved_docs`, `final_reply`

---

### 2.5 Memory Layer
**Purpose:** Hold context across turns in a session (short-term). Optional cross-session memory for v2.

**Topics to learn:**
- Short-term: `MessagesPlaceholder`, trimming, summarization
- Long-term: per-user store (Redis / Postgres) for facts learned across sessions
- Context-window budgeting
- When to summarize vs truncate
- Separating conversation memory from tool-call history

**What we build:**
- `agent/agents/order_support/memory.py`
  - `ConversationMemory(session_id)` — in-memory for dev, Redis for prod
  - Auto-summarize when history length exceeds N turns
- Long-term store deferred to v2.

---

### 2.6 LLM Core
**Purpose:** The model that actually generates text. Choice affects cost, latency, quality.

**Topics to learn:**
- Trade-offs: Groq (fast + cheap) vs OpenAI (quality) vs Claude (long context + tool use) vs Ollama (free + private)
- Prompt engineering: system prompts, role framing, CoT, self-critique
- Structured output: JSON mode, function calling, Pydantic parsers
- Temperature per layer (0 for classification, ~0.3 for synthesis)
- Streaming for perceived latency

**What we build:**
- `agent/agents/order_support/llm.py` — factory `get_llm(task: "classify" | "synthesize" | "summarize")`
- Default routing: Groq for classify/summarize (cheap+fast), OpenAI/Claude for synthesize (quality)
- All model choices driven by config, not hard-coded

---

### 2.7 Guardrails
**Purpose:** Stop the agent from being jailbroken, leaking data, or blowing the cost budget.

**Topics to learn:**
- Prompt-injection defences — input filtering, quoting untrusted content, dual-LLM pattern
- Output validation — schema enforcement, PII scrubbing
- Rate limiting (per user, per session)
- Cost caps per session
- Basic red-teaming

**What we build:**
- `agent/agents/order_support/guardrails/input.py` — flag/strip injection attempts, cap message length
- `agent/agents/order_support/guardrails/output.py` — Pydantic-validated reply, PII scrub
- Hard limits: max 5 tool calls per turn, max 8K tokens total
- Unit tests with a known-jailbreak corpus

---

### 2.8 Observability & Evaluation
**Purpose:** Can't improve what you can't see. Every turn must be inspectable.

**Topics to learn:**
- LangSmith or Langfuse — spans per layer
- Metrics: latency, tokens, cost, tool-call count, intent accuracy
- LLM-as-judge
- Golden-dataset evals
- RAGAS for retrieval quality

**What we build:**
- LangSmith integration via env vars (traces every chain automatically)
- `eval/golden_set.yaml` — 50 Q&A pairs covering all intents + adversarial
- `eval/run_eval.py` — run golden set, report pass/fail + cost
- Dashboards (later): cost per intent, p95 latency per layer

---

## 3. Build Order (Milestones)

Each milestone is a stop-point — you can demo at the end of any.

| # | Milestone | Demo at the end | Rough effort |
|---|-----------|-----------------|--------------|
| M1 | **Skeleton** | FastAPI `/chat` echoes input through Groq LLM, with config + logging | 1 day |
| M2 | **Intent classifier** | `/chat` classifies into 5 intents, returns JSON with confidence | 1 day |
| M3 | **RAG on policies** | Policy questions answered with citations from indexed docs | 2 days |
| M4 | **Single tool** | Can answer "status of order #X" via a real `bms-order-service` call | 1 day |
| M5 | **Multi-tool agent loop** | LangGraph orchestrates intent → retrieve → tools → reply | 2–3 days |
| M6 | **Memory** | Multi-turn conversation works within a session | 1 day |
| M7 | **Guardrails** | Injection attempts blocked, PII scrubbed, cost capped | 1 day |
| M8 | **Observability + eval** | LangSmith traces live, golden-set eval ≥85% pass | 2 days |
| M9 | **Deploy** | Dockerized, running in staging, callable from a frontend | 2 days |

**Total:** ~2–3 weeks of focused work.

---

## 4. Topics Checklist — Who Owns What

### You own (hands-on — I explain / review)
- Writing each module's first-pass code
- Pydantic models for tools & state
- Prompts (I review)
- Integration with real Qwipo services (you have domain knowledge + access)
- Running evals, reading traces
- Deploy / infra

### I own (I draft — you review)
- Architecture decisions (model choice, vector DB) — I propose options + trade-offs, you pick
- LangChain/LangGraph wiring patterns
- Eval harness design
- Guardrails / injection defences
- Code review for correctness

### We decide together (no default)
- LLM choice per task
- Vector DB (Chroma dev → Pinecone/Qdrant prod?)
- Scope-creep questions ("should v1 include X?")

---

## 5. Deliverables

### Folder layout
```
ai-learning/
  goal/                    # plan + status (this directory)
  week-one/ ...            # learning exercises (existing)
  agent/                   # the real project
    app.py                 # FastAPI entrypoint
    config.py              # Pydantic BaseSettings
    agents/order_support/
      graph.py
      intent.py
      llm.py
      memory.py
      rag/
        ingest.py
        retrieve.py
      tools/
        orders.py
        logistics.py
        cancellation.py
      guardrails/
        input.py
        output.py
    prompts/               # versioned yaml
    data/policies/         # source docs for RAG
    eval/
      golden_set.yaml
      run_eval.py
    tests/
    Dockerfile
    requirements.txt
```

### End-to-end done-when example
```
POST /chat
{"message": "where is my order 12345?", "session_id": "abc"}

→
{
  "reply": "Your order #12345 shipped on Apr 14 and is out for delivery today, expected by 6 PM.",
  "intent": "order_status",
  "tools_used": ["get_order_status", "get_tracking"],
  "citations": [],
  "cost_usd": 0.0023,
  "latency_ms": 1840,
  "trace_id": "ls_abc123"
}
```
