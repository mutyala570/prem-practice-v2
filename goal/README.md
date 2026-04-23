# Where we are — start here

**Single-source dashboard.** If you ask me "where are we?" or "what's next?", I read this file first — not the whole `goal/` folder.

**Last updated:** 2026-04-16

---

## TL;DR current state

- **Project:** Order & Logistics Support Agent for Qwipo B2B customers
- **Phase:** **P0 — Python core learning — NOT STARTED YET**
- **Agent build:** **M0 (planning done) — blocked on P0**
- **Next action (user):** start Phase 1 of `AI_ENGINEER_ROADMAP.md`, then ping me
- **Next action (me, when unblocked):** M1 skeleton (FastAPI + Groq echo endpoint)

---

## Progress at a glance

### Learning (Python + AI)
| Phase | Topic | Status |
|-------|-------|--------|
| P0 | Python core | ⏳ not started |
| P1 | Pydantic v2, FastAPI, async, structlog | 🔒 blocked by P0 |
| P2 | LangChain / LangGraph | 🔒 blocked |
| P3 | RAG | 🔒 blocked |
| P4 | Agent patterns | 🔒 blocked |
| P5 | Guardrails / security | 🔒 blocked |
| P6 | Evaluation | 🔒 blocked |
| P7 | Observability | 🔒 blocked |
| P8 | Deploy | 🔒 blocked |

### Agent build (milestones)
| # | Milestone | Status |
|---|-----------|--------|
| M0 | Planning | ✅ done |
| M1 | Skeleton | 🔒 blocked on P0/P1 |
| M2 | Intent classifier | 🔒 blocked |
| M3 | RAG on policies | 🔒 blocked |
| M4 | Single tool | 🔒 blocked |
| M5 | Multi-tool agent loop | 🔒 blocked |
| M6 | Memory | 🔒 blocked |
| M7 | Guardrails + Auth + Escalation | 🔒 blocked |
| M8 | Observability + Eval | 🔒 blocked |
| M9 | Deploy | 🔒 blocked |

---

## Which file answers which question?

| If the user asks… | Read this file |
|-------------------|----------------|
| "where are we?" / "what's next?" / "status?" | **This file first.** Only dive deeper if needed. |
| "what are we building?" / "what's the spec?" | `01-what-we-build.md` |
| "how should I write this code?" / "what's the pattern for X?" | `02-patterns-and-code-quality.md` |
| "which milestones are done?" / "what's the next milestone?" | `03-status.md` |
| "which topics have I studied?" / "update my learning progress" | `04-learning-status.md` |
| "explain layer X" / "remind me what RAG does" | `05-layers-reference.md` |
| "what's my skill gap?" / "what do I need to learn?" | `my-req.md` |

---

## Open decisions (resolve before the milestone that needs them)
- [ ] **Vector DB (dev)** — Chroma vs Qdrant? → before M3
- [ ] **Primary LLM (synthesis)** — Groq vs OpenAI vs Claude? → before M5
- [ ] **Observability tool** — LangSmith vs Langfuse? → before M8
- [ ] **Final intent list** — confirm draft `order_status | cancellation | policy_qa | small_talk | out_of_scope` → before M2

## Open questions for user
- Dev/staging access to `bms-order-service` & `logistics-*`, or mock for M4?
- Shared auth pattern across Qwipo services for `customer_id` token?
- Policy-doc location (Confluence / markdown / PDFs / Notion)?

---

## How to keep this file cheap

Update only these fields at the end of each session:
- `Last updated` at top
- `TL;DR current state` (1–3 lines)
- `Progress at a glance` checkboxes
- `Open decisions` / `Open questions` if any resolved

Everything else lives in the detail files. Do NOT paste long explanations here.
