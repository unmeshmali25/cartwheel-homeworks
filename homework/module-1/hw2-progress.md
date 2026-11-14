# Homework 2 progress

Interactive walkthrough of `homework/module-1/hw2.md`.

## Deliverables checklist

- [x] `observability/instrument.py` (Part A — tool span attributes)
- [x] `server/app.py` — `create_session` (Part B)
- [x] `server/app.py` — `post_message` (Part C)
- [x] `tests/test_observability.py` (Part D)
- [x] Langfuse inspection + ≥5 requests from `hw1-session.jsonl` (Part E)
  - [x] ≥5 live requests sent (1 earlier + 4 today)
  - [x] Student inspected merchant 4127 tool span (`permission_denied=true`, role/user/store set)
- [x] Two prompt versions compared (Part F)
- [x] `hw2-traces.json` (exactly two traces)
- [ ] Video (student records; deferred to later — not blocking HW3)

## Done

- Step 1: Core ideas — trace, span, `gen_ai.*` vs `cartwheel.*`, server identity, prompt versioning.
- Step 2: `_set_permission_denied_attributes` in `observability/instrument.py`.
- Step 3: `record_tool_result` — Part A complete.
- Step 4: `create_session` — Part B complete.
  - Offline check: `uv run pytest --runxfail -vv tests/test_hw_holes.py -k "create_session_binds"` → 1 passed.
- Step 5: `post_message` — Part C complete (root span + auth + prompt version).
- Step 6: Part D auth tests — complete.
  - Offline: `uv run pytest --runxfail tests/test_hw_holes.py -k hw2` → 1 passed
  - Offline: `uv run pytest tests/test_observability.py` → 2 passed
  - Offline: full `uv run pytest` → 149 passed, 4 skipped, 18 xfailed, 9 xpassed

- Step 7: Restored `LANGFUSE_*` in `.env` for local Langfuse. `TRACELOOP_TRACE_CONTENT=true` already set.
- Step 8: Langfuse Docker Compose stack is up (`docker compose -f observability/docker-compose.yml up -d`).
- Step 9: Agent server running on port 8010 (`uv run uvicorn server.app:app --port 8010`).
- Step 10: First live traced request (shopper 1, "Show my recent orders.")
  - `session_id`: `770f104858e549b48f4be9ce291b7b44`
  - `prompt_version`: `4e777f3bf61a`
  - Reply listed recent orders (live model).
- Step 11: Student confirmed the trace in Langfuse (root + tool spans).

- Step 12: Sent 4 more live Part E requests (total ≥5). All `prompt_version=4e777f3bf61a`.
  - shopper 1: order 4127 details
  - merchant 9002: order 4127 → permission denial in reply
  - support 9501: order 4127 details
  - merchant 9002: store orders today

- Step 13: Part E inspect confirmed — merchant `get_order` tool span has cartwheel.* identity + `permission_denied=true`.

- Step 14: Part F complete — same request, two prompt hashes.
  - Baseline: `4e777f3bf61a` (session `dac2f3d1eeb64b32bb057490e7a097c1`)
  - Altered Tone wording: `db176ea8bcf9` (session `39503d7d43554514b2ab8b79ea676d3f`)
  - Prompt restored to baseline; server restarted.

- Step 15: Wrote `hw2-traces.json`
  - merchant 9002 denial on order 4127 (`eef392a4…`, prompt `4e777f3bf61a`)
  - shopper 1 Part F altered-prompt run (`73b50286…`, prompt `db176ea8bcf9`)

## Next

- Step 16: Student records the ≤5 min HW2 video (auth test, two traces, identity, tools, both prompt hashes).
