# Agent Build Status

**Purpose:** tracks the Order & Logistics Support Agent build only. Python / AI learning progress lives in `04-learning-status.md`.

**Read this file first when resuming build work.** Update at the end of every build session.

---

## Current phase
- **Milestone:** M0 — Planning complete
- **Status:** Blocked on P0 (Python core). See `04-learning-status.md`.
- **Last updated:** 2026-04-16

## Completed
- [x] Agent choice decided → **Order & Logistics Support Agent**
- [x] Build plan → `goal/01-what-we-build.md`
- [x] Code-quality standards → `goal/02-patterns-and-code-quality.md`
- [x] Skill audit → `goal/my-req.md`
- [x] `.env` + `.gitignore` at project root

## Milestone board
| # | Milestone | Status | Notes |
|---|-----------|--------|-------|
| M1 | Skeleton (FastAPI `/chat` + Groq LLM) | Not started | Blocked on P0 |
| M2 | Intent classifier | Not started | — |
| M3 | RAG on policies | Not started | — |
| M4 | Single tool (`get_order_status`) | Not started | Needs `bms-order-service` access |
| M5 | Multi-tool agent loop (LangGraph) | Not started | — |
| M6 | Memory | Not started | — |
| M7 | Guardrails + Auth | Not started | — |
| M8 | Observability + Eval | Not started | — |
| M9 | Deploy | Not started | — |

## In progress
- _Nothing — blocked on Python learning. Resume when `04-learning-status.md` shows P0 far enough along._

## Next step (when P0 unblocks)
**M1 — Skeleton**
1. Create `agent/` folder per `01-what-we-build.md` §5
2. `config.py` — Pydantic `BaseSettings` + `structlog`
3. `app.py` — FastAPI `POST /chat` → Groq LLM
4. Acceptance:
   ```
   curl -X POST localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "hi", "session_id": "test"}'
   ```
   returns an LLM reply; one JSON log event emitted.

## Open decisions (need to resolve before the milestone that needs them)
- [ ] **Vector DB for dev:** Chroma vs Qdrant? — blocks M3
- [ ] **Primary LLM for synthesis:** Groq vs OpenAI vs Claude? — blocks M5
- [ ] **Observability tool:** LangSmith vs Langfuse? — blocks M8
- [ ] **Final intent list:** draft `order_status | cancellation | policy_qa | small_talk | out_of_scope` — confirm before M2

## Open questions for user
- Dev/staging `bms-order-service` access, or mock HTTP for M4?
- Shared auth pattern across Qwipo services for `customer_id` token?
- Policy-doc location (Confluence / markdown / PDFs / Notion)? — blocks M3

## Blockers
- **P0 (Python core) not started.** See `04-learning-status.md`.

## Artifacts
- `goal/01-what-we-build.md` — plan
- `goal/02-patterns-and-code-quality.md` — standards
- `goal/my-req.md` — skill audit
- `goal/03-status.md` — this file (agent build)
- `goal/04-learning-status.md` — learning progress

---

## How to resume a build session
1. Read `04-learning-status.md` — is P0 far enough along to unblock?
2. Read this file top to bottom.
3. Re-read `01-what-we-build.md` if scope feels unclear.
4. Start at "Next step". No re-planning unless something changed.
5. At end of session: update "Milestone board" + "In progress" + "Next step" + "Last updated".
