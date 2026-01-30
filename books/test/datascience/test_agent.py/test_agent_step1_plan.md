# Agent Step 1: Planning

Agent analyzes the question and creates an answering strategy


## Loading Context

Loaded 34000 characters of documentation


## Creating Plan

✓ Created plan with 148 words


### Question

How do I test a multi-step ML pipeline with booktest?


### Plan

- Highlight the most relevant booktest features up front: the TestCaseRun API for authoring tests, named sections/steps (h1/h2), snapshotting/artifact capture for intermediate outputs, reviewer annotations/approval flow, and built-in diff/comparison helpers. Mention reproducibility aids (seeding, small fixtures) and caching/mocking for expensive steps.

- Explain the key concepts to teach: isolate and test each pipeline stage (capture inputs/outputs), normalize outputs for stable diffs, combine automated invariant checks with human review for subjective output, and store intermediate artifacts so reviewers can judge regressions. Emphasize designing small deterministic fixtures and using snapshots for regression detection.

- Present information in this order: 1) high-level workflow and strategy (what to capture and why), 2) a minimal concrete example test that walks through a 3-step pipeline (preprocess → model → postprocess) showing TestCaseRun usage and snapshotting of intermediates, 3) running and reviewing tests, and 4) practical tips (handling slow steps, seeding, updating snapshots, CI integration).


### Plan Review

 * Does plan address the question? Yes
    * The plan explicitly covers booktest features needed for multi-step pipelines (TestCaseRun, named steps, snapshotting, artifact capture, reviewer flow and diffs).
    * It lays out testing strategy and key concepts (stage isolation, deterministic fixtures, normalized outputs, combining automated checks with human review) and promises a concrete 3-step example plus practical tips (seeding, caching, CI), which directly answers how to test such pipelines.
 * Does plan reference relevant features? Yes
    * The plan explicitly calls out and plans to demonstrate key booktest features: the TestCaseRun API, named sections/steps, snapshotting/artifact capture, reviewer annotations/approval flow, and built-in diff/comparison helpers.
    * It also covers practical, relevant practices for ML pipelines—capturing intermediate outputs, normalizing outputs for stable diffs, deterministic fixtures/seeding, caching/mocking, and CI/update workflows—and includes a concrete example to show those features in action.
