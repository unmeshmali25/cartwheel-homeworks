# Homework 3 progress

Interactive walkthrough of `homework/module-1/hw3.md`.
HW2 video deferred; HW2 endpoints + cartwheel.* spans already implemented (no reference patch).

## Deliverables checklist

- [x] `scenarios/pilot_scenarios.jsonl` (30; validated; awaiting sample review before run)
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

Revised after review (exact `user_style` values; split order vs product DQ; reasons column).

| Dimension | Values | Reason (SPEC / data) |
| --- | --- | --- |
| role | shopper, merchant, support | AUTH-1: permissions and visible rows differ by role |
| mutation | read, write | Write tools change state / hit refund threshold & approvals; reads do not (SPEC tools + ESC-1) |
| info_source | database_record, policy_docs, mixed, none | Authoritative answers come from SQL vs policy docs (`facts.yaml` / help center); none for out-of-scope |
| intent | order_status, refund, cancellation, policy_question, product_search, dispute, escalation, out_of_scope | Different intents exercise different tools and SCOPE / ESC rules |
| record_state | order_in_window, order_past_window, order_above_threshold, order_pre_ship, order_damaged_dq, product, product_damaged_dq, store_policy_page, none | Extra metadata depends on real order/product/policy rows; DQ split: orders 8001–8003 vs products 2–4 |
| applicable_policy | platform_rule, store_override, none | Store overrides can beat platform return window (`facts.yaml` store_overrides) |
| tools_needed | none, one_lookup, several_calls | Path length differs (refuse vs single lookup vs get_order+refund) |
| difficulty | well_specified, ambiguous, missing_information, boundary, auth_boundary | Challenge edges: vague asks, missing facts, $100/day-30 boundaries, cross-role access |
| user_style | `neutral_conversational`, `terse_fragmentary`, `typo_heavy`, `confused_rambling`, `frustrated_impatient`, `repetitive_pressuring`, `operational_shorthand`, `requests_short_plain_answer` | Validator exact-match set (`scenarios/validate.py`); RESP tone must hold across styles |
| scenario_group | coverage, challenge | Handout: report pools separately; challenge holds DQ + hard edges |
| turn_count | 1–25 (= 1 + followups) | Multi-turn corrections; not a free-form dial — set via followups list |

### DQ generation rule (explicit)

- Order DQ cases (`dq-order-*`): `record_state=order_damaged_dq`, set `tuple.order_id` to the case `entity_id`, `data_quality_case_id` = case id, `scenario_group=challenge`.
- Product DQ cases (`dq-product-*`): `record_state=product_damaged_dq`, set `tuple.product_id` to the case `entity_id`, same challenge/objective source rules.
- Final set: exactly **5** scenarios per each of the six cases (`validate.py --final`).

### Note on mutation / info_source vs intent

`mutation` and `info_source` are planning lenses so coverage is not all “read order status.” In JSONL they must stay consistent with `intent` + `tools_needed` (e.g. refund → write + mixed; policy_question → read + policy_docs; out_of_scope → read + none).

- Step 3: Generated `scenarios/pilot_scenarios.jsonl` (20 coverage + 10 challenge; all roles; 6 DQ cases once each).
  - Validator: `uv run python -m scenarios.validate scenarios/pilot_scenarios.jsonl` → 30 records OK.

## Next

- Step 4: Student reviews conversation sample (skill gate) — then go to reset DB + run pilot.
