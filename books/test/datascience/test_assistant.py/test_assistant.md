# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1017 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a Python testing framework built for data science that treats test outputs as human-reviewable, Git-trackable markdown snapshots and adds AI-assisted reviews and tolerance-based metrics for non‑deterministic outputs. It also provides a build-system for tests (dependencies, caching), automatic HTTP/LLM mocking and parallel execution to speed iteration and manage expensive operations.


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
Use booktest when you're testing ML/LLM/data‑science workflows where outputs are subjective or non‑deterministic and you need human/AI review, tolerance‑based metrics, snapshot diffs, HTTP/LLM mocking, and pipeline caching/dependencies to avoid re-running expensive ops. Use pytest for traditional deterministic unit tests with strict pass/fail assertions.


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
Here's a minimal booktest test that snapshots FizzBuzz output up to 15. 

```python
import booktest as bt

def fizzbuzz(n):
    return ["Fizz"*(i%3==0)+"Buzz"*(i%5==0) or str(i) for i in range(1, n+1)]

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz up to 15")
    seq = fizzbuzz(15)
    for i, s in enumerate(seq, start=1):
        t.tln(f"{i}: {s}")
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
Booktest makes non‑deterministic outputs deterministic by snapshotting and mocking: HTTP/LLM calls and functions can be recorded and replayed (e.g. @bt.snapshot_httpx(), @bt.snapshot_functions(time.time, random.random)), and expensive results can be cached via returns or t.cache().  It also uses tolerance metrics (t.tmetric()) and AI/human review to ignore harmless noise and only flag real regressions.


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
Install it (pip install booktest), run booktest --setup if you want a config, then add booktest-style tests (under test/) using the TestCaseRun API and decorators like @bt.snapshot_httpx()/@bt.depends_on. Run them with the CLI (booktest test or booktest test -p8 for parallel), commit the generated books/ markdown snapshots to Git (use DVC for large HTTP/LLM cassettes) and add booktest test to your CI.


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
 * Does answer mention creating a test directory? Yes
 * Does answer mention running 'booktest' command or CLI? Yes

#### Quality ratings:

 * How complete is the integration guide? Good
 * How easy would it be to follow these instructions? Excellent

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


## Final Evaluation

Tracking metrics with ±5% tolerance

 * Criteria Score: 16.5/17 = 97.059% (was 91.176%, Δ+5.883<5.000!%)
 * Rating Score: 9.5/10 = 95.000% (was 92.500%, Δ+2.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
