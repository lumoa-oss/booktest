# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1000 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a review-driven testing framework for data science that makes non-deterministic outputs reviewable by snapshotting test results as markdown, using AI-assisted reviews, and tracking metrics with tolerances. It also functions as a build system for tests—caching expensive steps, mocking HTTP/LLM calls, and running dependency-aware, parallel test pipelines so you can review and accept regressions like code.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
 * Does answer mention data science focus? Yes
 * Does answer mention Git-tracked results? No

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
 * How compelling is the value proposition for using booktest? Excellent

 * **Criteria Score:** 2/3
 * **Rating Score:** 2/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest for data‑science/ML/LLM integration tests where outputs are non‑deterministic or require expert (human or AI) review, tolerance‑based metrics, snapshot diffs, and pipeline caching/parallelism for expensive steps. Use pytest for traditional unit tests with precise, deterministic assertions.


#### Evaluation:

 * Does answer mention expert review needs? Yes
 * Does answer mention non-deterministic or probabilistic results? Yes
 * Does answer mention data science workflows or caching? Yes

#### Quality ratings:

 * How clearly are the use cases differentiated? Excellent
 * How helpful would this be for someone choosing a testing framework? Excellent

 * **Criteria Score:** 3/3
 * **Rating Score:** 2/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
Here's a minimal booktest fizzbuzz example you can drop into test/test_fizzbuzz.py:

```python
import booktest as bt

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz")
    for i in range(1, 16):
        if i % 15 == 0:
            out = "FizzBuzz"
        elif i % 3 == 0:
            out = "Fizz"
        elif i % 5 == 0:
            out = "Buzz"
        else:
            out = str(i)
        t.tln(f"{i}: {out}")
```


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
 * Does code define a test function starting with 'test_'? Yes
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
 * Does code use output methods like t.h1() or t.tln()? Yes
 * Is the code syntactically valid Python? Yes

#### Quality ratings:

 * How clear and understandable is the code example? Excellent
 * How well does the example demonstrate booktest features? Good

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.75/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest makes nondeterministic outputs reproducible by snapshotting and replaying external/unstable sources (LLM/HTTP calls, random/time functions) so subsequent runs reuse recorded results. You make tests deterministic with decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), or @bt.snapshot_functions(time.time, random.random).


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
 * Does answer mention caching intermediate results? Yes
 * Does answer mention mocking functions or environment variables? Partially

#### Quality ratings:

 * How well does the answer explain the technical approach? Excellent
 * How practical and actionable is the explanation? Excellent

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 2/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install and initialize booktest (pip install booktest and optionally booktest --setup), then add tests under your test/ directory using the booktest API (test functions take a bt.TestCaseRun). Use decorators like @bt.snapshot_httpx() and @bt.depends_on() to mock external calls and share/cache expensive results, run with booktest test, and commit the generated books/ snapshots to Git for reviewable diffs.


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
 * Does answer mention creating a test directory? Yes
 * Does answer mention running 'booktest' command or CLI? Yes

#### Quality ratings:

 * How complete is the integration guide? Good
 * How easy would it be to follow these instructions? Good

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


## Final Evaluation

Tracking metrics with ±5% tolerance, no drops allowed

 * Criteria Score: 15.5/17 = 91.176% (was 94.118%, Δ-2.942%)
 * Rating Score: 9.25/10 = 92.500% (was 92.500%, Δ+0.000%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
