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
- Step 2a: Read skill + SPEC; queried six `data_quality_cases` (orders 8001–8003, products 2–4).

## Data quality cases (for challenge set later)

| case_id | entity | expected handling |
| --- | --- | --- |
| dq-order-missing-delivery-date | order 8002 | Do not compute return deadline from missing date |
| dq-order-reversed-dates | order 8001 | Escalate inconsistent chronology |
| dq-order-store-mismatch | order 8003 | Preserve auth; escalate inconsistent store/product |
| dq-product-duplicate-title | product 2 | Clarify / use stable ids before unique match |
| dq-product-invalid-price | product 4 | Do not present negative price as valid |
| dq-product-missing-title | product 3 | Do not invent a product name |

## Dimension brainstorm (student)

- Read vs write request (side-effecting tools vs lookups).
- DB data vs policy-doc data (order/product facts vs help-center/policy).

## Approved dimension plan (Part A) — student approved 2026-11-14

| Dimension | Values |
| --- | --- |
| role | shopper, merchant, support |
| mutation (read vs write) | read, write |
| info_source | database_record, policy_docs, mixed, none |
| intent | order_status, refund, cancellation, policy_question, product_search, dispute, escalation, out_of_scope |
| record_state | order_in_window, order_past_window, order_above_threshold, order_pre_ship, order_damaged_dq, product, store_policy_page, none |
| applicable_policy | platform_rule, store_override, none |
| tools_needed | none, one_lookup, several_calls |
| difficulty | well_specified, ambiguous, missing_information, boundary, auth_boundary |
| user_style | 8 validator styles |
| scenario_group | coverage \| challenge |
| turn_count | 1 + followups (not a free dial) |

## Next

- Step 3: Part B — generate `scenarios/pilot_scenarios.jsonl` (30 scenarios) using the skill; validate; then run (separate go).
