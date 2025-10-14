# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 585 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a review-driven, snapshot testing tool for data‑science workflows that combines Jupyter‑book style result reporting with regression testing. It caches intermediate results, stores human‑readable MD "books" (and snapshots) in the filesystem/Git, and compares new outputs to prior snapshots instead of strict assertions.


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
Use booktest when you need review-driven, snapshot-style testing for data‑science workflows — e.g. fuzzy or probabilistic outputs, rich human-readable results (tables, images, MD), long/expensive pipelines with cached intermediate steps, or HTTP/env snapshots and resource management. For strict unit tests and assertion-based checks use pytest; booktest complements pytest for regression-by-inspection and iterative data‑analysis development.


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
Here's a minimal booktest fizzbuzz example:

```python
import booktest as bt

def test_fizzbuzz(t: bt.TestCaseRun):
    t.h1("FizzBuzz")
    for i in range(1, 21):
        if i % 15 == 0:
            t.tln("FizzBuzz")
        elif i % 3 == 0:
            t.tln("Fizz")
        elif i % 5 == 0:
            t.tln("Buzz")
        else:
            t.tln(str(i))
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
Booktest handles non-determinism by snapshotting outputs and external interactions: you can use decorators like snapshot_functions, snapshot_requests/snapshot_httpx and snapshot_env (and mock_missing_env) to record function inputs/outputs, HTTP calls and env values into JSON snapshots that are compared against future runs. For variable/ordering content it also provides headers/anchors and ignored lines to tolerate or skip volatile output, and you can capture or recapture snapshots with the -s / -S flags.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
 * Does answer mention caching intermediate results? Partially
 * Does answer mention mocking functions or environment variables? Yes

#### Quality ratings:

 * How well does the answer explain the technical approach? Excellent
 * How practical and actionable is the explanation? Excellent

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 2/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install booktest (pip install booktest), add a test/ directory with test functions that accept a bt.TestCaseRun (see the README example), and write your test output using the bt API. Run booktest (e.g. booktest -v -i to capture/accept snapshots, then plain booktest for CI), commit the generated books/ files to VCS and add books/**/.out to .gitignore; optionally run booktest --setup to create a .booktest config.


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

 * Criteria Score: 16.5/17 (97.1%)
 * Rating Score: 9.0/10 (90.0%)

 * Require 13.6+ criteria score (80%).. ok
 * Require 7.0+ rating score (70%).. ok
