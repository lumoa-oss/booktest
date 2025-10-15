# Getting Started with Booktest

Get from zero to testing in **5 minutes**. Each section is copy-pasteable and builds on the previous one.

---

## Installation (30 seconds)

```bash
pip install booktest
```

That's it. No configuration required to start.

---

## Your First Test (2 minutes)

Create a test file:

```bash
mkdir test
cat > test/test_hello.py << 'EOF'
import booktest as bt

def test_hello(t: bt.TestCaseRun):
    t.h1("My First Test")
    t.tln("Hello, World!")
EOF
```

Run it:

```bash
booktest test
```

**What happened?**

Booktest created `books/test/test_hello.md` with your test output:

```markdown
# My First Test

Hello, World!
```

**The magic**: This markdown file is now your **test snapshot**. Change your test output, and booktest will show you the diff. Review it, accept or reject the change.

Try it:

```bash
# Edit test to say "Hello, Booktest!"
# Run again
booktest test

# See the diff - booktest will show you what changed
# Accept the change
booktest test -u
```

**You just learned the core workflow**: Write test → Run → Review changes → Accept/Reject

---

## Your First LLM Evaluation (2 minutes)

Now the real magic - automatically evaluating AI outputs with AI.

```bash
cat > test/test_llm.py << 'EOF'
import booktest as bt

def simple_llm(prompt: str) -> str:
    """Simulates an LLM response"""
    if "capital" in prompt.lower():
        return "Paris is the capital of France."
    return "I don't know."

@bt.snapshot_functions(simple_llm)  # Mock for speed
def test_llm_evaluation(t: bt.TestCaseRun):
    # Generate response
    response = simple_llm("What is the capital of France?")

    # Let AI review AI output
    r = t.start_review()
    r.h1("Generated Response")
    r.iln(response)

    # Automated evaluation
    r.reviewln("Is the response accurate?", "Yes", "No")
    r.reviewln("Is it concise?", "Yes", "No")
EOF
```

Run it:

```bash
# Set your OpenAI key (or use snapshots)
export OPENAI_API_KEY="sk-..."

# Run with snapshot mode to record LLM evaluation
booktest test test/test_llm.py -s -u
```

**What happened?**

1. Your test generated an LLM response
2. **Another LLM evaluated it automatically**
3. The evaluation is saved as a snapshot
4. Next runs reuse the evaluation (instant, free)

**The breakthrough**: No more manually reviewing 500 test cases. AI does it consistently in seconds.

---

## Your First Metric Tracking (1 minute)

Track metrics that can fluctuate (like accuracy) without breaking tests on every tiny change.

```bash
cat > test/test_metrics.py << 'EOF'
import booktest as bt

def test_model_metrics(t: bt.TestCaseRun):
    # Simulate model evaluation
    accuracy = 0.87
    precision = 0.85
    recall = 0.89

    t.h1("Model Performance")

    # Track with tolerance - allows ±5% variation
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
    t.key("Precision:").tmetric(precision, tolerance=0.05)
    t.key("Recall:").tmetric(recall, tolerance=0.05)

    # Hard requirement - must always pass
    t.h2("Minimum Requirements")
    t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)
EOF
```

Run it:

```bash
booktest test test/test_metrics.py -u
```

**What you'll see first run**:

```
Accuracy: 0.870 (baseline)
Precision: 0.850 (baseline)
Recall: 0.890 (baseline)
```

**Change accuracy to 0.88 and run again**:

```
Accuracy: 0.880 (was 0.870, Δ+0.010)  ✅ Within tolerance
```

**Change accuracy to 0.82 and run again**:

```
Accuracy: 0.820 (was 0.870, Δ-0.050<0.05!)  ⚠️ Outside tolerance
```

**The power**: Catch real regressions, ignore noise. No more false alarms from 87% → 86% changes.

---

## What You Just Learned

In 5 minutes you discovered booktest's three superpowers:

1. **Snapshot testing** - Test outputs tracked in Git, review changes like code
2. **AI-assisted evaluation** - Let LLMs review LLM outputs automatically
3. **Tolerance metrics** - Track trends, catch regressions, ignore noise

---

## Real-World Example: Testing an LLM App

Let's combine everything into a realistic scenario:

```python
import booktest as bt
import openai

@bt.snapshot_httpx()  # Mock OpenAI requests for speed
def test_sentiment_classifier(t: bt.TestCaseRun):
    """Test sentiment classification with automated evaluation."""

    # Test data
    reviews = [
        "This product is amazing!",
        "Terrible experience, would not recommend.",
        "It's okay, nothing special.",
    ]

    expected = ["positive", "negative", "neutral"]
    predictions = []

    # Generate predictions (cached after first run)
    for review in reviews:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Classify sentiment: {review}\nRespond with only: positive, negative, or neutral"
            }]
        )
        predictions.append(response.choices[0].message.content.strip().lower())

    # Calculate metrics
    correct = sum(p == e for p, e in zip(predictions, expected))
    accuracy = correct / len(reviews)

    # Show predictions for human review
    t.h1("Predictions")
    for review, pred, exp in zip(reviews, predictions, expected):
        status = "✓" if pred == exp else "✗"
        t.tln(f"{status} \"{review}\" → {pred} (expected: {exp})")

    # Automated LLM evaluation
    r = t.start_review()
    r.h2("Automated Review")
    for review, pred in zip(reviews, predictions):
        r.iln(f"Review: \"{review}\" → {pred}")
        r.reviewln("Is classification reasonable?", "Yes", "No")

    # Track metrics with tolerance
    t.h2("Performance Metrics")
    t.key("Accuracy:").tmetric(100 * accuracy, tolerance=10, unit="%")

    # Hard requirements
    t.h2("Requirements")
    t.assertln("Accuracy ≥ 60%", accuracy >= 0.60)
```

**First run** (5 seconds):
- Makes real OpenAI requests
- Records responses
- LLM evaluates results
- Saves everything as snapshot

**Every subsequent run** (100ms):
- Replays recorded responses (instant, free)
- Reuses LLM evaluation
- Checks metrics against tolerance
- Shows diffs if output changed

**After changing your prompt**:
- See exactly what changed in predictions
- Review if changes are improvements or regressions
- Accept good changes: `booktest test -u`
- Reject bad changes: `git checkout books/`

---

## Configuration (Optional)

Booktest works out of the box, but you can customize it:

```bash
booktest --setup
```

This creates a `.booktest` configuration file where you can set:
- Test directory location
- Output directory location
- Markdown viewer for reviewing results
- Diff tool for comparing changes

**Note**: Configuration is optional. Most users don't need it initially.

---

## Common Workflows

### Development workflow
```bash
# Write/modify test
# Run and see changes
booktest test -v

# Accept changes
booktest test -u

# Commit
git add books/
git commit -m "Update test expectations"
```

### Updating snapshots (HTTP/LLM responses)
```bash
# Capture missing snapshots
booktest test -s

# Recapture all snapshots (use real APIs)
export OPENAI_API_KEY="sk-..."
booktest test -S
```

### Parallel execution
```bash
# Run 8 tests in parallel
booktest test -p8
```

### Running specific tests
```bash
booktest test test/test_llm.py              # One file
booktest test test/test_llm.py::test_eval   # One test
booktest test test/datascience/             # Directory
```

---

## Common Patterns

### Two-tier evaluation (recommended)
```python
def test_model(t: bt.TestCaseRun):
    # Tier 1: Track metrics with tolerance (catch regressions)
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)

    # Tier 2: Hard requirements (must always pass)
    t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)
```

### Expensive operations
```python
def test_expensive(t: bt.TestCaseRun):
    # Cache expensive computation
    embeddings = t.cache(lambda: compute_embeddings(corpus))

    # Use cached result
    similarity = compute_similarity(embeddings)
    t.tln(f"Similarity: {similarity}")
```

### Snapshot testing with pandas
```python
def test_data_pipeline(t: bt.TestCaseRun):
    df = run_pipeline()

    # Snapshot entire DataFrame as markdown table
    t.h1("Pipeline Output")
    t.tdf(df)

    # Track summary statistics
    t.h2("Statistics")
    t.key("Mean:").tmetric(df['value'].mean(), tolerance=0.1)
```

---

## What's Next?

You now know enough to test real projects. Explore more:

### Learn All Features
- **[Complete Feature Guide](docs/features.md)** - Comprehensive documentation of all capabilities
  - Output formatting (headers, tables, code blocks)
  - Tolerance metrics for tracking trends
  - AI-assisted reviews for LLM outputs
  - Snapshots & mocking (HTTP, functions, env vars)
  - Dependencies & resource management
  - DataFrames, images, and visualizations
  - Async support
  - Process setup & teardown

### Common Use Cases
- **[LLM Applications](test/datascience/test_gpt.py)** - Prompt engineering, response quality
- **[ML Models](test/datascience/test_evaluate.py)** - Classification, regression evaluation
- **[Data Pipelines](test/examples/example_book.py)** - DataFrame snapshots, transformations

### Quick References
- **[API Reference](docs/api/testcaserun.py.md)** - Complete API documentation
- **[Workflows & CI](workflows.md)** - Coverage, continuous integration
- **[README](readme.md)** - Overview and three pain points

---

## Troubleshooting

**Q: Test shows DIFF but I didn't change anything**

A: Non-deterministic code (timestamps, random values) needs mocking:
```python
@bt.snapshot_functions(time.time, random.random)
def test_random(t: bt.TestCaseRun):
    # Now deterministic
```

**Q: How do I update just one test's snapshot?**

```bash
booktest test test/test_llm.py -u
```

**Q: HTTP mocking not working**

Make sure decorator is applied:
```python
@bt.snapshot_httpx()  # for httpx
# or
@bt.snapshot_requests()  # for requests library
```

**Q: Tests slow even with caching**

Use parallel execution:
```bash
booktest test -p8  # 8 parallel processes
```

---

## Getting Help

- **Issues**: [github.com/lumoa-oss/booktest/issues](https://github.com/lumoa-oss/booktest/issues)
- **Discussions**: [github.com/lumoa-oss/booktest/discussions](https://github.com/lumoa-oss/booktest/discussions)
- **Examples**: Browse [test/examples/](test/examples/) for copy-pasteable code

---

**Ready to solve real problems?** → [Back to README](readme.md)
