# Booktest Feature Guide

Complete reference for all Booktest features with examples.

---

## Table of Contents

1. [Output Formatting](#output-formatting)
2. [Tolerance Metrics (New in 1.0)](#tolerance-metrics-new-in-10)
3. [AI-Assisted Review (New in 1.0)](#ai-assisted-review-new-in-10)
   - [Basic Review](#basic-review)
   - [AI-Assisted Diff Review](#ai-assisted-diff-review)
4. [Snapshots & Mocking](#snapshots--mocking)
5. [Dependencies & Resources](#dependencies--resources)
6. [Data Visualization](#data-visualization)
7. [Async Support](#async-support)
8. [Process Setup & Teardown](#process-setup--teardown)
9. [Configuration](#configuration)

---

## Output Formatting

### Headers and Sections

Organize test output into readable sections with headers:

```python
import booktest as bt

def test_headers(t: bt.TestCaseRun):
    t.h1("Main Title")
    t.tln("Content under main title")

    t.h2("Subsection")
    t.tln("Content under subsection")

    t.h3("Sub-subsection")
    t.tln("Detailed content")

    # Alternative syntax
    t.h(4, "Level 4 Header")
```

**Output**: [example](../books/test/examples/example_suite/headers.md)

### Tested vs Ignored Lines

**Tested lines** (`tln`) are compared against snapshots:

```python
def test_comparison(t: bt.TestCaseRun):
    t.h1("Tested Output")
    t.tln("This line is compared")  # Must match snapshot
    t.tln("This too")                # Must match snapshot
```

**Ignored lines** (`iln`) are not compared - use for logs, timestamps, varying content:

```python
import random
import time

def test_with_logs(t: bt.TestCaseRun):
    t.h1("Test Results")
    t.tln("Stable output")

    t.h2("Debug Logs (ignored)")
    for i in range(random.randint(1, 5)):
        t.iln(f"[{time.time()}] Log line {i}")  # Not compared

    t.h2("Final Result")
    t.tln("Expected result")  # Compared
```

**Why?** Random log lengths would break snapshot tests. Headers act as anchors - testing resumes at the next matching header.

### Key-Value Output

Format key-value pairs consistently:

```python
def test_keyvalue(t: bt.TestCaseRun):
    # Inline key
    t.key("Name:").tln("Alice")
    t.key("Age:").tln("30")

    # Key on separate line
    t.keyvalueln("Score:", 95.5)

    # Chained operations
    t.key("Status:").assertln(status == "OK", "Expected OK")
```

**Output**:
```markdown
Name: Alice
Age: 30
Score: 95.5
Status: OK ✓
```

### Multiline Content

Print multiline strings with proper formatting:

```python
def test_multiline(t: bt.TestCaseRun):
    code = """
    def hello():
        print("world")
    """

    t.h1("Code Sample")
    t.icode(code, "python")  # Ignored code block

    t.h1("Expected Output")
    t.tcode(expected, "python")  # Tested code block
```

---

## Tolerance Metrics (New in 1.0)

Track metrics that can fluctuate without breaking tests on minor changes.

### Basic Usage

```python
def test_ml_metrics(t: bt.TestCaseRun):
    accuracy = 0.87

    # Track with ±5% tolerance
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
```

**First run** (establishes baseline):
```
Accuracy: 0.870 (baseline)
```

**Second run** (within tolerance):
```
Accuracy: 0.880 (was 0.870, Δ+0.010) ✓
```

**Third run** (exceeds tolerance):
```
Accuracy: 0.820 (was 0.870, Δ-0.050<0.05!) ⚠️ DIFF
```

### With Units

```python
def test_performance(t: bt.TestCaseRun):
    latency_ms = 145.2
    throughput_rps = 850.5

    t.key("Latency:").tmetric(latency_ms, tolerance=10, unit="ms")
    t.key("Throughput:").tmetric(throughput_rps, tolerance=50, unit="req/s")
```

**Output**:
```
Latency: 145.200ms (was 140.000ms, Δ+5.200ms) ✓
Throughput: 850.500req/s (was 820.000req/s, Δ+30.500req/s) ✓
```

### Two-Tier Evaluation Pattern

Combine tolerance tracking with hard requirements:

```python
def test_model_quality(t: bt.TestCaseRun):
    accuracy = evaluate_accuracy()
    precision = evaluate_precision()

    t.h1("Metrics (with tolerance)")
    t.iln("Track trends, catch regressions")
    t.iln()

    # Tier 1: Track with tolerance
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
    t.key("Precision:").tmetric(precision, tolerance=0.05)

    t.h1("Minimum Requirements")
    t.iln("Hard requirements - must always pass")
    t.iln()

    # Tier 2: Hard thresholds
    t.key("Accuracy ≥ 80%..").assertln(accuracy >= 0.80)
    t.key("Precision ≥ 75%..").assertln(precision >= 0.75)
```

**Why two tiers?**
- **Tolerance metrics**: Catch real regressions (10% drop) while allowing natural variation (±2%)
- **Assertions**: Critical thresholds that must never be crossed

**Example**: [test/test_metrics.py](../test/test_metrics.py)

---

## AI-Assisted Review (New in 1.0)

Let AI evaluate AI outputs automatically - scales to 1000s of test cases.

### Basic Review

```python
@bt.snapshot_httpx()  # Mock OpenAI for fast replay
def test_code_generation(t: bt.TestCaseRun):
    code = generate_code("fizzbuzz in python")

    # Start review section
    r = t.start_review()
    r.h1("Generated Code")
    r.icode(code, "python")

    # AI evaluates automatically
    r.reviewln("Is code syntactically correct?", "Yes", "No")
    r.reviewln("Does it solve fizzbuzz?", "Yes", "No")
    r.reviewln("Code quality?", "Excellent", "Good", "Poor")
```

**First run**: GPT evaluates the code
**Subsequent runs**: Reuses evaluation (instant, free)

### Multi-Choice Reviews

```python
def test_response_quality(t: bt.TestCaseRun):
    response = llm.generate(prompt)

    r = t.start_review()
    r.iln(response)

    # Binary evaluation
    r.reviewln("Accurate?", "Yes", "No")
    r.reviewln("Complete?", "Yes", "No")

    # Multi-choice evaluation
    r.reviewln("Tone?", "Professional", "Casual", "Inappropriate")
    r.reviewln("Length?", "Too Short", "Perfect", "Too Long")
```

### Custom Review Criteria

```python
def test_summarization(t: bt.TestCaseRun):
    article = load_article()
    summary = llm.summarize(article)

    r = t.start_review()
    r.h2("Original Article")
    r.iln(article[:500] + "...")

    r.h2("Generated Summary")
    r.iln(summary)

    r.h2("Evaluation")
    r.reviewln("Captures main points?", "Yes", "Partially", "No")
    r.reviewln("Factually accurate?", "Yes", "Has errors", "Misleading")
    r.reviewln("Appropriate length?", "Yes", "Too short", "Too long")
    r.reviewln("Writing quality?", "Excellent", "Good", "Poor")
```

**Example**: [test/datascience/test_gpt.py](../test/datascience/test_gpt.py)

### Using Alternative LLM Backends

```python
# Configure LLM backend at test level
@bt.use_llm(model="gpt-4")
def test_with_gpt4(t: bt.TestCaseRun):
    r = t.start_review()
    r.reviewln("Quality check?", "Pass", "Fail")

# Or configure globally via environment
# BOOKTEST_LLM_MODEL=gpt-4 booktest test
```

### Environment Setup for AI Review

AI-assisted review requires OpenAI or Azure OpenAI credentials. Set these environment variables:

#### For Azure OpenAI (recommended for production)

```bash
# Required variables
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_API_BASE="https://your-resource.openai.azure.com"
export OPENAI_MODEL="gpt-4"
export OPENAI_DEPLOYMENT="gpt35turbo"
export OPENAI_API_VERSION="2024-08-01-preview"

# Optional
export OPENAI_COMPLETION_MAX_TOKENS=1024  # Default if not set
```

**Get your Azure credentials**:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Find "Keys and Endpoint" in the left menu
4. Copy `KEY 1` as `OPENAI_API_KEY`
5. Copy `Endpoint` as `OPENAI_API_BASE`
6. Note your deployment name from "Deployments" section

#### For Standard OpenAI

```bash
# Required variables
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4"

# Not needed for standard OpenAI
# OPENAI_API_BASE, OPENAI_DEPLOYMENT, OPENAI_API_VERSION
```

**Get your OpenAI API key**:
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Copy and save it (you can't view it again!)

#### Using .env File

Create a `.env` file in your project root (see `.env.example`):

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
# .env file is gitignored by default - never commit it!
```

Load it before running tests:

```bash
# Source env vars
source .env

# Run tests
booktest test
```

#### Testing Without Real API Keys

Use snapshots to run tests without API calls:

```bash
# First run with real API (generates snapshots)
export OPENAI_API_KEY="sk-..."
booktest test -s

# Subsequent runs use snapshots (no API key needed)
booktest test
```

**Result**: After first run with real credentials, all AI evaluations replay from snapshots (instant, free, offline).

### AI-Assisted Diff Review

Let AI analyze test output differences and recommend whether to accept or reject changes.

#### Basic Usage

When tests produce different output (DIFF status), enable AI review to automatically analyze changes:

```bash
# Run tests with AI diff review
booktest -R

# AI review in interactive mode
booktest -R -i
```

**What it does:**
- Analyzes differences between expected and actual test outputs
- Provides 5-category classification with confidence scores
- Auto-accepts clear improvements, auto-rejects clear regressions
- Only prompts for human review on ambiguous cases

#### Classification Categories

AI classifies changes into 5 categories:

1. **FAIL (1)** - Definitive rejection
   - Clear regressions detected
   - Critical errors introduced
   - Auto-rejects without prompting (confidence ≥ 95%)

2. **RECOMMEND FAIL (2)** - Suggest rejection
   - Likely regressions
   - Suspicious changes
   - Prompts user for confirmation

3. **UNSURE (3)** - Requires human judgment
   - Complex changes
   - Ambiguous differences
   - Always prompts user

4. **RECOMMEND ACCEPT (4)** - Suggest acceptance
   - Minor formatting changes
   - Expected improvements
   - Prompts user for confirmation

5. **ACCEPT (5)** - Definitive acceptance
   - No significant changes
   - Clear improvements
   - Auto-accepts without prompting (confidence ≥ 95%)

#### Interactive Mode

In interactive mode (`-i`), press `R` to get AI analysis of test differences:

```bash
booktest -R -i
```

**Example interaction:**
```
test/test_model.py::test_accuracy - DIFF

Expected:
  Accuracy: 87.5%

Actual:
  Accuracy: 85.2%

(a)ccept, (c)ontinue, AI (R)eview, (v)iew, (d)iff? R

AI Review (confidence: 0.92):
  Category: RECOMMEND FAIL

  Rationale: Accuracy dropped from 87.5% to 85.2% (-2.3%).
  This is a meaningful regression that should be investigated.

  Suggestion: Use tolerance metrics (tmetric) to allow natural
  variation while catching real regressions.

Continue without accepting? [y/n]
```

**Smart behavior:**
- Definitive FAIL (1) or ACCEPT (5) → auto-continues, no prompt
- RECOMMEND (2,4) or UNSURE (3) → prompts for user decision

#### Configuration

Adjust AI confidence thresholds in `.booktest` or `booktest.ini`:

```ini
# Require 98% confidence for auto-accept/reject (more conservative)
ai_auto_accept_threshold=0.98
ai_auto_reject_threshold=0.98

# Default is 0.95 (95% confidence)
```

**Higher threshold** = More conservative, prompts user more often
**Lower threshold** = More aggressive, auto-decides more often

#### Workflow Examples

**Non-interactive AI review:**
```bash
# AI reviews all diffs automatically
booktest -R

# Only definitive cases auto-decided
# Ambiguous cases marked for review with AI notes
```

**Interactive with AI assist:**
```bash
# Stop at each diff, press R for AI analysis
booktest -R -i

# Best for: reviewing complex changes with AI guidance
```

**Review only failed tests:**
```bash
# Skip successful tests, AI review failures
booktest -R -c

# Best for: fixing failures after code changes
```

**Verbose AI analysis:**
```bash
# Show full AI rationale and suggestions
booktest -R -v

# Best for: understanding AI reasoning, improving tests
```

#### AI Review Results

AI reviews are stored alongside test outputs:

```
books/
  .out/
    test/
      test_model.md           # Test output
      test_model.ai.json      # AI review result
```

**Why stored?**
- Review AI decisions later
- Track AI accuracy over time
- Debug incorrect classifications
- Include in test reports

#### Force Interactive Mode

Use `-I` (capital I) to force interactive mode even for definitive AI decisions:

```bash
# Always prompt, even for clear ACCEPT/FAIL
booktest -R -I

# Useful for: auditing AI decisions, learning from AI
```

**Example**: [docs/adr/009-ai-assisted-test-review.md](adr/009-ai-assisted-test-review.md)

---

## Snapshots & Mocking

Record external dependencies once, replay forever.

### HTTP Mocking with requests

```python
import booktest as bt
import requests
import json

@bt.snapshot_requests()
def test_api(t: bt.TestCaseRun):
    response = requests.get("https://api.github.com/users/octocat")

    t.h1("User Data")
    t.tln(json.dumps(response.json(), indent=2))
```

**First run**: Makes real HTTP request, records response
**Subsequent runs**: Replays from snapshot (instant, offline)

**Update snapshots**:
```bash
booktest test -s   # Capture missing snapshots
booktest test -S   # Recapture all snapshots
```

### HTTPX Mocking (async support)

```python
import booktest as bt
import httpx
import json

@bt.snapshot_httpx()
def test_openai(t: bt.TestCaseRun):
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Say hello"}]
        },
        headers={"Authorization": f"Bearer {api_key}"}
    )

    t.h1("GPT Response")
    t.tln(response.json()["choices"][0]["message"]["content"])
```

**Headers are ignored by default** to prevent leaking secrets via hashes.

### Function Mocking

Mock non-deterministic or slow functions:

```python
import time
import random

def slow_algorithm(input):
    time.sleep(5)  # Expensive operation
    return random.randint(0, 1000)  # Non-deterministic

@bt.snapshot_functions(time.time, random.randint, slow_algorithm)
def test_algorithm(t: bt.TestCaseRun):
    t.h1("Results")
    t.keyvalueln("Timestamp:", time.time())
    t.keyvalueln("Random:", random.randint(0, 100))
    t.keyvalueln("Algorithm:", slow_algorithm(42))
```

**First run**: 5 seconds, records all outputs
**Subsequent runs**: Instant, replays recorded values

### Environment Variable Mocking

```python
import os

@bt.snapshot_env("API_KEY", "DATABASE_URL")
@bt.mock_missing_env({"API_KEY": "test-key-123"})
def test_with_env(t: bt.TestCaseRun):
    api_key = os.environ["API_KEY"]

    t.h1("Configuration")
    t.iln(f"API Key: {api_key[:8]}...")  # Don't log full key
```

**First run with real env**: Records actual values
**Subsequent runs**: Uses recorded values
**Missing env vars**: Uses mock values

**Example**: [test/examples/snapshots_book.py](../test/examples/snapshots_book.py)

---

## Dependencies & Resources

Share expensive operations between tests and manage exclusive resources.

### Test Dependencies

Cache expensive operations and reuse results:

```python
import booktest as bt

def test_train_model(t: bt.TestCaseRun):
    t.h1("Training Model")
    model = train_large_model()  # Takes 10 minutes

    t.tln(f"Model trained: {model.accuracy}")
    return model  # Cache result

@bt.depends_on(test_train_model)
def test_evaluate_batch_1(t: bt.TestCaseRun, model):
    t.h1("Batch 1 Evaluation")
    predictions = model.predict(batch_1)
    t.tdf(predictions)

@bt.depends_on(test_train_model)
def test_evaluate_batch_2(t: bt.TestCaseRun, model):
    t.h1("Batch 2 Evaluation")
    predictions = model.predict(batch_2)
    t.tdf(predictions)
```

**Result**: Train once (10 min), evaluate batches in parallel (seconds each)

**Cached results**: Stored in `books/.out/` as pickle files

**Example**: [test/examples/simple_book.py](../test/examples/simple_book.py)

### Resource Management

Prevent race conditions with exclusive resources:

```python
import booktest as bt

class Database:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

DB = Database()

@bt.depends_on(bt.resource(DB))
def test_db_write_1(t: bt.TestCaseRun, db):
    t.h1("Write Test 1")
    db.add("item1")
    t.tln(f"DB has {len(db.data)} items")

@bt.depends_on(bt.resource(DB))
def test_db_write_2(t: bt.TestCaseRun, db):
    t.h1("Write Test 2")
    db.add("item2")
    t.tln(f"DB has {len(db.data)} items")
```

**Without resource**: Race conditions in parallel mode
**With resource**: Tests never run simultaneously

**Example**: [test/examples/resource_book.py](../test/examples/resource_book.py)

### Port Pools

Allocate ports for parallel tests without conflicts:

```python
import booktest as bt

@bt.depends_on(port=bt.port_range(10000, 10100))
def test_server_1(t: bt.TestCaseRun, port):
    t.h1(f"Test Server on Port {port}")
    start_server(port)
    test_api(f"http://localhost:{port}")

@bt.depends_on(port=bt.port_range(10000, 10100))
def test_server_2(t: bt.TestCaseRun, port):
    t.h1(f"Test Server on Port {port}")
    start_server(port)  # Different port allocated
    test_api(f"http://localhost:{port}")
```

**Result**: Each test gets a unique port from the pool

**Example**: [test/examples/pool_book.py](../test/examples/pool_book.py)

---

## Data Visualization

### DataFrames as Tables

Display pandas DataFrames as markdown tables:

```python
import booktest as bt
import pandas as pd

def test_dataframe(t: bt.TestCaseRun):
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "score": [95.5, 87.3, 92.1]
    })

    t.h1("User Data")
    t.tdf(df)
```

**Output**:
```markdown
| name    | age | score |
|---------|-----|-------|
| Alice   | 25  | 95.5  |
| Bob     | 30  | 87.3  |
| Charlie | 35  | 92.1  |
```

**Large DataFrames**: Automatically paginated in output

**Example**: [test/examples/example_book.py](../test/examples/example_book.py)

### Dictionaries as Tables

```python
def test_table(t: bt.TestCaseRun):
    data = {
        "x": [1, 2, 3],
        "y": [2, 4, 6],
        "label": ["a", "b", "c"]
    }

    t.h1("Results")
    t.ttable(data)
```

### Images and Plots

Embed matplotlib plots in test output:

```python
import booktest as bt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for determinism
import matplotlib.pyplot as plt

def test_plot(t: bt.TestCaseRun):
    t.h1("Model Performance")

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot([1, 2, 3, 4], [85, 87, 89, 91])
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title("Training Progress")

    # Save to test directory with deterministic metadata
    plot_file = t.file("accuracy.png")
    plt.savefig(plot_file, metadata={'Software': None, 'CreationDate': None})
    plt.close()  # Clean up

    # Embed in markdown
    t.timage(plot_file)
```

**Important**: For deterministic images that work with `rename_file_to_hash()`:
- Use `matplotlib.use('Agg')` before importing pyplot
- Strip metadata with `metadata={'Software': None, 'CreationDate': None}`
- Call `plt.close()` after saving to avoid interference

**Output**: Image displayed in markdown viewer

**Storage**: Images stored in test directory, tracked in Git

**Example**: [test/examples/example_book.py](../test/examples/example_book.py)

---

## Async Support

Run asynchronous tests natively:

```python
import booktest as bt
import asyncio
import httpx

async def test_async_api(t: bt.TestCaseRun):
    t.h1("Async API Test")

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    t.tln(f"Status: {response.status_code}")
```

### Async Dependencies

```python
async def test_create_data(t: bt.TestCaseRun):
    t.h1("Creating Data")
    data = await async_load_data()
    return data

@bt.depends_on(test_create_data)
async def test_process_data(t: bt.TestCaseRun, data):
    t.h1("Processing Data")
    result = await async_process(data)
    t.tln(f"Processed: {len(result)} items")
```

**Example**: [test/examples/async_book.py](../test/examples/async_book.py)

---

## Process Setup & Teardown

Initialize global state before test execution.

### Setup File

Create `__booktest__.py` in your test directory:

```python
# __booktest__.py
def process_setup_teardown():
    # Setup
    initialize_global_state()
    configure_logging()

    yield  # Run tests

    # Teardown
    cleanup_resources()
```

### Example Use Case

```python
# __booktest__.py
import time

def process_setup_teardown():
    # Freeze time for deterministic tests
    from unittest.mock import patch
    with patch('time.time', return_value=1234567890):
        yield

# test_with_time.py
import time

def test_timestamp(t: bt.TestCaseRun):
    t.h1("Timestamp Test")
    t.keyvalueln("Current time:", time.time())  # Always 1234567890
```

**Example**: [test/setup_teardown_test.py](../test/setup_teardown_test.py)

---

## Configuration

### Setup Configuration

Run interactive setup:

```bash
booktest --setup
```

Configures:
- Test directory location
- Output directory location
- Markdown viewer for reviewing results
- Diff tool for comparing changes

### Configuration File

Creates `.booktest` file:

```ini
[paths]
test_dir = test
books_dir = books

[tools]
md_viewer = code  # VS Code
diff_tool = meld   # Meld diff viewer

[execution]
parallel_workers = 8
timeout = 300
```

### Environment Variables

Override settings with environment variables:

```bash
# Override MD viewer
BOOKTEST_MD_VIEWER=typora booktest test -v

# Override test directory
BOOKTEST_TEST_DIR=tests booktest test

# Configure LLM
BOOKTEST_LLM_MODEL=gpt-4 booktest test
```

### Precedence

1. Environment variables (highest)
2. Local `.booktest` file
3. Home directory `~/.booktest` file
4. Built-in defaults (lowest)

---

## Common Workflows

### Development Workflow

```bash
# Write/modify test
# Run and see changes
booktest test -v

# Review changes in markdown viewer
git diff books/

# Accept changes
booktest test -u

# Commit
git add books/
git commit -m "Update test expectations"
```

### Updating Snapshots

```bash
# Capture missing snapshots only
booktest test -s

# Recapture all snapshots (use live APIs)
export OPENAI_API_KEY="sk-..."
booktest test -S

# Update specific test
booktest test test/test_api.py -S
```

### Parallel Execution

```bash
# Use 8 workers
booktest test -p8

# Auto-detect CPU cores
booktest test -p

# With verbose output
booktest test -p8 -v
```

### Running Specific Tests

```bash
# One file
booktest test test/test_llm.py

# One test function
booktest test test/test_llm.py::test_evaluation

# Directory
booktest test test/datascience/

# Pattern matching
booktest test test/test_gpt*
```

---

## API Reference

For complete API documentation, see:
- [TestCaseRun API](testcaserun.py.md) - Main testing API
- [OutputWriter API](output.md) - Output formatting methods
- [Dependencies API](dependencies.md) - Dependency management

---

## Examples

Browse complete working examples:
- [Basic Examples](../test/examples/) - Simple demonstrations
- [Data Science Examples](../test/datascience/) - ML/LLM testing
- [Example Results](../books/index.md) - Generated outputs

---

**Next Steps**:
- [Getting Started Guide](../getting-started.md) - Quick 5-minute intro
- [Workflows & CI](../workflows.md) - Continuous integration setup
- [README](../readme.md) - Overview and use cases
