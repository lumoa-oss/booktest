# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1090 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework for data science and LLM workflows that treats test outputs as human-readable, Git-tracked markdown snapshots instead of binary asserts. It combines build-style caching/dependencies, tolerance-based metrics, HTTP/LLM snapshotting, and AI-assisted review/diffing to make non-deterministic outputs reviewable and regressions manageable.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
 * Does answer mention data science focus? Yes
 * Does answer mention Git-tracked results? Yes

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
 * How compelling is the value proposition for using booktest? Excellent

 * **Criteria Score:** 3/3
 * **Rating Score:** 2/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest for data‑science or LLM workflows where outputs are non‑deterministic or subjective and need human/AI review, tolerance‑based metrics, snapshot diffs, HTTP/LLM mocking, and incremental/cached pipelines. For traditional deterministic unit tests with strict pass/fail assertions, stick with pytest.


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
Create test/test_fizzbuzz.py to snapshot FizzBuzz output (so future changes are reviewable). Example:

```python
import booktest as bt

def fizzbuzz(n):
    if n % 15 == 0:
        return "fizzbuzz"
    if n % 3 == 0:
        return "fizz"
    if n % 5 == 0:
        return "buzz"
    return str(n)

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1–15")
    for i in range(1, 16):
        t.tln(f"{i}: {fizzbuzz(i)}")
```


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
 * Does code define a test function starting with 'test_'? Yes
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
 * Does code use output methods like t.h1() or t.tln()? Yes
 * Is the code syntactically valid Python? Yes

#### Quality ratings:

 * How clear and understandable is the code example? Excellent
 * How well does the example demonstrate booktest features? Excellent

 * **Criteria Score:** 5/5
 * **Rating Score:** 2/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest makes non‑deterministic outputs reproducible by recording and replaying them: use decorators like @bt.snapshot_httpx()/@bt.snapshot_requests() to cassette HTTP/LLM calls and @bt.snapshot_functions(time.time, random.random) to stub random/timestamps. First runs record snapshots (including AI reviews) and cached test returns; subsequent runs replay those snapshots so tests behave deterministically.


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
Install booktest (pip install booktest) and run booktest --setup, then add tests under test/ as functions taking t: bt.TestCaseRun that use t.h1/t.tln/t.tdf/tmetric/etc. to produce snapshots and run them with the CLI (booktest test). Use decorators like @bt.snapshot_httpx(), @bt.snapshot_functions(), and @bt.depends_on() to mock external calls and compose pipeline steps, commit the generated books/ markdown to Git (use DVC for large cassettes) and run in CI with booktest test -pN.


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

Tracking metrics with ±5% tolerance

 * Criteria Score: 16.5/17 = 97.059% (was 97.059%, Δ-0.000%)
 * Rating Score: 9.5/10 = 95.000% (was 95.000%, Δ+0.000%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
