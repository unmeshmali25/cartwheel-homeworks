# Homework 3 progress

Interactive walkthrough of `homework/module-1/hw3.md`.
HW2 video deferred; HW2 endpoints + cartwheel.* spans already implemented (no reference patch).

## Deliverables checklist

- [ ] `scenarios/pilot_scenarios.jsonl`
- [ ] `scenarios/pilot-results.jsonl`
- [ ] `scenarios/pilot_review.jsonl` (≥10 reviewed, ≥5 confirmed failures)
- [ ] `scenarios/support_scenarios.jsonl` (175 coverage + 75 challenge)
- [ ] `scenarios/support_review.jsonl` (15 reviewed)
- [ ] `scenarios/monitoring_scenarios.jsonl` (50 selected)
- [ ] `scenarios/final-results.jsonl` (250 completed)
- [ ] `reports/smoke-output.txt`
- [ ] `traces/support_traces.json`
- [ ] Video (student records)

## Concepts (Step 1)

- **Scenario** — planned request + extra metadata from DB/policies (not from the model).
- **Trace** — recorded run (conversation, model calls, tools) in Langfuse.
- **Dimension** — one axis of variation; a **tuple** is one combination → one scenario.
- **Coverage vs challenge** — broad ordinary/hard set vs intentionally difficult set.
- **Pilot** — 30 runs first to fix scenarios and confirm failures before the full 250.

## Done

- Step 1: Orientation + progress note.

## Next

- Step 2: Part A — read skill + SPEC, query `data_quality_cases`, propose dimensions for student review (stop before generation).
