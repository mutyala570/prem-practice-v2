# Patterns & Code Quality Standards

Follow these so every module looks the same and you don't have to re-learn the codebase each session. If we deviate, update this file — don't leave two conventions fighting each other.

---

## Project structure
- One folder per concern (`rag/`, `tools/`, `guardrails/`) — no god-files.
- Every folder has `__init__.py`.
- Entrypoints (FastAPI routes, CLI scripts) live at the top level, not nested deep.
- Tests mirror source layout: `tests/tools/test_orders.py` for `tools/orders.py`.

## Python
- **Version:** 3.11+.
- **Type hints everywhere** — functions without types fail review.
- **Pydantic v2 for every boundary** — tool I/O, agent state, API request/response. No raw dicts across module lines.
- **Async** for anything HTTP (tools, LLM calls). Use `httpx.AsyncClient`, not `requests`.
- **`pathlib.Path` over `os.path`.**

## LangChain / LCEL
- Use **LCEL pipes (`|`)** for composition — not hand-rolled loops.
- Know the three runnable primitives and use the right one:
  - `RunnablePassthrough()` — pass input through unchanged (identity)
  - `RunnablePassthrough.assign(k=chain)` — add a new key to an input dict
  - `RunnableLambda(fn)` — transform the value with a function
- End every sub-chain with an output parser (`StrOutputParser`, `PydanticOutputParser`). Never pipe raw `AIMessage` into the next chain.
- Use `llm.bind_tools([...])` for function calling — not prompt-engineered JSON.
- LangGraph: typed state (Pydantic), one responsibility per node, explicit edges.

## Prompts
- All prompts live in `prompts/*.yaml` — never inline in `.py` (exception: one-liners < 100 chars).
- Every prompt file has: `name`, `version`, `description`, `template`, `input_vars`, `model_recommended`.
- Use explicit roles (system/user/assistant) via `ChatPromptTemplate.from_messages`.
- Few-shot examples live beside the prompt in the same yaml.
- Bump `version` when you change a prompt — eval runs should be tied to a version.

## Secrets & config
- **Never** read secrets outside `config.py` / `llm.py`. No `os.getenv("OPENAI_API_KEY")` scattered in business logic.
- Pydantic `BaseSettings` for config — typed, validated, loaded from `.env`.
- `.env` is git-ignored (already done).
- Keys exposed in chat/logs must be rotated immediately.

## Error handling
- Fail fast at boundaries. Validate input at layer entry, not 5 functions deep.
- **Never catch bare `Exception:`** — catch the specific thing you expect.
- Tool errors → structured output: `{"ok": False, "error": "timeout", "retryable": True}`. Don't let exception text bubble into the LLM prompt.
- User-visible errors are friendly strings; internal errors are logged with stack trace.

## Logging
- `structlog` — one JSON line per event.
- Log every LLM call: model, prompt-version, input tokens, output tokens, cost, latency, trace_id.
- In prod, scrub PII before logging prompts/replies. In dev, full logging is fine.
- `print()` is for scripts, never library code.

## Testing
- Every tool has a unit test with a mocked HTTP client.
- Every prompt has a golden-output test (exact-match or judge-based).
- Intent classifier has a fixture set in `tests/fixtures/intent_cases.yaml`.
- `eval/run_eval.py` runs in CI on every push. Fail the build if pass-rate drops.

## Git
- Small commits per milestone. Message format: `<area>: <imperative>` — e.g. `tools: add get_order_status`.
- `.env`, `__pycache__/`, `.venv/` never committed.
- Every PR includes: what changed, why, how to test.

## Code-review checklist (before marking any task done)
- [ ] Types on all public functions
- [ ] Pydantic models at boundaries
- [ ] No secrets in code
- [ ] At least one test added/updated
- [ ] Logs the key events
- [ ] Matches existing patterns (grep for similar code first — don't invent a second convention)
- [ ] No commented-out code
- [ ] No TODO without a linked ticket or an explanatory comment

## Anti-patterns (actively avoid)
- Catching exceptions just to silence them.
- Printing instead of logging.
- Global mutable state (module-level dicts used as caches).
- Hard-coded API URLs — use config.
- LLM calls inside `__init__`.
- Passing raw dicts between chains instead of Pydantic models.
- "Temporary" hacks without a comment explaining the workaround.
- Stripping someone's chosen primitive (e.g. `RunnablePassthrough`) for a "cleaner" one without asking — fix the usage, don't swap the tool.
