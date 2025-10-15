# Agent Step 1: Planning

Agent analyzes the question and creates an answering strategy


## Loading Context

Loaded 27513 characters of documentation


## Creating Plan

✓ Created plan with 136 words


### Question

How do I test a multi-step ML pipeline with booktest?


### Plan

- Highlight booktest features to use: TestCaseRun for structured tests (h1/tln for step headings), artifact logging (save intermediate outputs as CSV/NDJSON), checkpoints/caching to persist and re-use step outputs, and built‑in diff/review mechanisms for human grading. Key concept: treat each pipeline stage as a mini-test that emits artifacts you can inspect or compare.
- Explain the test order/strategy: start with fast unit tests for each component (small deterministic inputs, mocked external services), then integration tests that chain a few steps together capturing intermediate artifacts, and finally end‑to‑end runs for full pipelines evaluated via booktest’s review/diff UI or numeric thresholds.
- Practical tips to include: fix random seeds and mock external calls for reproducibility, save golden/intermediate artifacts for regression comparisons, reuse cached artifacts to speed runs, and annotate failing cases in the review UI to iterate on fixes.


### Plan Review

 * Does plan address the question? Yes
 * Does plan reference relevant features? Yes

