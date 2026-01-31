# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1000 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a review-driven regression testing framework for data-science and AI systems (LLMs, NLP, ML) that captures test outputs as human-readable markdown, snapshots them in Git (with DVC for large data) and makes behavioral changes reviewable instead of giving binary pass/fail. It adds tolerance-based metrics, AI-assisted evaluations, HTTP/LLM mocking, and a dependency-style build system to speed iteration and manage expensive operations.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
    * The answer explicitly calls Booktest a "review-driven regression testing framework".
    * It states that it "snapshots [test outputs] in Git (with DVC for large data)," directly mentioning snapshots.
    * It also says it "makes behavioral changes reviewable instead of giving binary pass/fail," reinforcing the review-driven aspect.
 * Does answer mention data science focus? Yes
    * The answer explicitly says it is for "data-science and AI systems (LLMs, NLP, ML)", directly stating a data science focus.
    * It mentions data-science workflow elements like DVC for large data, tolerance-based metrics, and managing expensive operations, which are relevant to data science projects.
 * Does answer mention Git-tracked results? Yes
    * The answer explicitly says outputs are 'snapshots them in Git (with DVC for large data)'.
    * It describes making behavioral changes reviewable via Git instead of a binary pass/fail, implying Git-tracked test artifacts.

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
    * Provides a clear one-sentence definition of Booktest's purpose (review-driven regression testing for AI/ML/NLP).
    * Lists key features (markdown outputs, Git/DVC snapshots, tolerance metrics, AI-assisted evals, mocking, dependency build) concisely, showing benefits without extraneous detail.
    * Uses direct, domain-specific terms that make functionality and workflow understandable.
 * How compelling is the value proposition for using booktest? Excellent
    * Addresses a real and growing need: LLM/ML outputs are nondeterministic and semantic, so replacing binary pass/fail with reviewable behavioral snapshots is highly valuable.
    * Integrates with existing dev workflows (Git + DVC) and stores human-readable Markdown snapshots, making regressions easy to inspect, review, and audit.
    * Adds practical features (tolerance-based metrics, AI-assisted evaluations, HTTP/LLM mocking, dependency-style builds) that reduce noise, handle subjective judgments, and cut iteration cost.
    * While effectiveness depends on execution (quality of AI evaluations, operational overhead), the core proposition strongly improves collaboration, traceability, and reliability for AI/DS testing.

 * **Criteria Score:** 3/3
 * **Rating Score:** 2/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest when outputs aren’t strictly right/wrong—LLM/ML/NLP systems, non‑deterministic pipelines, or expensive multi‑step workflows where you need reviewable markdown snapshots, tolerance‑based metrics, AI‑assisted review, and incremental caching. For traditional deterministic unit tests with clear pass/fail assertions, continue using pytest.


#### Evaluation:

 * Does answer mention expert review needs? Yes
    * The answer explicitly cites "reviewable markdown snapshots" and "AI‑assisted review", which indicate review needs.
    * It highlights use cases like non‑deterministic LLM/ML pipelines and tolerance‑based metrics that typically require human/expert review rather than strict pass/fail tests.
 * Does answer mention non-deterministic or probabilistic results? Yes
    * The answer explicitly mentions "non‑deterministic pipelines" and LLM/ML/NLP systems, indicating non-deterministic outputs.
    * It also refers to "tolerance‑based metrics" and outputs that "aren’t strictly right/wrong," which implies probabilistic/uncertain results.
 * Does answer mention data science workflows or caching? Yes
    * The answer explicitly references ML/LLM, NLP, non‑deterministic pipelines and expensive multi‑step workflows (i.e., data science workflows).
    * It explicitly mentions 'incremental caching'.

#### Quality ratings:

 * How clearly are the use cases differentiated? Excellent
    * The answer gives a clear, actionable contrast: use booktest for non‑deterministic/ML/LLM workflows and pytest for traditional deterministic unit tests.
    * It enumerates concrete distinguishing features (reviewable markdown snapshots, tolerance‑based metrics, AI‑assisted review, incremental caching) that directly map to when booktest is appropriate.
 * How helpful would this be for someone choosing a testing framework? Good
    * Clearly states the specific scenarios where booktest is preferable (LLM/ML/NLP, non‑deterministic pipelines, reviewable markdown, tolerance‑based metrics, AI‑assisted review, caching).
    * Provides a direct contrast with pytest for traditional deterministic unit tests, helping readers decide between them.
    * Not rated Excellent because it lacks concrete examples, benchmarks, and implementation/compatibility details that would fully guide adoption.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
```python
import booktest as bt

def fizzbuzz(n):
    return [
        "FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
        for i in range(1, n + 1)
    ]

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1..15")
    for line in fizzbuzz(15):
        t.tln(line)
```

Run booktest to snapshot the output (books/test/...), review diffs, and accept or reject changes as your implementation evolves.


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
    * The first line is exactly 'import booktest as bt'.
    * The code then uses bt.TestCaseRun, confirming the module is imported and referenced.
 * Does code define a test function starting with 'test_'? Yes
    * The code defines a function named 'test_fizzbuzz' which starts with the required 'test_' prefix.
    * The function signature accepts a bt.TestCaseRun parameter and contains test actions (t.h1, t.tln), so it is indeed a test function.
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
    * The test function signature declares t: bt.TestCaseRun (def test_fizzbuzz(t: bt.TestCaseRun)).
    * The parameter t is used inside the test (t.h1 and t.tln), so the TestCaseRun object is actually employed.
 * Does code use output methods like t.h1() or t.tln()? Yes
    * The test calls t.h1("FizzBuzz 1..15") to output a header.
    * The loop uses t.tln(line) to emit each fizzbuzz line.
 * Is the code syntactically valid Python? Yes
    * All constructs (import, def, list comprehension, nested conditional expressions) are valid Python syntax.
    * Type annotation on test_fizzbuzz and the bracket/indentation usage are correct; there are no unmatched delimiters or syntax errors.

#### Quality ratings:

 * How clear and understandable is the code example? Good
    * The example is correct and minimal: it implements FizzBuzz properly and shows how to produce a headed snapshot with t.h1 and line output with t.tln.
    * Readability is slightly reduced by the nested ternary inside a list comprehension; expanding to a clearer loop or helper would make it Excellent.
 * How well does the example demonstrate booktest features? Good
    * The example correctly uses booktest primitives (bt.TestCaseRun, t.h1, t.tln) to produce deterministic output that can be snapshotted.
    * It is minimal and readable, but it doesn't show the snapshot lifecycle (creating snapshots, reviewing diffs, accepting/rejecting changes) or other features such as multiple cases, failure reporting, or metadata.

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.5/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest snapshots and replays non-deterministic outputs (HTTP/LLM calls, functions, env vars, etc.) using decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), and @bt.snapshot_functions(), so subsequent runs are deterministic. For noisy numeric metrics it also provides tolerance-based metrics (t.tmetric) and caching to absorb small fluctuations and stabilize pipelines.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
    * The answer explicitly states "Booktest snapshots and replays non-deterministic outputs."
    * It lists snapshot-related decorators (@bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions()), indicating snapshot testing is used.
    * It describes replaying snapshots to make subsequent runs deterministic.
 * Does answer mention caching intermediate results? Yes
    * The answer explicitly states 'and caching to absorb small fluctuations and stabilize pipelines.'
    * Caching is mentioned as a mechanism alongside tolerance-based metrics to handle noisy numeric outputs and make runs deterministic.
 * Does answer mention mocking functions or environment variables? Yes
    * The answer explicitly names @bt.snapshot_functions(), which indicates handling/mocking of functions.
    * It also explicitly mentions “env vars” as one of the non-deterministic outputs that are snapshotted and replayed.

#### Quality ratings:

 * How well does the answer explain the technical approach? Good
    * Explains the core technical approach: snapshot-and-replay of non-deterministic outputs and lists concrete decorators (e.g., @bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions()).
    * Mentions handling of numeric noise via tolerance-based metrics and caching, but omits deeper implementation details (storage/replay mechanics, scope, or lifecycle), so it is not fully exhaustive.
 * How practical and actionable is the explanation? Excellent
    * Provides concrete, actionable mechanisms (snapshot + replay) and names of decorators (@bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions()) to implement determinism.
    * Also addresses numeric noise with tolerance-based metrics (t.tmetric) and caching, which makes the guidance practical for stabilizing real pipelines.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install it (pip install booktest) and optionally run booktest --setup to create config. Add Booktest tests under your test/ directory using the booktest API (bt.TestCaseRun, t.h1/t.tdf/t.tmetric, snapshot decorators), run them with the CLI (booktest or booktest test, use -pN for parallel), then review/accept snapshots (booktest -u) and add the booktest command to your CI pipeline.


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
    * The answer explicitly states "Install it (pip install booktest)".
    * It also references installation-related steps (running booktest --setup and adding the command to CI).
 * Does answer mention creating a test directory? Yes
    * The answer explicitly states: 'Add Booktest tests under your test/ directory', which mentions creating/using a test directory.
    * It also gives placement guidance for tests (under test/) as part of integration steps.
 * Does answer mention running 'booktest' command or CLI? Yes
    * The answer explicitly cites running the CLI commands such as 'booktest --setup', 'booktest' or 'booktest test', and 'booktest -u'.
    * It also advises adding the 'booktest' command to the CI pipeline, confirming mention of the CLI.

#### Quality ratings:

 * How complete is the integration guide? Good
    * Covers the essential workflow: installation, optional setup, placing tests, running them, accepting snapshots, and adding to CI.
    * Mentions key API elements (bt.TestCaseRun, t.h1/t.tdf/t.tmetric, snapshot decorators) and CLI usage (including parallel flag and -u to update snapshots).
    * Lacks concrete examples, file/config locations, version/Python compatibility, and troubleshooting tips which would help full integration.
    * Doesn't show sample test code or CI snippet—enough to get started but not fully prescriptive for complex projects.
 * How easy would it be to follow these instructions? Good
    * The answer gives a clear, ordered set of practical steps (install, optional setup, where to add tests, how to run, update snapshots, add to CI).
    * It omits concrete examples and detailed config/API usage (no sample test code, config contents, or CI snippet), so it may require additional reference material to implement fully.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


## Final Evaluation

Tracking metrics with ±5% tolerance

 * Criteria Score: 17/17 = 100.000% (was 97.059%, Δ+2.941%)
 * Rating Score: 8.5/10 = 85.000% (was 82.500%, Δ+2.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
