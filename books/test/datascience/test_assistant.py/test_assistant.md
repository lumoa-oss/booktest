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
Use booktest when you're testing data‑science or LLM workflows with non‑deterministic or subjective outputs that need human/AI review, tolerance‑based metrics, snapshot diffs, incremental/cached pipeline steps, and HTTP/LLM mocking. For traditional deterministic unit tests with strict equality assertions, stick with pytest.


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
Booktest makes non‑deterministic behavior deterministic by snapshotting external effects: use decorators like @bt.snapshot_httpx(), @bt.snapshot_requests(), or @bt.snapshot_functions(time.time, random.random) to record HTTP/LLM responses and noisy functions on first run and replay them thereafter. It also snapshottes AI reviews (so evaluations are reused), so subsequent runs are fast and repeatable unless the outputs actually change.


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
Install it (pip install booktest) and run booktest --setup, then add tests under test/ that use the Booktest API (functions taking t: bt.TestCaseRun and optional decorators like @bt.snapshot_httpx() or @bt.depends_on()). Run tests with booktest (e.g. booktest test or booktest test -p8), review/accept snapshots (booktest test -u) and commit the generated books/ snapshots (large HTTP/LLM cassettes go to DVC) as part of your repo/CI.


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

 * Criteria Score: 16.5/17 = 97.059% (was 100.000%, Δ-2.941%)
 * Rating Score: 9.25/10 = 92.500% (was 90.000%, Δ+2.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
