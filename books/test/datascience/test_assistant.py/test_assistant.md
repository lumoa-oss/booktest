# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1103 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework for data science that treats test outputs as Git-tracked, reviewable snapshots and combines AI-assisted evaluation, tolerance-based metrics, and a dependency/build system so you can manage non-deterministic and expensive ML/LLM workflows. It also provides HTTP/LLM mocking, DVC integration for large snapshots, and parallel execution to speed iteration and triage regressions.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
    * The answer explicitly says it 'treats test outputs as Git-tracked, reviewable snapshots'.
    * That wording directly indicates snapshot-based and review-driven testing.
 * Does answer mention data science focus? Yes
    * The answer explicitly calls Booktest a "Python testing framework for data science."
    * It references ML/LLM workflows and DVC integration, which are data-science-specific features.
 * Does answer mention Git-tracked results? Yes
    * The answer explicitly states that Booktest "treats test outputs as Git-tracked, reviewable snapshots."
    * This description directly indicates that results are tracked with Git and intended to be reviewable.

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
    * Provides a concise, high-level definition of purpose and scope (Python testing framework for data science).
    * Lists key features clearly and specifically (Git-tracked snapshots, AI-assisted evaluation, tolerance metrics, mocking, DVC integration, parallel execution) without unnecessary detail.
 * How compelling is the value proposition for using booktest? Excellent
    * Directly tackles core ML/LLM testing pain points: Git-tracked, reviewable snapshots plus AI-assisted evaluation and tolerance-based metrics make non-deterministic outputs testable and auditable.
    * Practical operational features (dependency/build system for expensive workflows, HTTP/LLM mocking, DVC integration, parallel execution) meaningfully reduce iteration and triage cost — potential caveat is typical maturity/learning-curve risk, but the value proposition is strong.

 * **Criteria Score:** 3/3
 * **Rating Score:** 2/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest when you're testing data‑science or LLM workflows with non‑deterministic or subjective outputs that need human/AI review, tolerance‑based metrics, snapshot diffs, incremental/cached pipeline steps, and HTTP/LLM mocking. For traditional deterministic unit tests with strict equality assertions, stick with pytest.


#### Evaluation:

 * Does answer mention expert review needs? Yes
    * The answer explicitly states outputs "that need human/AI review", directly mentioning expert review.
    * It highlights subjective or non‑deterministic outputs which require human/AI judgment rather than pure automated assertions.
 * Does answer mention non-deterministic or probabilistic results? Yes
    * The answer explicitly mentions "non‑deterministic or subjective outputs."
    * It recommends booktest for cases with tolerance‑based metrics and human/AI review, which are typical for probabilistic behavior.
 * Does answer mention data science workflows or caching? Yes
    * The answer explicitly refers to "data‑science or LLM workflows."
    * It also mentions "incremental/cached pipeline steps," which indicates caching.

#### Quality ratings:

 * How clearly are the use cases differentiated? Excellent
    * Provides a clear, actionable rule: use booktest for non‑deterministic/subjective ML/LLM workflows and pytest for deterministic unit tests.
    * Lists specific features and scenarios (human/AI review, tolerance metrics, snapshot diffs, incremental/cached steps, HTTP/LLM mocking) that justify choosing booktest, making the distinction concrete.
 * How helpful would this be for someone choosing a testing framework? Good
    * Directly contrasts the strengths of booktest (non‑deterministic, human/AI review, snapshot diffs, caching, HTTP/LLM mocking) with pytest (deterministic unit tests), which is exactly the core decision factor.
    * Lacks supporting details (ecosystem/maturity, examples, integration cost, when not to use booktest beyond strict equality), so it's helpful but not comprehensive enough to be rated Excellent.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
Create test/test_fizzbuzz.py with a Booktest test that prints FizzBuzz for 1–15 and snapshots the output:

```python
import booktest as bt

def fizzbuzz(n):
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0: return "Fizz"
    if n % 5 == 0: return "Buzz"
    return str(n)

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1..15")
    for i in range(1, 16):
        t.tln(f"{i}: {fizzbuzz(i)}")
```


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
    * The snippet begins with 'import booktest as bt'.
    * This matches the allowed forms (specifically the 'import booktest as bt' variant).
 * Does code define a test function starting with 'test_'? Yes
    * The code includes a top-level function named def test_fizzbuzz(...).
    * The function name begins with 'test_', matching the required test-function naming convention.
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
    * The test function is defined as test_fizzbuzz(t: bt.TestCaseRun), i.e. it declares a parameter of type bt.TestCaseRun.
    * The code calls methods on t (t.h1 and t.tln), showing it uses the TestCaseRun instance.
 * Does code use output methods like t.h1() or t.tln()? Yes
    * The test function calls t.h1("FizzBuzz 1..15").
    * The loop uses t.tln(...) to print each fizzbuzz line.
 * Is the code syntactically valid Python? Yes
    * All constructs used (import, def, if/return, for loop, f-strings, type annotation) are valid Python syntax.
    * Annotations and references to booktest are syntactically allowed; any missing module or attributes would be a runtime issue, not a syntax error.

#### Quality ratings:

 * How clear and understandable is the code example? Good
    * The example is simple and shows both the fizzbuzz implementation and a Booktest test that emits structured output (t.h1 and t.tln) for 1..15.
    * It uses clear, idiomatic Python and a minimal amount of code, so readers can quickly understand and reuse it.
    * Minor omissions reduce perfect clarity: it doesn't show how to run the test or explicitly snapshot/assert the output (e.g. t.snapshot() or expected output), so a reader unfamiliar with Booktest may be unsure how the output is validated.
 * How well does the example demonstrate booktest features? Good
    * Demonstrates a minimal, runnable test file that uses booktest's TestCaseRun API (t.h1 and t.tln) to produce readable output.
    * Illustrates the fizzbuzz logic and shows how to emit output that can be snapshotted, but it doesn't show the snapshot/assert call or the expected snapshot content.
    * Omits other common booktest features (snapshot storage, verification, setup/teardown, richer formatting or examples), so it's useful as a basic example but not comprehensive.

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.5/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest makes non‑deterministic behavior deterministic by snapshotting external effects: use decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), or @bt.snapshot_functions(time.time, random.random) to record HTTP/LLM responses and noisy functions on first run and replay them thereafter. It also snapshottes AI reviews (so evaluations are reused), so subsequent runs are fast and repeatable unless the outputs actually change.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
    * Answer explicitly states it makes behavior deterministic by "snapshotting external effects".
    * Lists decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions(...) and describes recording and replaying responses (including AI reviews).
 * Does answer mention caching intermediate results? Yes
    * It explicitly describes “snapshotting” external effects to record on first run and replay thereafter — this is caching intermediate results.
    * It notes AI reviews are snapshotted and reused, and shows decorators (e.g. @bt.snapshot_functions) that capture noisy function outputs for reuse.
 * Does answer mention mocking functions or environment variables? Partially
    * The answer explicitly mentions snapshotting/noisy functions using @bt.snapshot_functions(time.time, random.random), which corresponds to handling/mocking functions.
    * The answer does not mention environment variables at all.

#### Quality ratings:

 * How well does the answer explain the technical approach? Good
    * Explains the core mechanism clearly — snapshotting external effects to record on first run and replay thereafter — and gives concrete decorator examples (@bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions(...)).
    * Notes important use cases (HTTP/LLM responses, noisy functions, AI reviews) and the practical outcome (fast, repeatable subsequent runs).
    * Does not cover lower‑level implementation details (storage format, matching/validation, handling changed outputs or environment drift), so it is informative but not exhaustive.
 * How practical and actionable is the explanation? Excellent
    * Provides concrete, actionable mechanisms (specific decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), @bt.snapshot_functions(...)) that a user can apply immediately.
    * Clearly explains what is snapshotted (HTTP/LLM responses and noisy functions) and the runtime behavior (record on first run, replay thereafter) making repeatability and performance implications obvious.
    * Notes the practical limitation (outputs will update if they actually change), so users understand when snapshots are reused versus refreshed.

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 1.75/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install it (pip install booktest) and run booktest --setup, then add tests under test/ that use the Booktest API (functions taking t: bt.TestCaseRun and optional decorators like @bt.snapshot_httpx() or @bt.depends_on()). Run tests with booktest (e.g. booktest test or booktest test -p8), review/accept snapshots (booktest test -u) and commit the generated books/ snapshots (large HTTP/LLM cassettes go to DVC) as part of your repo/CI.


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
    * The answer explicitly states the installation command 'pip install booktest'.
    * It also gives installation-related steps ('Install it' and 'run booktest --setup'), confirming installation guidance is provided.
 * Does answer mention creating a test directory? Yes
    * The answer explicitly says to "add tests under test/", which implies creating/using a test directory.
    * It also instructs running "booktest --setup", which implies initializing test-related scaffolding in the project.
 * Does answer mention running 'booktest' command or CLI? Yes
    * The answer explicitly instructs to 'run booktest --setup'.
    * It gives CLI examples such as 'booktest test', 'booktest test -p8', and 'booktest test -u'.

#### Quality ratings:

 * How complete is the integration guide? Good
    * Provides the essential, concrete steps: installation, initial setup, where to place tests, how to run tests, snapshot review/acceptance, and committing snapshots (including DVC for large cassettes).
    * Missing finer details and examples needed for an "Excellent" integration guide — e.g., sample test code snippets, interaction with existing test frameworks (pytest/unittest) and CI configuration examples, handling virtualenvs or version constraints, and edge-case guidance.
 * How easy would it be to follow these instructions? Good
    * Instructions give a clear, correct high‑level workflow: install, run setup, add tests, run tests, accept snapshots, and commit artifacts.
    * Missing concrete examples and details (no sample test code, no explanation of what booktest --setup does, no import/usage snippets), which may slow first‑time users.
    * Ambiguous guidance about DVC/CI integration and snapshot storage (how to configure DVC remotes, CI commands, or handling large cassettes) so some additional configuration knowledge is needed.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


## Final Evaluation

Tracking metrics with ±5% tolerance

 * Criteria Score: 16.5/17 = 97.059% (was 97.059%, Δ-0.000%)
 * Rating Score: 8.5/10 = 85.000% (was 92.500%, Δ-7.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
