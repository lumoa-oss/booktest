# Agent Step 3: Validation

Agent validates the answer for quality and completeness


## Inherited State from Steps 1-2

Question: How do I test a multi-step ML pipeline with booktest?
Answer: Treat each pipeline stage as a mini-test inside a TestCaseRun (e.g., def test_pipe(t: bt.TestCaseRun):) using t.h1/tln to document steps and emitting ...


## Validation

✓ Completed validation with 165 words


### Validation Result

What works well: The answer gives a sensible, practical strategy (unit/integration/E2E tiers, save intermediate artifacts, fix seeds, mock externals) and mentions relevant booktest concepts — TestCaseRun, review/diff UI, checkpoints/caching and metrics — so it points testers in the right direction.

Issues / missing information: It’s high-level and lacks concrete, actionable details — no example code showing how to emit artifacts or register checkpoints, no precise API calls for saving artifacts or enabling caching, and no guidance on automatically asserting on intermediates (rather than only inspecting/diffing them). A couple of named methods (e.g., t.h1/tln, t.tmetric(), t.start_review()) may be correct in spirit but you should confirm exact APIs in your booktest version; the answer could also cover how to run only later stages against cached outputs and how to manage large artifacts.

Overall assessment: Good — useful and accurate as a strategy, but could be improved by adding short code examples, exact API usage for artifacts/checkpoints, and concrete steps for automated verification and selective re-run of stages.


### Quality Assessment

 * Overall answer quality? Good
 * Completeness? Mostly Complete


## Agent Execution Complete



### Final Output

**Question:** How do I test a multi-step ML pipeline with booktest?

**Answer:** Treat each pipeline stage as a mini-test inside a TestCaseRun (e.g., def test_pipe(t: bt.TestCaseRun):) using t.h1/tln to document steps and emitting intermediate artifacts (save as CSV/NDJSON) so you can inspect or diff them. Persist and reuse heavy work with booktest checkpoints/caching so integration and E2E runs reuse saved step outputs instead of recomputing everything. Test strategy: fast unit tests for each component with small deterministic inputs and mocked external calls, integration tests that chain a few stages while capturing intermediate artifacts, then full end‑to‑end runs judged with booktest’s review/diff UI and numeric thresholds (t.start_review(), t.tmetric()). For reproducibility and fast iteration, fix random seeds, mock external services, save golden/intermediate artifacts for regression comparisons, and reuse cached checkpoints; when a case fails, annotate it in the review UI to guide fixes.

**Quality:** Good
**Completeness:** Mostly Complete


### Metrics

 * Quality Score: 75.000% (baseline)
 * Completeness Score: 75.000% (baseline)


### Minimum Requirements

 * Quality ≥ 50%.. ok
 * Completeness ≥ 50%.. ok


## Benefits of Build System + Snapshotting

✅ **First run:** ~20-30 seconds (3 GPT calls, context loading)
✅ **Subsequent runs:** ~100ms (all snapshotted, all cached)
✅ **Iterating on Step 3?** Only Step 3 re-runs
✅ **Iterating on Step 2?** Steps 2-3 re-run, Step 1 cached

**Pattern:** Break agent into test steps → iterate fast on individual steps

**Code structure:**
```python
agent = BooktestAgent(context)
state, message = agent.plan(state)     # Step 1
state, message = agent.answer(state)   # Step 2
state, message = agent.validate(state) # Step 3
```
