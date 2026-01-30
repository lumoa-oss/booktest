# Booktest - Review-Driven Testing for Data Science

[![PyPI version](https://img.shields.io/pypi/v/booktest.svg)](https://pypi.org/project/booktest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/lumoa-oss/booktest)](https://github.com/lumoa-oss/booktest/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/lumoa-oss/booktest)](https://github.com/lumoa-oss/booktest/commits/main)

> Stop playing whack-a-mole with regressions. Stop waiting hours for test suites.
> Stop pretending `assertEqual()` works for "Is this good enough?"

<p align="center">
  <img src="docs/assets/demo.gif" alt="Booktest Demo" width="700">
</p>

Booktest is the first testing framework built for the **three fundamental realities** of data science:

1. **No correct answer** - Results need expert review, not binary pass/fail
2. **Everything breaks everything** - Change one thing, get regressions everywhere
3. **Operations are expensive** - Big data + slow models = productivity death

Built by [Netigate](https://www.netigate.net/) (formerly Lumoa) after years of production experience testing LLM analytics at scale. Used daily to test NLP models processing millions of customer feedback messages.

**Try it in 30 seconds:**
```bash
pip install booktest && echo 'import booktest as bt

def test_hello(t: bt.TestCaseRun):
    t.h1("My First Test")
    t.tln("Hello, World!")' > test_hello.py && booktest test test_hello.py
```

---

## The Three Problems Booktest Solves

### 1. The Good vs Bad Problem 🎯

**Traditional software testing:**
```python
assert result == "Paris"  # ✅ Clear right/wrong
```

**Data science reality:**
```python
# Which is "correct"?
result1 = "Paris"
result2 = "The capital of France is Paris, which is located..."
result3 = "Paris, France"

# This doesn't work:
assert result == ???  # ❌ No correct answer
```

**The issue**: You need expert review, statistical thresholds, human judgment. Manual review doesn't scale to 1,000 test cases.

**Booktest solution:**

```python
import booktest as bt

def test_gpt_response(t: bt.TestCaseRun):
    response = generate_response("What is the capital of France?")

    # 1. Human review via markdown output & Git diffs
    t.h1("GPT Response")
    t.iln(response)

    # 2. AI reviews AI outputs automatically
    r = t.start_review()
    r.iln(response)
    r.reviewln("Is response accurate?", "Yes", "No")
    r.reviewln("Is it concise?", "Yes", "No")

    # 3. Tolerance metrics - catch regressions, not noise
    accuracy = evaluate_accuracy(response)
    t.tmetric(accuracy, tolerance=0.05)  # 85% ± 5% = OK
```

**Result**: Three-tier quality control. Human review via markdown, AI evaluation at scale, tolerance metrics for trends.

---

### 2. The Regression Whack-a-Mole 🔨

**The nightmare every data scientist knows:**

- Change one prompt → 47 tests fail
- Update training data → model behaves differently everywhere
- Tweak hyperparameters → metrics shift across the board
- Upgrade a library → output formats change subtly

**Traditional testing gives you:**
- ❌ Binary pass/fail (not helpful when output is "slightly different")
- ❌ No visibility into what actually changed
- ❌ No way to accept "close enough" changes

**Booktest treats test outputs like code:**

```python
def test_model_predictions(t: bt.TestCaseRun):
    model = load_model()
    predictions = model.predict(test_data)

    # Snapshot everything as markdown
    t.h1("Model Predictions")
    t.tdf(predictions)  # DataFrame → readable markdown table

    # Track metrics
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
    t.key("F1 Score:").tmetric(f1, tolerance=0.05)
```

**Review changes like code:**
```bash
booktest -v -i

# See exactly what changed:
   ...
?  ?  * Prediction: 54% Positive (should be Negative)                          |  * Prediction: 51% Negative (ok)
   ...
?  ?  * Accuracy: 93.3% (was 98.4%, Δ-5.1%) 
   ...

    test/datascience/test_model.py::test_model_predictions DIFF 3027 ms (snapshots updated)
    (a)ccept, (c)ontinue, (q)uit, (v)iew, (l)ogs, (d)iff or fast (D)iff
```

**Result**: Regressions become **reviewable**, not catastrophic. Git history tracks how your model evolved.

---

### 3. The Expensive Operations Problem ⏱️

**The productivity killer:**

You have a 10-step ML pipeline: load data → clean → featurize → train → validate → test → deploy prep.

Traditional testing forces you to:
- ❌ Run all 10 steps every time (even when testing step 7)
- ❌ Wait hours to test a one-line change in the last step
- ❌ Choose between: duplicate code (Jupyter + pytest) or slow iteration

**Example pipeline:**
1. Prepare data: 10 min
2. Train model A: 5 min
3. Train model B: 5 min
4. Train model C: 5 min
5. Evaluate combined model A+B+C: 4 min
6. Generate reports: 1 min 
**Total: 30 minutes** to test a report formatting change

**Booktest is a build system for tests:**

Tests return objects (like Make targets). Other tests depend on them. Change step 7 → only step 7+ re-runs.

```python
# Step 1: Load data (slow, runs once)
def test_load_data(t: bt.TestCaseRun):
    data = expensive_data_load()  # 5 minutes
    t.tln(f"Loaded {len(data)} rows")
    return data  # Cache result

# Step 2: Train model (slow, depends on step 1)
@bt.depends_on(test_load_data)
def test_train_model(t: bt.TestCaseRun, data):
    model = train_large_model(data)  # 20 minutes
    t.key("Accuracy:").tmetric(model.accuracy, tolerance=0.05)
    return model  # Cache result

# Step 3: Evaluate (fast, depends on step 2)
@bt.depends_on(test_train_model)
def test_evaluate(t: bt.TestCaseRun, model):
    results = evaluate(model, test_data)  # 10 minutes
    t.tdf(results)
    return results

# Step 4: Generate report (fast, depends on step 3)
@bt.depends_on(test_evaluate)
def test_report(t: bt.TestCaseRun results):
    report = generate_report(results)  # 5 minutes
    t.h1("Final Report")
    t.tln(report)
```

**Iteration speed:**
- **Change formatting in step 6?** Only step 6 re-runs (1 min, not 30 min)
- **Change model A params in step 2?** Steps 2 and 5 re-run (9 min, cached step 1)
- **All steps run in parallel?** `booktest test -p8` → smart scheduling: 20min, instead of 30min

**Plus HTTP mocking:**
```python
@bt.snapshot_httpx()  # Record once, replay forever
def test_openai_prompts(t):
    response = openai.chat(...)  # 5s first run, instant after
```

**Result**: **40 min → 5 min** for iteration. Test each pipeline step in isolation, reuse expensive results.

**Real example**: [3-step agent testing](test/datascience/test_agent.py) - Break agent into plan → answer → validate steps. Iterate on validation logic without re-running plan generation.

---

## Why Traditional Tools Fail

| Problem | Jupyter | pytest + syrupy | promptfoo | Booktest |
|---------|---------|----------------|-----------|----------|
| Expert review at scale | ❌ Manual | ❌ No support | ⚠️ LLM only | ✅ AI-assisted |
| Tolerance metrics | ❌ None | ❌ None | ❌ None | ✅ Built-in |
| Pipeline decomposition | ❌ No | ❌ No | ❌ No | ✅ Built-in |
| Git-trackable outputs | ❌ No | ⚠️ Basic | ❌ No | ✅ Markdown |
| HTTP/LLM mocking | ❌ Manual | ⚠️ Complex | ❌ No | ✅ Automatic |
| Parallel execution | ❌ No | ⚠️ Limited | ⚠️ Limited | ✅ Native |
| Data science ergonomics | ⚠️ Exploration | ❌ No | ❌ No | ✅ Yes |

**Jupyter**: Great for exploration, terrible for regression testing. No automated review, no Git tracking, no CI/CD integration.

**pytest + syrupy**: Built for traditional software where outputs are deterministic. No concept of "good enough" - either exact match or fail.

**promptfoo/langsmith**: LLM-focused evaluation platforms. Missing: dataframe support, metric tracking with tolerance, resource sharing, parallel dependency resolution.

**Booktest**: Only tool that combines review-driven workflow + tolerance metrics + snapshot testing + parallel execution for data science at scale.

---

## What's New in 1.0

**Making tests maintainable at scale:**

### ✨ Tolerance-Based Metrics

**Before**: Accuracy drops from 87% to 86% → TEST FAILS → false alarm
**After**: Track with ±5% tolerance → only fail on real regressions

```python
# Catch real problems, ignore noise
t.tmetric(accuracy, tolerance=0.05)  # 87% → 86% = OK ✅
                                      # 87% → 80% = DIFF ⚠️

# Set minimum thresholds for critical KPIs
t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)  # Hard requirement
```

**Result**: 90% fewer false alarms, catch real regressions.

### 🤖 AI as North Star

Booktest provides **two AI-powered capabilities** for scaling test review:

#### 1. AI Evaluation of Test Outputs

**Before**: Human reviews 500 LLM outputs → 3 days
**After**: GPT reviews 500 LLM outputs → 5 minutes

```python
# Automated, consistent evaluation that scales
r = t.start_review()
r.iln(response)
r.reviewln("Is code syntactically correct?", "Yes", "No")
r.reviewln("Does it solve the problem?", "Yes", "No")
r.reviewln("Code quality?", "Excellent", "Good", "Poor")
```

**How it works:**
- First run: AI evaluates outputs, records decisions
- Subsequent runs: Reuses evaluations (instant, deterministic, free)
- Only re-evaluates when outputs change

#### 2. AI-Assisted Diff Review

**Before**: 47 tests change output → must manually review each one
**After**: AI reviews diffs → only 3 need human judgment

**Enable with `-R` flag:**

```bash
# AI automatically reviews test differences
booktest -R

# Interactive mode: press 'R' to get AI recommendations
booktest -R -i
```

**5-category classification:**
- **ACCEPT** (5): No significant changes, clear improvements → **auto-accept**
- **RECOMMEND ACCEPT** (4): Minor changes, likely acceptable → prompt user
- **UNSURE** (3): Complex changes requiring human judgment → prompt user
- **RECOMMEND FAIL** (2): Suspicious changes, likely issues → prompt user
- **FAIL** (1): Clear regressions, critical errors → **auto-reject**

**Example workflow:**

```bash
# you update the hello world test
$ booktest -v -I test/examples/hello_book.py::test_hello

# test results:

test test/examples/hello_book.py::test_hello

? # Review criteria:                                           | # This test prints hello world
  
?  - prints 'hello world', freely formatted                    | hello world
  
  # This test prints hello world
  
? Hello world!                                                 | hello world

test/examples/hello_book.py::test_hello DIFF 0 ms
(a)ccept, (c)ontinue, (q)uit, (v)iew, (l)ogs, (d)iff, fast (D)iff or AI (R)eview? R
    Analyzing differences with AI...

    AI Review (confidence: 0.72):
      Category: RECOMMEND ACCEPT
      Summary: Cosmetic formatting changes; semantics preserved, recommend accept

      Rationale:
        The actual output differs only in formatting and added explanatory comments: 'hello world' became 'Hello world!' (capitalization and punctuation) and a short review-criteria header was added. There are no numerical changes or error messages. Semantically the program still prints the expected phrase. If the test is intended to allow free formatting (as the added header even states), these differences are non-functional. If the test harness requires exact-match output, it would fail, but that would be a brittle test rather than a real regression.

      Issues:
        - line 1-3: New header/comments were added (# Review criteria ...), which change output but are non-functional
        - last line: 'hello world' -> 'Hello world!' (capital H and added exclamation) — formatting/punctuation change

      Suggestions:
        - Relax the test to be format-tolerant: compare lowercased/alphanumeric-only forms or use a regex like /hello\s*world/i allowing trailing punctuation
        - Ignore comment/header lines in output comparison (strip lines starting with '#') if they are non-essential
        - If exact match is required, update the expected output to match the intended canonical form or add alternative accepted forms

      ⚠ Flagged for human review

(a)ccept, (c)ontinue, (q)uit, (v)iew, (l)ogs, (d)iff, fast (D)iff or AI (R)eview? a
```

**Smart behavior:**
- Definitive decisions (FAIL/ACCEPT at 95%+ confidence) → auto-decided, no prompt
- Ambiguous cases (RECOMMEND/UNSURE) → prompts for human review
- In non-interactive mode: adds AI notes to test reports

**Configuration:**

```ini
# .booktest or booktest.ini
# Adjust confidence thresholds (default: 0.95)
ai_auto_accept_threshold=0.98  # More conservative
ai_auto_reject_threshold=0.98
```

**Result**: Scalable evaluation without human bottleneck. AI triages obvious cases, humans focus on truly ambiguous changes. Turn 3-day review sessions into 30-minute sessions.

### 💾 DVC Integration

**Before**: Git repo bloated with HTTP/LLM cassettes → slow clones, merge conflicts
**After**: DVC stores snapshots, Git tracks tiny manifest

```python
# HTTP/LLM snapshots stored in DVC, not Git
@bt.snapshot_httpx()
def test_gpt(t: bt.TestCaseRun):
    response = openai.chat(...)  # Cassette → DVC
                                 # Git: only manifest hash

# Markdown outputs still in Git for easy review
t.h1("Results")
t.tdf(predictions)  # Readable markdown table in Git
```

**Result**: Fast Git operations, no repo bloat. Snapshots stored off-Git, markdown diffs stay reviewable.

### 🎯 Auto-Report on Failures

**Before**: Tests fail → "computer says no" → must memorize `-v -L -w -c` spell
**After**: Tests fail → detailed report appears automatically

```bash
booktest -p8                       # Run in parallel
# Failures automatically show detailed report - no extra flags needed!
```

**Result**: See exactly what failed immediately, no flag memorization required.

### ✅ Reviewable Changes

**Before**: 47 tests fail → red/green panic
**After**: See what changed → review → accept or reject

```bash
booktest -w                        # Interactive review of failures
booktest -u -c                     # Accept all changes
```

**Result**: Regressions become manageable, not catastrophic.

---

## Quick Start

```bash
# Install
pip install booktest

# Initialize
booktest --setup

# Create your first test
cat > test/test_hello.py << EOF
import booktest as bt

def test_hello(t: bt.TestCaseRun):
    t.h1("My First Test")
    t.tln("Hello, World!")
EOF

# Run
booktest
# Failures show detailed report automatically - no flags needed!

# Or run with verbose output during execution
booktest -v

# Or run interactively to review each test
booktest -v -i
```

**Output**: Test results saved to `books/test/test_hello.md`

```markdown
# My First Test

Hello, World!
```

**When tests fail**: Detailed failure report appears automatically. No need to memorize flags!

**Next steps**: See [Getting Started Guide](getting-started.md) for LLM evaluation, metric tracking, and more.

---

## Real-World Examples

**At Netigate**: Testing sentiment classification across 50 languages × 20 topic models × 100 customer segments = 100,000 test combinations. Booktest reduced our CI time from 12 hours to 45 minutes while catching 3× more regressions through systematic review.

### LLM Application Testing

```python
@bt.snapshot_httpx()  # Mock OpenAI automatically
def test_code_generation(t: bt.TestCaseRun):
    code = generate_code("fizzbuzz in python")

    r = t.start_review()
    r.h1("Generated Code")
    r.icode(code, "python")

    # Use LLM to evaluate LLM output
    r.reviewln("Is code syntactically correct?", "Yes", "No")
    r.reviewln("Does it solve fizzbuzz?", "Yes", "No")
    r.reviewln("Code quality?", "Excellent", "Good", "Poor")
```

### ML Model Evaluation

```python
def test_sentiment_model(t: bt.TestCaseRun):
    model = load_model()
    predictions = model.predict(test_data)

    t.h1("Predictions")
    t.tdf(predictions)  # Snapshot as table

    # Two-tier evaluation
    t.h2("Metrics (with tolerance)")
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
    t.key("F1 Score:").tmetric(f1, tolerance=0.05)

    t.h2("Minimum Requirements")
    t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)
    t.assertln("F1 ≥ 0.75", f1 >= 0.75)
```

### Agent Testing with Build System

```python
# Step 1: Agent plans approach (slow: loads docs, calls GPT)
@snapshot_gpt()
def test_agent_step1_plan(t: bt.TestCaseRun):
    context = load_documentation()  # Expensive
    plan = llm.create_plan(context)
    return {"context": context, "plan": plan}  # Cache for next steps

# Step 2: Agent generates answer (depends on step 1)
@bt.depends_on(test_agent_step1_plan)
@snapshot_gpt()
def test_agent_step2_answer(t, state):
    answer = llm.generate_answer(state["plan"])  # Uses cached state
    return {**state, "answer": answer}

# Step 3: Agent validates (depends on step 2)
@bt.depends_on(test_agent_step2_answer)
@snapshot_gpt()
def test_agent_step3_validate(t, state):
    validation = llm.validate(state["answer"])
    t.key("Quality:").tmetric(validation.score, tolerance=10)
```

**Iteration speed:**
- Iterating on step 3? Steps 1-2 cached (instant)
- First run: ~30 seconds (3 GPT calls)
- Subsequent runs: ~100ms (all snapshotted)

**Full example:** [test/datascience/test_agent.py](test/datascience/test_agent.py)

More examples: [test/examples/](test/examples/) and [test/datascience/](test/datascience/)

---

## Core Features

**For the Good vs Bad Problem:**
- 📝 **Human review via markdown** - Git-tracked outputs, review changes like code diffs
- 🤖 **AI-assisted review** - LLM evaluates LLM outputs automatically (use `-R` flag for AI diff review)
- 📊 **Tolerance metrics & asserts** - Track trends with `tmetric()`, set thresholds with `assertln()`

**For Regression Whack-a-Mole:**
- 📸 **Snapshot testing** - Git-track all outputs as markdown
- 🔍 **Git diff visibility** - See exactly what changed
- ✅ **Selective acceptance** - Accept good changes, reject bad ones
- 💾 **DVC integration** - Large snapshots outside Git

**For Expensive Operations:**
- 🔧 **Build system for tests** - Tests return objects, other tests depend on them (like Make/Bazel)
- ⚡ **Pipeline decomposition** - Turn 10-step pipeline into 10 tests, iterate on step 7 without re-running 1-6
- 🎭 **Automatic HTTP/LLM mocking** - HTTP/HTTPX requests recorded and replayed with `@snapshot_httpx()`
- 🔄 **Parallel execution** - Native multi-core support with intelligent dependency scheduling
- 🔗 **Resource sharing** - Share expensive resources (models, data) across tests with `@depends_on()`

**Plus:**
- 📝 **Markdown output** - Human-readable, reviewable test reports
- 📊 **DataFrame support** - Snapshot pandas DataFrames as tables
- 🖼️ **Image support** - Snapshot plots and visualizations
- 🌐 **Environment mocking** - Control and snapshot env vars

---

## Documentation

- **[Getting Started Guide](getting-started.md)** - Your first test in 5 minutes
- **[Use Case Gallery](docs/use-cases.md)** - Quick recipes for common scenarios
- **[Complete Feature Guide](docs/features.md)** - Comprehensive documentation of all features
- **[CI/CD Integration](docs/ci-cd.md)** - GitHub Actions, GitLab CI, CircleCI
- **[API Reference](docs/api/README.md)** - Full API documentation
- **[Examples](test/examples/)** - Copy-pasteable examples
- **[Development Guide](development.md)** - Contributing to booktest

---

## Use Cases

**Perfect for:**
- Testing LLM applications (ChatGPT, Claude, etc.)
- ML model evaluation and monitoring
- Data pipeline regression testing
- Prompt engineering and optimization
- Non-deterministic system testing
- Exploratory data analysis that needs regression testing

**Not ideal for:**
- Traditional unit testing (use pytest)
- Testing with strict equality requirements
- Systems without review component

---

## Community

- **GitHub**: [lumoa-oss/booktest](https://github.com/lumoa-oss/booktest)
- **Issues**: [Report bugs or request features](https://github.com/lumoa-oss/booktest/issues)
- **Discussions**: [Ask questions, share use cases](https://github.com/lumoa-oss/booktest/discussions)

Built by [Netigate](https://www.netigate.net/) - Enterprise feedback and experience management platform.

---

## License

MIT - See [LICENSE](LICENSE) for details.

---

---

## FAQ

**Q: Why not just use pytest-regtest or syrupy?**
A: Those are great for traditional software with deterministic outputs. They fail for data science where you need to track metrics with tolerance, review subjective quality, and handle massive test matrices efficiently.

**Q: Why not promptfoo or langsmith?**
A: They're excellent for LLM-specific evaluation dashboards. Booktest is complementary - it handles the full data science workflow (dataframes, metrics, resource management, parallel execution) while integrating review-driven testing into your Git workflow.

**Q: Won't AI reviews give inconsistent results?**
A: No - reviews are snapshotted. First run records GPT's evaluation, subsequent runs reuse it (instant, deterministic, free). You only re-review when output changes.

**Q: Why Git-track test outputs? Won't that bloat my repo?**
A: Markdown outputs are small (human-readable summaries). Large snapshots (HTTP cassettes, binary data) go to DVC. You get reviewable diffs in Git without bloat.

**Q: Does this replace pytest?**
A: No, it complements it. Use pytest for unit tests with clear pass/fail. Use booktest for integration tests, LLM outputs, model evaluation - anything requiring expert review or tolerance.

**Q: How is this different from Make or Bazel?**
A: Similar concept (dependency graph, incremental builds) but purpose-built for data science testing. Tests return Python objects (models, dataframes), not files. Built-in review workflow, tolerance metrics, parallel scheduling with resource management. Think "Make for testing ML pipelines."

---

## Why "Booktest"?

Test outputs are organized like a book - chapters (test files), sections (test cases), with all results in readable markdown. Review your tests like reading a book, track changes in Git like code.

---

**Ready to stop the whack-a-mole?** → [Get Started](getting-started.md)

---

![Booktest - Review-Driven Testing for Data Science](docs/assets/social_preview.png)

*Found this useful? Give us a ⭐ on [GitHub](https://github.com/lumoa-oss/booktest)!*
