# Booktest - Review-Driven Testing for Data Science

[![PyPI version](https://img.shields.io/pypi/v/booktest.svg)](https://pypi.org/project/booktest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/lumoa-oss/booktest)](https://github.com/lumoa-oss/booktest/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/lumoa-oss/booktest)](https://github.com/lumoa-oss/booktest/commits/main)

Booktest is a regression testing tool for systems where outputs aren't strictly right or wrong — ML models, LLM applications, NLP pipelines, and other data science systems that need expert review rather than binary assertions.

<p align="center">
  <img src="docs/assets/demo.gif" alt="Booktest Demo" width="700">
</p>

In these systems, the hard problem isn't checking correctness — it's **seeing what changed**. When you update a prompt, retrain a model, or tweak parameters, behavior shifts across the system. You need to see what changed, understand how, and decide whether it's acceptable. Traditional test frameworks aren't built for this.

Booktest captures test outputs as readable markdown, tracks them in Git, and makes behavioral changes reviewable — the same way you review code. Tolerance metrics separate real regressions from noise. AI evaluation scales review beyond what humans can do manually. A build-system-style dependency graph lets you iterate on one step of a pipeline without re-running everything before it.

Built by [Netigate](https://www.netigate.net/) (formerly Lumoa) after years of production use testing NLP models processing millions of customer feedback messages.

```python
import booktest as bt

def test_gpt_response(t: bt.TestCaseRun):
    response = generate_response("What is the capital of France?")

    # Capture output as reviewable markdown
    t.h1("GPT Response")
    t.iln(response)

    # AI evaluates AI outputs
    r = t.start_review()
    r.iln(response)
    r.reviewln("Is response accurate?", "Yes", "No")
    r.reviewln("Is it concise?", "Yes", "No")

    # Tolerance metrics - catch regressions, ignore noise
    accuracy = evaluate_accuracy(response)
    t.tmetric(accuracy, tolerance=0.05)  # 85% ± 5% = OK
```

```bash
# Review changes interactively
booktest -v -i

# See exactly what changed:
?  * Prediction: 54% Positive (should be Negative)     |  * Prediction: 51% Negative (ok)
?  * Accuracy: 93.3% (was 98.4%, delta -5.1%)

    test_model DIFF 3027 ms
    (a)ccept, (c)ontinue, (q)uit, (v)iew, (l)ogs, (d)iff or fast (D)iff
```

---

## The Three Problems Booktest Solves

### 1. No Correct Answer

Traditional software testing has clear pass/fail:
```python
assert result == "Paris"  # Clear right/wrong
```

Data science doesn't:
```python
# Which is "correct"?
result1 = "Paris"
result2 = "The capital of France is Paris, which is located..."
result3 = "Paris, France"

assert result == ???  # No single correct answer
```

You need expert review, statistical thresholds, human judgment — but manual review doesn't scale to 1,000 test cases.

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
    t.tmetric(accuracy, tolerance=0.05)  # 85% +/- 5% = OK
```

Three-tier quality control: human review via markdown, AI evaluation at scale, tolerance metrics for trends.

---

### 2. Regressions Without Visibility

This is the scenario every data scientist recognizes:

- Change one prompt -> 47 tests fail
- Update training data -> model behaves differently everywhere
- Tweak hyperparameters -> metrics shift across the board
- Upgrade a library -> output formats change subtly

Traditional testing gives you binary pass/fail, no visibility into what actually changed, and no way to accept "close enough" changes.

**Booktest treats test outputs like code:**

```python
def test_model_predictions(t: bt.TestCaseRun):
    model = load_model()
    predictions = model.predict(test_data)

    # Snapshot everything as markdown
    t.h1("Model Predictions")
    t.tdf(predictions)  # DataFrame -> readable markdown table

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
?  ?  * Accuracy: 93.3% (was 98.4%, delta -5.1%)
   ...

    test/datascience/test_model.py::test_model_predictions DIFF 3027 ms (snapshots updated)
    (a)ccept, (c)ontinue, (q)uit, (v)iew, (l)ogs, (d)iff or fast (D)iff
```

Regressions become **reviewable**, not catastrophic. Git history tracks how your model evolved.

---

### 3. Expensive Operations, Slow Iteration

A typical ML pipeline: load data, clean, featurize, train, validate, test, generate reports.

Traditional testing forces you to run all steps every time, even when you're only changing the last one.

**Example pipeline:**
1. Prepare data: 10 min
2. Train model A: 5 min
3. Train model B: 5 min
4. Train model C: 5 min
5. Evaluate combined model A+B+C: 4 min
6. Generate reports: 1 min
**Total: 30 minutes** to test a report formatting change

**Booktest is a build system for tests:**

Tests return objects (like Make targets). Other tests depend on them. Change step 6 -> only step 6 re-runs.

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

# Step 3: Evaluate (depends on step 2)
@bt.depends_on(test_train_model)
def test_evaluate(t: bt.TestCaseRun, model):
    results = evaluate(model, test_data)  # 10 minutes
    t.tdf(results)
    return results

# Step 4: Generate report (depends on step 3)
@bt.depends_on(test_evaluate)
def test_report(t: bt.TestCaseRun, results):
    report = generate_report(results)  # 5 minutes
    t.h1("Final Report")
    t.tln(report)
```

**Iteration speed:**
- **Change formatting in step 6?** Only step 6 re-runs (1 min, not 30 min)
- **Change model A params in step 2?** Steps 2 and 5 re-run (9 min, cached step 1)
- **All steps run in parallel?** `booktest test -p8` -> smart scheduling: 20 min instead of 30 min

**Plus HTTP mocking:**
```python
@bt.snapshot_httpx()  # Record once, replay forever
def test_openai_prompts(t):
    response = openai.chat(...)  # 5s first run, instant after
```

Test each pipeline step in isolation, reuse expensive results.

**Real example**: [3-step agent testing](test/datascience/test_agent.py) - Break agent into plan, answer, and validate steps. Iterate on validation logic without re-running plan generation.

---

## How Booktest Compares

| Problem | Jupyter | pytest + syrupy | promptfoo | Booktest |
|---------|---------|----------------|-----------|----------|
| Expert review at scale | Manual | No support | LLM only | AI-assisted |
| Tolerance metrics | None | None | None | Built-in |
| Pipeline decomposition | No | No | No | Built-in |
| Git-trackable outputs | No | Basic | No | Markdown |
| HTTP/LLM mocking | Manual | Complex | No | Automatic |
| Parallel execution | No | Limited | Limited | Native |
| Data science ergonomics | Exploration only | No | No | Yes |

**Jupyter**: Great for exploration, not for regression testing. No automated review, no Git tracking, no CI/CD integration.

**pytest + syrupy**: Built for deterministic outputs. No concept of "good enough" — either exact match or fail.

**promptfoo/langsmith**: LLM-focused evaluation platforms. Missing: dataframe support, metric tracking with tolerance, resource sharing, parallel dependency resolution.

**Booktest**: Combines review-driven workflow + tolerance metrics + snapshot testing + parallel execution for data science.

---

## What's New in 1.1

### Tolerance-Based Metrics

Track metrics with acceptable ranges instead of exact matches:

```python
t.tmetric(accuracy, tolerance=0.05)  # 87% -> 86% = OK
                                      # 87% -> 80% = DIFF

t.assertln("Accuracy >= 80%", accuracy >= 0.80)  # Hard minimum threshold
```

Catch real regressions, ignore noise.

### AI-Powered Review

Two capabilities for scaling test review:

**AI evaluation of outputs** — use LLMs to evaluate LLM outputs:
```python
r = t.start_review()
r.iln(response)
r.reviewln("Is code syntactically correct?", "Yes", "No")
r.reviewln("Does it solve the problem?", "Yes", "No")
```

First run: AI evaluates and records decisions. Subsequent runs: reuses evaluations (instant, deterministic, free). Only re-evaluates when outputs change.

**AI-assisted diff review** — when many tests change output, AI triages which changes need human attention:

```bash
booktest -R        # AI reviews all diffs automatically
booktest -R -i     # Interactive: press 'R' for AI review on individual tests
```

AI classifies changes from ACCEPT (auto-approve) to FAIL (auto-reject), with intermediate categories flagged for human review. See the [Feature Guide](docs/features.md) for details.

### DVC Integration

Large HTTP/LLM snapshots stored in DVC instead of Git. Markdown outputs stay in Git for easy review:

```python
@bt.snapshot_httpx()
def test_gpt(t: bt.TestCaseRun):
    response = openai.chat(...)  # Cassette -> DVC, Git tracks only manifest hash
```

### Auto-Report on Failures

Tests that fail now show a detailed report automatically — no need to remember verbose flags:

```bash
booktest -p8    # Run in parallel; failures show detailed report automatically
```

### Reviewable Changes

Review and selectively accept or reject changes:

```bash
booktest -w       # Interactive review of failures
booktest -u -c    # Accept all changes
```

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

**When tests fail**: Detailed failure report appears automatically.

**Next steps**: See [Getting Started Guide](getting-started.md) for LLM evaluation, metric tracking, and more.

---

## Real-World Examples

**At Netigate**: Testing sentiment classification across 50 languages x 20 topic models x 100 customer segments = 100,000 test combinations. Booktest reduced CI time from 12 hours to 45 minutes while catching 3x more regressions through systematic review.

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
    t.assertln("Accuracy >= 80%", accuracy >= 0.80)
    t.assertln("F1 >= 0.75", f1 >= 0.75)
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

**Review and evaluation:**
- **Human review via markdown** - Git-tracked outputs, review changes like code diffs
- **AI-assisted review** - LLM evaluates outputs automatically; `-R` flag for AI diff review
- **Tolerance metrics and assertions** - Track trends with `tmetric()`, set thresholds with `assertln()`

**Regression management:**
- **Snapshot testing** - Git-track all outputs as markdown
- **Git diff visibility** - See exactly what changed
- **Selective acceptance** - Accept good changes, reject bad ones
- **DVC integration** - Large snapshots outside Git

**Performance and pipeline:**
- **Build system for tests** - Tests return objects, other tests depend on them (like Make/Bazel)
- **Pipeline decomposition** - Turn 10-step pipeline into 10 tests, iterate on any step independently
- **Automatic HTTP/LLM mocking** - HTTP/HTTPX requests recorded and replayed with `@snapshot_httpx()`
- **Parallel execution** - Native multi-core support with intelligent dependency scheduling
- **Resource sharing** - Share expensive resources (models, data) across tests with `@depends_on()`

**Data science ergonomics:**
- **Markdown output** - Human-readable, reviewable test reports
- **DataFrame support** - Snapshot pandas DataFrames as tables
- **Image support** - Snapshot plots and visualizations
- **Environment mocking** - Control and snapshot env vars

---

## Documentation

- **[Getting Started Guide](getting-started.md)** - Your first test
- **[Use Case Gallery](docs/use-cases.md)** - Quick recipes for common scenarios
- **[Complete Feature Guide](docs/features.md)** - Comprehensive documentation of all features
- **[CI/CD Integration](docs/ci-cd.md)** - GitHub Actions, GitLab CI, CircleCI
- **[API Reference](docs/api/README.md)** - Full API documentation
- **[Examples](test/examples/)** - Copy-pasteable examples
- **[Development Guide](development.md)** - Contributing to booktest

---

## Use Cases

**Works well for:**
- Testing LLM applications (ChatGPT, Claude, etc.)
- ML model evaluation and monitoring
- Data pipeline regression testing
- Prompt engineering and optimization
- Non-deterministic system testing
- Exploratory data analysis that needs regression testing

**Not the right fit for:**
- Traditional unit testing (use pytest)
- Testing with strict equality requirements
- Systems without a review component

---

## FAQ

**Q: Why not just use pytest-regtest or syrupy?**
A: Those work well for deterministic outputs. They don't handle tolerance-based metrics, subjective quality review, or large test matrices where you need to scale evaluation.

**Q: Why not promptfoo or langsmith?**
A: They're good for LLM-specific evaluation. Booktest is complementary — it handles the broader data science workflow (dataframes, metrics, resource management, parallel execution) and integrates review-driven testing into your Git workflow.

**Q: Won't AI reviews give inconsistent results?**
A: Reviews are snapshotted. First run records the AI's evaluation, subsequent runs reuse it (instant, deterministic, free). Re-evaluation only happens when output changes.

**Q: Why Git-track test outputs? Won't that bloat my repo?**
A: Markdown outputs are small (human-readable summaries). Large snapshots (HTTP cassettes, binary data) go to DVC. You get reviewable diffs in Git without bloat.

**Q: Does this replace pytest?**
A: No, it complements it. Use pytest for unit tests with clear pass/fail. Use booktest for integration tests, LLM outputs, model evaluation — anything requiring expert review or tolerance.

**Q: How is this different from Make or Bazel?**
A: Similar concept (dependency graph, incremental builds) but purpose-built for testing. Tests return Python objects (models, dataframes), not files. Built-in review workflow, tolerance metrics, parallel scheduling with resource management.

---

## Why "Booktest"?

Test outputs are organized like a book — chapters (test files), sections (test cases), with all results in readable markdown. Review your tests like reading a book, track changes in Git like code.

---

## Community

- **GitHub**: [lumoa-oss/booktest](https://github.com/lumoa-oss/booktest)
- **Issues**: [Report bugs or request features](https://github.com/lumoa-oss/booktest/issues)
- **Discussions**: [Ask questions, share use cases](https://github.com/lumoa-oss/booktest/discussions)

Built by [Netigate](https://www.netigate.net/) - Enterprise feedback and experience management platform.

---

## License

MIT - See [LICENSE](LICENSE) for details.
