# Agent Step 2: Generating Answer

Agent uses the plan to generate a detailed answer


## Inherited State from Step 1

Question: How do I test a multi-step ML pipeline with booktest?
Plan: - Relevant features: TestCaseRun (per-test context), saving intermediate artifacts/checkpoints or "snapshots" for human review, diffing/visualization ...


## Generating Answer

✓ Generated answer with 127 words


### Generated Answer

Break the pipeline into independent stages and write one Booktest TestCaseRun that runs each stage on deterministic or sampled inputs, saving intermediate artifacts/checkpoints (e.g., write snapshot files and log their paths) so you can inspect exactly what changed. For each stage use t.h1/t.iln (or t.tln) to record human-readable outputs, compute quick sanity metrics and report them with t.tmetric(..., tolerance=...) to automatically catch obvious regressions, and persist checkpoints for visual diffing. For things that need human judgment start a review (r = t.start_review()), attach the intermediate outputs with r.iln() and use r.reviewln() questions so reviewers see git-style diffs and can approve or comment. Keep tests fast by sampling inputs, assert only on stable metrics, and iterate by inspecting the saved snapshots/diffs to pinpoint which stage introduced a regression.


### Answer Review

 * Does answer follow the plan? Yes
 * Is answer accurate per documentation? Yes
 * Is answer clear and concise? Yes
