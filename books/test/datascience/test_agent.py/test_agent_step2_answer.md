# Agent Step 2: Generating Answer

Agent uses the plan to generate a detailed answer


## Inherited State from Step 1

Question: How do I test a multi-step ML pipeline with booktest?
Plan: - Highlight the most relevant booktest features up front: the TestCaseRun API for authoring tests, named sections/steps (h1/h2), snapshotting/artifact...


## Generating Answer

✓ Generated answer with 154 words


### Generated Answer

Use the TestCaseRun API to author multi-step tests: name each stage with t.h1 / t.h2, emit intermediate inputs/outputs with t.iln/t.tln so booktest will snapshot and diff them, and leverage the built‑in artifact/snapshot capture, reviewer annotations (t.start_review) and comparison helpers to surface regressions.  
Workflow: isolate every pipeline stage (preprocess → model → postprocess), normalize outputs for stable diffs (sort keys, round floats, redact timestamps), combine automated invariants (t.tmetric or lightweight assertions with tolerances) with human review for subjective results, and store intermediate artifacts so reviewers can judge changes.  
Concrete pattern: in a single test function call t.h1("Preprocess"); t.tln(preproc_out); t.h2("Model"); t.tln(model_out); t.h2("Postprocess"); t.tln(final_out) — booktest will snapshot those sections and show diffs; add t.tmetric checks for numeric stability and t.start_review() prompts for human approval.  
Run with booktest test and review generated diffs; for CI keep slow steps mocked or cached, seed RNGs and use small deterministic fixtures, and only update snapshots when reviewers approve intentional changes.


### Answer Review

 * Does answer follow the plan? Yes
 * Is answer accurate per documentation? No
 * Is answer clear and concise? Yes
