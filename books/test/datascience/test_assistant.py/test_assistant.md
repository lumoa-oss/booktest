# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 585 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
booktest is a review-driven, Jupyter‑book style testing tool for data‑science workflows that uses snapshot testing instead of strict assertions. It lets you print test results as Markdown, cache intermediate results (in memory and on disk) to speed iterative work, and store snapshots in the filesystem and Git for expert review and regression tracking.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
 * Does answer mention data science focus? Yes
 * Does answer mention Git-tracked results? Yes

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
 * How compelling is the value proposition for using booktest? Good

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest when you need review-driven, snapshot testing for data‑science workflows—cases with probabilistic or non‑deterministic outputs, expensive intermediate computations, and a need for Jupyter‑book style visibility and cached results. Use pytest for traditional, deterministic unit tests where strict assertions and classic CI behavior are appropriate.


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
Minimal booktest example printing FizzBuzz from 1 to 15:

```python
import booktest as bt

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz 1-15")
    for i in range(1, 16):
        out = "Fizz"*(i % 3 == 0) + "Buzz"*(i % 5 == 0) or str(i)
        t.tln(out)
```


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
 * Does code define a test function starting with 'test_'? Yes
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
 * Does code use output methods like t.h1() or t.tln()? Yes
 * Is the code syntactically valid Python? Yes

#### Quality ratings:

 * How clear and understandable is the code example? Good
 * How well does the example demonstrate booktest features? Good

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.5/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
It records (“snapshots”) non‑deterministic sources (functions, time/random calls, HTTP requests, env vars, etc.) using decorators like @bt.snapshot_functions, @bt.snapshot_requests/@bt.snapshot_httpx and @bt.snapshot_env, storing inputs/outputs and replaying them so comparisons are deterministic. Snapshots are stored as JSON (so have type limitations), sensitive headers are ignored by default, and you update/capture snapshots with the booktest flags (e.g. -s, -S).


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
Install booktest (pip install booktest), add a test/ directory with your test modules that import booktest and define tests (e.g. using TestCaseRun), then run the CLI (booktest, or booktest -v -i to interactively capture snapshots). Commit the generated books/ markdown snapshots to Git (but add books/*/.out or .out to .gitignore) and run booktest --setup to configure your MD viewer/diff tools if needed.


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

 * Criteria Score: 17/17 = 100.000% (was 94.118%, Δ+5.882%)
 * Rating Score: 8.75/10 = 87.500% (was 95.000%, Δ-7.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
