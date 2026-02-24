# Test: LLM Assistant for Booktest Questions

This test evaluates an LLM's ability to answer questions about booktest
using documentation as context.


## Loading Context

Loaded 1001 lines of documentation


## Testing Prompts


### Prompt 1: What is booktest?

**Question:** What is booktest?

**Answer:**
Booktest is a regression-testing tool for data-science and AI systems (LLMs, ML models, NLP pipelines) where outputs are subjective or noisy. It snapshots human-readable markdown outputs in Git, provides tolerance-based metrics and AI-assisted review, and supports dependency caching, HTTP/LLM mocking and DVC for scalable, review-driven testing.


#### Evaluation:

 * Does answer mention snapshot or review-driven testing? Yes
    * The answer explicitly states it 'snapshots human-readable markdown outputs in Git', which mentions snapshot testing.
    * It also explicitly says 'review-driven testing' and refers to 'AI-assisted review', confirming review-driven testing is referenced.
 * Does answer mention data science focus? Yes
    * The answer explicitly calls Booktest a tool for "data-science and AI systems (LLMs, ML models, NLP pipelines)".
    * It references data-science–specific elements (ML models, NLP pipelines, DVC) that confirm a data science focus.
 * Does answer mention Git-tracked results? Yes
    * The answer explicitly states it "snapshots human-readable markdown outputs in Git."
    * It also references review-driven testing and versioning (DVC), reinforcing that results are Git-tracked.

#### Quality ratings:

 * How clear and concise is the explanation? Excellent
    * The answer succinctly defines what Booktest is and its target use case (regression testing for subjective/noisy AI/ML outputs).
    * It concisely lists key features (markdown snapshotting in Git, tolerance metrics, AI-assisted review, caching, HTTP/LLM mocking, DVC) that make the purpose clear and actionable.
 * How compelling is the value proposition for using booktest? Good
    * Targets real, painful gaps in testing LLM/ML outputs (subjective/noisy results) with sensible primitives: Git snapshots of human-readable outputs, tolerance-based metrics, and AI-assisted review.
    * Includes practical engineering features (dependency caching, HTTP/LLM mocking, DVC integration) that enable scalable, review-driven workflows, but the pitch lacks detail on maturity, UX, integration effort and concrete ROI, so it stops short of being clearly 'Excellent'.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.75/2


### Prompt 2: When should I use booktest instead of pytest?

**Question:** When should I use booktest instead of pytest?

**Answer:**
Use booktest for data‑science/LLM scenarios where outputs are subjective or noisy and you need readable markdown snapshots, AI‑assisted review, tolerance‑based metrics, HTTP/LLM mocking and incremental pipeline caching. For traditional deterministic unit tests with strict equality assertions, stick with pytest.


#### Evaluation:

 * Does answer mention expert review needs? Partially
    * The answer explicitly mentions “AI‑assisted review,” which indicates review-related functionality.
    * It does not explicitly state a need for human or expert review or use the phrase “expert review,” so the mention is indirect.
 * Does answer mention non-deterministic or probabilistic results? Yes
    * The answer explicitly refers to "subjective or noisy" outputs, which indicates non-deterministic/probabilistic behavior.
    * It mentions LLM scenarios, tolerance-based metrics and AI-assisted review—features aimed at handling probabilistic, non-deterministic outputs rather than strict deterministic assertions.
 * Does answer mention data science workflows or caching? Yes
    * The answer explicitly mentions "data‑science/LLM scenarios", indicating data science workflows.
    * The answer explicitly mentions "incremental pipeline caching", indicating caching.

#### Quality ratings:

 * How clearly are the use cases differentiated? Excellent
    * Gives a clear, actionable decision rule: use booktest for subjective/noisy DS/LLM outputs and pytest for deterministic strict-equality unit tests.
    * Lists concrete distinguishing features (markdown snapshots, AI-assisted review, tolerance-based metrics, HTTP/LLM mocking, caching) that make the differences easy to evaluate.
 * How helpful would this be for someone choosing a testing framework? Good
    * The answer clearly states the specific scenarios (data‑science/LLM, subjective/noisy outputs) and features (markdown snapshots, AI review, tolerance metrics, mocking, caching) that make booktest preferable over pytest.
    * It is concise and practical but omits broader tradeoffs (maturity, ecosystem, integration examples, performance) that would be needed to be rated Excellent.

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 1.75/2


### Prompt 3: Write a simple booktest example for fizzbuzz

**Question:** Write a simple booktest example for fizzbuzz

**Answer:**
Example test (plain code):

import booktest as bt

def fizzbuzz(n):
    return [("Fizz" if i%3==0 else "") + ("Buzz" if i%5==0 else "") or str(i) for i in range(1, n+1)]

def test_fizzbuzz(t: bt.TestCaseRun):
    out = fizzbuzz(15)
    t.h1("FizzBuzz 1–15")
    t.tln("\n".join(out))
    expected = ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
    correct = sum(o==e for o,e in zip(out, expected)) / len(expected)
    t.key("Correctness:").tmetric(100*correct, tolerance=0)  # 100% expected

This snapshots the 1–15 FizzBuzz output for human/AI review and records a simple correctness metric.


#### Evaluation:

 * Does code include 'import booktest' or 'import booktest as bt'? Yes
    * The code contains the line 'import booktest as bt' at the top.
    * The example uses bt.TestCaseRun and bt-related calls (t.h1, t.tln, t.key, t.tmetric), confirming the import is used.
 * Does code define a test function starting with 'test_'? Yes
    * The provided code includes a function defined as def test_fizzbuzz(...), which begins with the prefix 'test_'.
    * The function signature (t: bt.TestCaseRun) and its body perform testing actions, so it is a test function as required.
 * Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')? Yes
    * The test function is defined as def test_fizzbuzz(t: bt.TestCaseRun) — it declares a parameter typed as bt.TestCaseRun.
    * The parameter t is used throughout the test (t.h1, t.tln, t.key, t.tmetric), showing active use of the TestCaseRun object.
 * Does code use output methods like t.h1() or t.tln()? Yes
    * The test function explicitly calls t.h1("FizzBuzz 1–15") and t.tln("\n".join(out)) to produce output.
    * It also uses t.key(...).tmetric(...) which are additional output/reporting methods from the same API.
 * Is the code syntactically valid Python? Yes
    * All constructs (import, def, list comprehension, annotations, function calls) are syntactically correct Python.
    * The Unicode en dash in the string is allowed in Python 3 source and there are no unmatched parentheses or invalid tokens.

#### Quality ratings:

 * How clear and understandable is the code example? Good
    * The example is concise and correctly demonstrates fizzbuzz logic and basic booktest usage (h1, tln, key, tmetric).
    * The one‑line fizzbuzz comprehension and lack of comments or explanation of booktest APIs may be dense for beginners; also the correctness calculation uses zip which would hide length mismatches.
 * How well does the example demonstrate booktest features? Good
    * The example clearly demonstrates two core booktest features: snapshotting human-readable output (t.h1, t.tln) and recording a numeric metric (t.key(...).tmetric(...)).
    * It is a complete, runnable example (defines fizzbuzz and a test function) so users can try it immediately.
    * The example is minimal and omits other useful booktest capabilities (attachments, diffs, richer assertions/metadata) and has a slight ambiguity in the method name t.tmetric (could be a typo), so it is not a comprehensive or fully documented showcase.

 * **Criteria Score:** 5/5
 * **Rating Score:** 1.5/2


### Prompt 4: How does booktest handle non-deterministic results?

**Question:** How does booktest handle non-deterministic results?

**Answer:**
Booktest makes runs deterministic by snapshotting/replaying external and non-deterministic behavior (e.g. HTTP/LLM calls via @bt.snapshot_httpx() or specific functions via @bt.snapshot_functions(time.time, random.random)), and by caching expensive steps. It also uses tolerance metrics to ignore small metric drift so minor noise doesn't become a failing regression.


#### Evaluation:

 * Does answer mention snapshots or snapshot testing? Yes
    * The answer explicitly says it uses snapshotting/replaying external and non-deterministic behavior.
    * It gives concrete snapshot APIs/examples (e.g. @bt.snapshot_httpx(), @bt.snapshot_functions(...)), which are snapshot testing mechanisms.
 * Does answer mention caching intermediate results? Yes
    * The answer explicitly says it makes runs deterministic "by caching expensive steps."
    * This is a direct mention of using caching to avoid re-computation or variability, i.e., caching intermediate results.
 * Does answer mention mocking functions or environment variables? Partially
    * The answer explicitly mentions snapshotting/mocking specific functions (e.g., @bt.snapshot_functions(time.time, random.random)).
    * It does not mention handling or mocking environment variables anywhere in the response.

#### Quality ratings:

 * How well does the answer explain the technical approach? Good
    * The answer clearly identifies the main technical mechanisms used to control nondeterminism: snapshot/replay of external calls and specific functions, plus caching of expensive steps.
    * It also mentions tolerance metrics to handle small metric drift, which is an important practical detail.
    * It is concise but omits implementation specifics (storage and lifecycle of snapshots, replay modes, configuration of tolerances, or seed management), so it is not a fully exhaustive explanation.
 * How practical and actionable is the explanation? Excellent
    * Gives concrete, implementable mechanisms (snapshot/replay) and specific examples of decorators (@bt.snapshot_httpx(), @bt.snapshot_functions(time.time, random.random)) so a user can apply them immediately.
    * Covers complementary practical measures (caching expensive steps and using tolerance metrics to ignore minor drift), addressing both reproducibility and real-world noise.

 * **Criteria Score:** 2.5/3
 * **Rating Score:** 1.75/2


### Prompt 5: How do I integrate booktest into my existing Python project?

**Question:** How do I integrate booktest into my existing Python project?

**Answer:**
Install with pip (pip install booktest), add tests as normal Python files under test/ using the Booktest API (import booktest as bt) to emit markdown snapshots, metrics and reviews. Run via the CLI (booktest or booktest test), use booktest --setup for optional config, integrate into CI with e.g. booktest test -p8 and use decorators like @bt.snapshot_httpx() to mock expensive HTTP/LLM calls and manage snapshots (-u to accept).


#### Evaluation:

 * Does answer mention 'pip install booktest' or installation? Yes
    * The answer explicitly states "Install with pip (pip install booktest)".
    * It also discusses installation-related commands (CLI usage and --setup), confirming installation is mentioned.
 * Does answer mention creating a test directory? Yes
    * The answer explicitly says to "add tests as normal Python files under test/", which names creating a test directory.
    * It gives concrete instructions to place tests in the test/ folder (and how to run them), so this is a clear mention.
 * Does answer mention running 'booktest' command or CLI? Yes
    * Answer explicitly says to "Run via the CLI (booktest or booktest test)".
    * It lists specific commands/flags such as "booktest --setup", "booktest test -p8", and the "-u" option.

#### Quality ratings:

 * How complete is the integration guide? Good
    * Covers the essential steps: installation, where to place tests, import statement, CLI commands and a CI example so a developer can get started
    * Mentions important integration features (snapshots, metrics, reviews, --setup, -u, and @bt.snapshot_httpx() for mocking) which are directly relevant to integrating into an existing project
    * Not complete: no concrete code/examples of tests or Booktest API usage, no details on configuration options, output locations, or troubleshooting, so additional documentation/examples are needed for full integration
 * How easy would it be to follow these instructions? Good
    * Gives a clear, actionable workflow: install via pip, add tests under test/, import booktest, run via CLI, and integrate into CI.
    * Mentions useful details like --setup, parallel flag (-p8), snapshot decorators, and -u to accept snapshots.
    * Lacks concrete examples, file/naming conventions, and deeper config or error-handling details, so it's not fully beginner-ready for an "Excellent" rating.

 * **Criteria Score:** 3/3
 * **Rating Score:** 1.5/2


## Final Evaluation

Tracking metrics with ±5% tolerance

 * Criteria Score: 16.0/17 = 94.118% (was 100.000%, Δ-5.882<5.000!%)
 * Rating Score: 8.25/10 = 82.500% (was 85.000%, Δ-2.500%)


## Minimum Requirements

Hard requirements that must always pass

 * Criteria score ≥ 13.6 (80%).. ok
 * Rating score ≥ 7.0 (70%).. ok
