# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1093 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework for data science that turns test outputs into Git-trackable, human-readable snapshots and adds review-driven workflows (including AI-assisted evaluation) and tolerance-based metrics for non-deterministic ML/LLM outputs. It also provides a build-style dependency system with caching and automatic HTTP/LLM mocking to speed up expensive pipelines and make regressions reviewable rather than simply failing.


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
Use booktest when outputs are non‑deterministic or need expert/AI review — e.g., LLM responses, model evaluation, large data pipelines that need snapshot diffs, tolerance metrics, caching, and incremental runs. For traditional deterministic unit tests with clear pass/fail assertions, stick with pytest.


#### Evaluation:

 * Does answer mention expert review needs? Yes
 * Does answer mention non-deterministic or probabilistic results? Yes
 * Does answer mention data science workflows or caching? Yes

#### Quality ratings:

 * How clearly are the use cases differentiated? Good
 * How helpful would this be for someone choosing a testing framework? Excellent

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
Create test/test_fizzbuzz.py with this content. Run with `booktest test` to snapshot and review the FizzBuzz output.

```python
import booktest as bt

def fizzbuzz(n):
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0: return "Fizz"
    if n % 5 == 0: return "Buzz"
    return str(n)

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1-15")
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
Booktest makes non-deterministic outputs deterministic by snapshotting them on the first run and replaying those recordings thereafter. You can explicitly mock/record unstable sources with decorators like @bt.snapshot_httpx(), @bt.snapshot_functions(time.time, random.random) or @bt.snapshot_gpt(), so timestamps/HTTP/LLM/randomness are recorded and only change when you re-capture snapshots.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
 * Does answer mention caching intermediate results? Yes
 * Does answer mention mocking functions or environment variables? Yes

#### Quality ratings:

 * How well does the answer explain the technical approach? Excellent
 * How practical and actionable is the explanation? Excellent

 * **Criteria Score:** 3/3
 * **Rating Score:** 2/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install booktest (pip install booktest) and optionally run booktest --setup to create a config. Add tests under test/ using the booktest API (t.h1/t.tln/t.tdf, t.tmetric, r = t.start_review(), and decorators like @bt.snapshot_httpx() / @bt.depends_on()), run them with booktest test (use -p8 for CI), and commit the generated books/ snapshots (large cassettes can be stored in DVC).


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

 * Criteria Score: 17/17 = 100.000% (was 97.059%, Δ+2.941%)
 * Rating Score: 9.0/10 = 90.000% (was 95.000%, Δ-5.000%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
