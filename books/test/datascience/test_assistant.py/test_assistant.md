# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 940 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework for data science that treats test outputs as reviewable markdown snapshots and adds AI-assisted reviews, tolerance-based metrics, and snapshotting/mocking for HTTP/LLM calls. It also provides a build-like dependency system (caching and parallel execution) and DVC integration so you can review, track, and accept/reject changes instead of noisy pass/fail tests.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
 * Does answer mention data science focus? Yes
 * Does answer mention Git-tracked results? Partially

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
 * How compelling is the value proposition for using booktest? Excellent

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 2/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest when you need review-driven, snapshot-based testing for data science—LLM apps, model evaluation, non‑deterministic outputs, or multi‑step/expensive pipelines where you want AI+human review, tolerance metrics, HTTP/LLM mocking, and cached dependencies. For strict unit tests with deterministic, binary pass/fail logic, stick with pytest.


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
Here’s a tiny Booktest example that snapshots the first 15 FizzBuzz outputs for review:

```python
import booktest as bt

def fizzbuzz(n):
    return ["FizzBuzz" if i%15==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else str(i) for i in range(1, n+1)]

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1..15")
    t.tln("\n".join(fizzbuzz(15)))
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
Booktest makes non-deterministic outputs deterministic by recording and replaying snapshots and mocking sources of randomness: use decorators like @bt.snapshot_functions(time.time, random.random) to freeze timestamps/randomness and @bt.snapshot_httpx() (or snapshot_requests/snapshot_functions) to record external HTTP/LLM calls. Subsequent runs reuse these snapshots (and cached test returns), so tests are stable and fast until you deliberately re-record.


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
Install it (pip install booktest) and optionally run booktest --setup to create a config. Then add tests in your repo (e.g. test/ files) using the booktest API (bt.TestCaseRun, t.h1/t.tdf/t.tmetric, decorators like @bt.snapshot_httpx or @bt.depends_on) and run them with booktest test (use -p for parallel, -i for interactive review and -u to update snapshots); call booktest test from your CI to integrate into your pipeline.


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

 * Criteria Score: 16.0/17 = 94.118% (was 70.588%, Δ+23.530<5.000!%)
 * Rating Score: 9.25/10 = 92.500% (was 75.000%, Δ+17.500<10.000!%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
