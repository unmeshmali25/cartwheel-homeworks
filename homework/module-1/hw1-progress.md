# HW1 progress note (working file, not a submission)

## Deliverables checklist
- [x] Part A: implement 5 tools in `agent/tools.py` — all contract tests pass
  - [x] `get_policy`
  - [x] `search_products`
  - [x] `list_my_orders`
  - [x] `cancel_order`
  - [x] `find_order`
- [ ] Part A: add at least one extra tool of my own + register in `TOOLS_BY_ROLE`
- [ ] Part B: >=10 conversations in `hw1-session.jsonl` (all 3 roles + required cases)
  - [x] Draft file: 9 shopper + 14 merchant + 5 support lines (28 total)
  - [x] Merchant ask for order 4127 (permission denial)
  - [x] Policy-override case (Juniper 14 vs platform 30)
  - [x] Support role conversations
  - [x] Support email-change: before (no escalate) + after prompt revision (escalate_to_human)
  - [x] Part C: SYSTEM_PROMPT_TEMPLATE Escalation updated for ESC-2 account changes
- [ ] Part C: prompt investigation (revise `agent/agent.py` only with evidence)
- [ ] Video (<=5 min, one continuous screen recording)
- [ ] Run focused + regression tests

## Setup
- [x] `uv sync` (uv 0.9.22; project uses Python 3.12 via uv)
- [x] `uv run python -m seed.generate` -> data/cartwheel.db (dev scale) + 18 policy docs
- [x] `.env` created from `.env.example`
- [ ] `.env`: add OPENAI_API_KEY locally (still empty; blocks live conversations)
- [x] baseline `uv run pytest` -> 147 passed, 4 skipped, 27 xfailed

## Resolved test-suite quirk (not my code)
- `uv run pytest` reports **1 failed** (`test_m2_run_judge_persists_store_predictions_for_prevalence`)
  with `httpx.ConnectError: Connection refused`.
- Cause: `tests/test_cli.py::test_trace_destinations_are_mutually_exclusive` calls `cli.main()`,
  which calls the real `load_env()` (`agent/cli.py:211`). `load_env` does
  `os.environ.setdefault(...)` for every non-empty `.env` value, so the template's
  `LANGFUSE_*` dev defaults leak into `os.environ` for the rest of the process.
- `analysis/helpers/langfuse_io.is_configured()` then returns True, so
  `scale.load_store_traces()` takes the live branch and calls `fetch_traces()`
  against `LANGFUSE_HOST=http://localhost:3000` (nothing listening).
- Confirmed: hiding `.env` makes the suite green (147 passed, 0 failed).
- Fix applied: `LANGFUSE_*` values blanked in `.env` (load_env skips empty values).
  Full suite now green: 147 passed, 4 skipped, 26 xfailed, 1 xpassed, 0 failed.
  Restore the three values from `.env.example` when starting HW2.

## Status log
- Step 1 orientation: DONE. Repo/spec/agent relationship clear.
- Step 2 environment: DONE except the model key.
- Part A: all 5 tools implemented and passing.
  `uv run pytest --runxfail tests/test_hw_holes.py -k hw1` -> 8 passed.
  Regression `tests/test_agent_tools.py tests/test_auth.py tests/test_eligibility.py` -> 24 passed.
  Full suite -> 147 passed, 4 skipped, 19 xfailed, 8 xpassed.
- Next: Part A extra tool (should come from a Part B gap) and Part B conversations,
  which need OPENAI_API_KEY in `.env`.
- Learning mode: SPEC-FIRST. User writes md specs; agent critiques decomposition only;
  code generated at handover. Agent handles terminal commands.
- Next: implement `search_products`.
