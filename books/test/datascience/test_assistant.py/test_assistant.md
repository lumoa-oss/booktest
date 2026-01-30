# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1103 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework for data science that turns test outputs into Git‑tracked, reviewable markdown snapshots and adds AI‑assisted review and tolerance‑based metrics to handle non‑deterministic ML/LLM outputs. It also provides pipeline-style dependency caching, HTTP/LLM request snapshotting, DVC integration and parallel execution to speed iteration and manage regressions.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
    * The answer explicitly says it turns test outputs into "reviewable markdown snapshots" (snapshot testing).
    * It also mentions "AI‑assisted review," indicating a review-driven testing approach.
 * Does answer mention data science focus? Yes
    * The answer explicitly calls Booktest a "Python testing framework for data science."
    * It references handling non-deterministic ML/LLM outputs and DVC integration, which are data‑science/ML concerns.
 * Does answer mention Git-tracked results? Yes
    * The answer explicitly states it "turns test outputs into Git‑tracked, reviewable markdown snapshots."
    * That phrase directly indicates test results are tracked in Git, so Git-tracked results are clearly mentioned.

#### Quality ratings:

 * How clear and concise is the explanation? Good
    * The explanation succinctly states the core purpose (a Python testing framework for data science) and lists key features (markdown snapshots, AI‑assisted review, tolerance metrics, caching, HTTP/LLM snapshotting, DVC integration, parallel execution).
    * It is concise but uses some domain-specific jargon (e.g., “pipeline-style dependency caching”, “AI‑assisted review”) that could be clearer for readers unfamiliar with those terms.
 * How compelling is the value proposition for using booktest? Good
    * Addresses real and common pain points in ML/LLM testing: snapshotting, non-deterministic outputs, and reviewability via Git-markdown snapshots.
    * Unique features (AI-assisted review and tolerance-based metrics) directly tackle flaky/approximate outputs that standard test frameworks miss.
    * Practical integrations (DVC, HTTP/LLM request snapshotting, caching and parallel execution) make it useful in real data-science pipelines and likely to speed iteration and regression tracking.
    * Not rated Excellent because of typical caveats: potential operational/storage overhead of snapshots, reliance on AI review quality, and unknowns about maturity/compatibility and maintenance burden.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest for data‑science/integration tests where outputs are non‑deterministic or subjective (LLM outputs, model evaluations, pipelines) and you need snapshotting, AI/human review, tolerance metrics, and cached dependency-style runs to speed expensive work. For traditional deterministic unit tests with strict equality checks, stick with pytest.


#### Evaluation:

 * Does answer mention expert review needs? Yes
    * The answer explicitly mentions "AI/human review", which indicates a need for human (expert) review.
    * It recommends booktest for subjective, non‑deterministic outputs (LLM outputs, model evaluations) that typically require human oversight.
 * Does answer mention non-deterministic or probabilistic results? Yes
    * The answer explicitly states "where outputs are non‑deterministic or subjective (LLM outputs, model evaluations, pipelines)".
    * It describes handling probabilistic outputs with snapshotting, tolerance metrics, and AI/human review, which addresses non-deterministic results.
 * Does answer mention data science workflows or caching? Yes
    * The answer explicitly mentions "data‑science/integration tests" and examples like LLM outputs, model evaluations, and pipelines.
    * The answer explicitly refers to "cached dependency-style runs to speed expensive work," which describes caching.

#### Quality ratings:

 * How clearly are the use cases differentiated? Excellent
    * The answer gives a clear, direct contrast: booktest for non‑deterministic/subjective data‑science and integration scenarios, pytest for deterministic unit tests.
    * It lists concrete examples and distinguishing features (LLM outputs, snapshotting, AI/human review, tolerance metrics, cached dependency runs), making the decision actionable.
 * How helpful would this be for someone choosing a testing framework? Good
    * Directly addresses the core decision: use booktest for non‑deterministic/subjective ML or pipeline tests and pytest for deterministic unit tests.
    * Highlights useful differentiators (snapshotting, human/AI review, tolerance metrics, cached dependency runs) that are important for data‑science workflows.
    * Lacks concrete examples, tradeoffs, maturity/ecosystem info, and guidance on integration/migration, so not fully comprehensive for someone making a final choice.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
Here's a minimal booktest for FizzBuzz (1–15): 

```python
import booktest as bt

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1-15")
    for i in range(1, 16):
        out = "FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
        t.tln(out)
```


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
    * The code contains the line "import booktest as bt" at the top.
    * This exactly matches one of the required import patterns ('import booktest as bt').
 * Does code define a test function starting with 'test_'? Yes
    * The code defines a function named 'test_fizzbuzz' which begins with 'test_'.
    * The function appears to be intended as a test (accepts a TestCaseRun parameter and uses test methods), so it matches the required naming convention.
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
    * The test function signature is def test_fizzbuzz(t: bt.TestCaseRun), which uses the TestCaseRun parameter with type annotation.
    * The parameter t is actually used in the body (t.h1 and t.tln), confirming active use of TestCaseRun.
 * Does code use output methods like t.h1() or t.tln()? Yes
    * The code calls t.h1("FizzBuzz 1-15") to produce a heading.
    * It uses t.tln(out) inside the loop to emit each output line.
 * Is the code syntactically valid Python? Yes
    * The import, function definition, annotated parameter, for-loop, and nested conditional expression are all valid Python syntax.
    * Although 'booktest' or 'bt.TestCaseRun' may be undefined at runtime, that does not make the code syntactically invalid.

#### Quality ratings:

 * How clear and understandable is the code example? Good
    * The example is minimal and shows the core FizzBuzz logic and usage of booktest functions (t.h1, t.tln) clearly.
    * The single-line nested conditional is compact but slightly reduces readability compared to an if/elif/else block.
    * It lacks comments or explanation of booktest semantics and does not show explicit assertions/expected output, which could confuse readers unfamiliar with the library.
 * How well does the example demonstrate booktest features? Good
    * The example correctly uses booktest basics (a test function accepting bt.TestCaseRun, t.h1 and t.tln) and produces the right FizzBuzz output for 1–15.
    * It is minimal and clear, which is useful as a quick starting example.
    * It does not show important booktest features such as expressing expected outputs/assertions, test metadata, or how to run/verify the test, so it is not comprehensive enough for an 'Excellent' rating.

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.5/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest makes non-determinism deterministic by snapshotting and mocking external sources and functions: use decorators like @bt.snapshot_httpx() (or @bt.snapshot_functions(time.time, random.random)) to record real HTTP/LLM responses or random/timestamp functions on the first run and replay them thereafter. AI reviews are likewise snapshotted, and tests can return/cached objects (with @depends_on) so expensive/noisy steps aren’t re-run.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
    * The answer explicitly uses the term 'snapshotting' and says Booktest makes non-determinism deterministic by snapshotting and mocking external sources and functions.
    * It provides concrete snapshot-related decorators (@bt.snapshot_httpx(), @bt.snapshot_functions(...)) and notes AI reviews are 'snapshotted' and replayed on subsequent runs.
 * Does answer mention caching intermediate results? Yes
    * The answer explicitly says tests can return/cached objects (with @depends_on) so expensive/noisy steps aren’t re-run.
    * It also describes snapshotting and replaying responses (record on first run, replay thereafter), which is a form of caching intermediate results.
 * Does answer mention mocking functions or environment variables? Partially
    * Answer explicitly mentions mocking functions (e.g., @bt.snapshot_functions(time.time, random.random) and snapshotting external sources).
    * Answer does not mention environment variables at all.

#### Quality ratings:

 * How well does the answer explain the technical approach? Excellent
    * Explains the snapshot-and-replay approach that makes non-determinism deterministic.
    * Provides concrete decorators (@bt.snapshot_httpx, @bt.snapshot_functions) and examples (time.random, LLM/HTTP) and mentions caching with @depends_on.
 * How practical and actionable is the explanation? Excellent
    * Provides concrete, actionable mechanisms (specific decorators like @bt.snapshot_httpx() and @bt.snapshot_functions(...)) so a developer can implement it directly.
    * Clearly explains behavior (record on first run, replay thereafter) and covers both external I/O and non-deterministic functions (time, random) plus AI reviews.
    * Mentions caching/depends_on for expensive or noisy steps, making the approach practical for real test suites (only minor details like snapshot storage/update are omitted).

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 2/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
pip install booktest and run booktest --setup to add an optional config. Add tests in a test/ folder using the Booktest API (def test_x(t: bt.TestCaseRun): …), optionally use decorators like @bt.snapshot_httpx() or @bt.depends_on(), and run them with booktest test (use -p, -v, -i, -u, etc. for parallel, verbose, interactive review, and snapshot updates).


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
    * The answer explicitly states the installation command 'pip install booktest'.
    * It also mentions running 'booktest --setup' to configure the project, which is an installation/setup step.
 * Does answer mention creating a test directory? Yes
    * The answer explicitly instructs to "Add tests in a test/ folder".
    * It shows the test function format (def test_x(...)) and how to run them, implying use of that directory for tests.
 * Does answer mention running 'booktest' command or CLI? Yes
    * The answer explicitly says to "run booktest --setup" to add a config.
    * It also instructs to "run them with booktest test" and lists CLI flags (-p, -v, -i, -u).

#### Quality ratings:

 * How complete is the integration guide? Good
    * Gives the essential quick-start steps: installation, optional setup, where to place tests, example test signature, useful decorators, and the command with common flags.
    * Missing concrete examples (full test code), details of the --setup/config contents, how snapshots are stored/updated, CI/virtualenv guidance, and troubleshooting or deeper API coverage — so it's not comprehensive enough to be 'Excellent'.
 * How easy would it be to follow these instructions? Good
    * The answer gives clear, actionable steps (install, run setup, add tests, run test runner) and shows key commands and options.
    * It mentions important details like where tests go, the test-signature, useful decorators, and common run flags.
    * It lacks a concrete code example, details about what --setup changes, and environment/import specifics, so a user might need to look up a few small details.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


## Final Evaluation

Tracking metrics with ±5% tolerance

 * Criteria Score: 16.5/17 = 97.059% (was 97.059%, Δ-0.000%)
 * Rating Score: 8.25/10 = 82.500% (was 85.000%, Δ-2.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
