# Booktest Use Case Gallery

Quick recipes for common testing scenarios. Each example is minimal and copy-pasteable.

## Quick Reference

| I want to... | Use | Example |
|--------------|-----|---------|
| Test LLM output quality | `t.start_review()` + `reviewln()` | [test_agent.py](../test/datascience/test_agent.py) |
| Mock API calls | `@bt.snapshot_httpx()` | [snapshots_book.py](../test/examples/snapshots_book.py) |
| Track metrics with tolerance | `t.tmetricln(val, tolerance=0.05)` | [test_metrics.py](../test/test_metrics.py) |
| Snapshot DataFrames | `t.tdf(dataframe)` | [example_book.py](../test/examples/example_book.py) |
| Chain test dependencies | `@bt.depends_on(other_test)` | [test_agent.py](../test/datascience/test_agent.py) |
| Snapshot images/plots | `t.timage(figure)` | [example_book.py](../test/examples/example_book.py) |
| AI-review test diffs | `booktest -R -i` | - |

---

## Testing LLM Outputs

**Problem:** LLM responses aren't deterministic. You can't `assertEqual()` on them.

**Solution:** Snapshot the output, use AI to evaluate quality.

```python
import booktest as bt

@bt.snapshot_httpx()  # Record API calls, replay on subsequent runs
def test_llm_response(t: bt.TestCaseRun):
    response = call_llm("Explain testing in one sentence")

    t.h1("LLM Response")
    t.iln(response)

    # AI evaluates AI output
    r = t.start_review()
    r.iln(response)
    r.reviewln("Is it accurate?", "Yes", "No")
    r.reviewln("Is it concise?", "Yes", "No")
```

**First run:** Makes real API call, AI evaluates response
**Subsequent runs:** Replays from snapshot (instant, free, deterministic)

**Full example:** [test/datascience/test_agent.py](../test/datascience/test_agent.py)

---

## Metrics with Tolerance

**Problem:** Model accuracy fluctuates slightly between runs. Don't want false failures.

**Solution:** Track metrics with tolerance bands.

```python
import booktest as bt

def test_model_evaluation(t: bt.TestCaseRun):
    accuracy = 0.973
    f1_score = 0.952
    latency_ms = 42.5

    t.h1("Model Metrics")

    # Allow ±2% fluctuation (absolute)
    t.key("Accuracy:").tmetricln(accuracy, tolerance=0.02)
    t.key("F1 Score:").tmetricln(f1_score, tolerance=0.02)

    # Direction constraint: only fail if latency increases
    t.key("Latency:").tmetricln(latency_ms, tolerance=5, unit="ms", direction="<=")

    # Hard requirement (must always pass)
    t.assertln("Accuracy >= 80%", accuracy >= 0.80)
```

**Output when metric drifts:**
```
Accuracy: 97.3% (was 98.1%, Δ-0.8%) ✓ within tolerance
Latency: 48.2ms (was 42.5ms, Δ+5.7ms) ⚠ DIFF - exceeds tolerance
```

**Full example:** [test/test_metrics.py](../test/test_metrics.py)

---

## Mocking HTTP/API Calls

**Problem:** API calls are slow and cost money. Don't want to hit real APIs in CI.

**Solution:** Automatically record and replay HTTP requests.

```python
import booktest as bt
import httpx

@bt.snapshot_httpx()  # Records all HTTP traffic on first run
def test_weather_api(t: bt.TestCaseRun):
    response = httpx.get("https://api.weather.com/current?city=Helsinki")
    data = response.json()

    t.h1("Weather API Response")
    t.key("Temperature:").tln(f"{data['temp']}°C")
    t.key("Conditions:").tln(data['conditions'])
```

**First run:** Makes real API call, saves response to snapshot
**Subsequent runs:** Replays from snapshot (instant, free, deterministic)

For the `requests` library, use `@bt.snapshot_requests()`.

**Full example:** [test/examples/snapshots_book.py](../test/examples/snapshots_book.py)

---

## Working with DataFrames

**Problem:** Need to review tabular data changes in tests.

**Solution:** Snapshot DataFrames as readable markdown tables.

```python
import booktest as bt
import pandas as pd

def test_data_processing(t: bt.TestCaseRun):
    df = pd.DataFrame({
        'product': ['A', 'B', 'C'],
        'sales': [100, 250, 175],
        'growth': [0.12, 0.08, -0.03]
    })

    t.h1("Sales Report")
    t.tdf(df)  # Renders as markdown table

    t.h2("Summary")
    t.tdf(df[['product', 'growth']])
```

**Output in Git:**
```markdown
| product | sales | growth |
|---------|-------|--------|
| A       | 100   | 0.12   |
| B       | 250   | 0.08   |
| C       | 175   | -0.03  |
```

**Full example:** [test/examples/example_book.py](../test/examples/example_book.py)

---

## Multi-Step Pipelines

**Problem:** 10-step pipeline, want to iterate on step 7 without re-running 1-6.

**Solution:** Use `@depends_on` to create a test dependency graph.

```python
import booktest as bt

# Step 1: Expensive data loading (runs once, cached)
def test_load_data(t: bt.TestCaseRun):
    data = expensive_load()  # 5 minutes
    t.tln(f"Loaded {len(data)} rows")
    return data  # Return value is cached

# Step 2: Depends on step 1
@bt.depends_on(test_load_data)
def test_process_data(t: bt.TestCaseRun, data):
    processed = transform(data)  # Uses cached data
    t.tln(f"Processed {len(processed)} rows")
    return processed

# Step 3: Depends on step 2
@bt.depends_on(test_process_data)
def test_analyze(t: bt.TestCaseRun, processed):
    results = analyze(processed)
    t.tdf(results)
```

**Iteration:** Change step 3 → only step 3 re-runs. Steps 1-2 use cached results.

**Full example:** [test/datascience/test_agent.py](../test/datascience/test_agent.py) - 3-step agent with plan → answer → validate

---

## Images and Visualizations

**Problem:** Need to review plot changes in tests.

**Solution:** Snapshot images, review visually in Git diffs.

```python
import booktest as bt
import matplotlib.pyplot as plt

def test_visualization(t: bt.TestCaseRun):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("Growth Trend")

    t.h1("Visualization")

    # Save to file and embed
    file = t.file("chart.png")
    plt.savefig(file)
    plt.close()

    t.timage(t.rename_file_to_hash(file))
```

**Full example:** [test/examples/example_book.py](../test/examples/example_book.py)

---

## AI-Assisted Diff Review

**Problem:** 50 tests changed output. Manually reviewing each is tedious.

**Solution:** Let AI triage the diffs.

```bash
# AI reviews all diffs, auto-accepts obvious ones
booktest -R

# Interactive mode: AI advises, you decide
booktest -R -i
```

AI categorizes each diff:
- **ACCEPT (5):** Clear improvement or no meaningful change → auto-accept
- **RECOMMEND ACCEPT (4):** Minor changes, likely fine → prompt user
- **UNSURE (3):** Needs human judgment → prompt user
- **RECOMMEND FAIL (2):** Suspicious changes → prompt user
- **FAIL (1):** Clear regression → auto-reject

**Configure LLM provider:**
```bash
# Use Claude
export ANTHROPIC_API_KEY=sk-ant-...

# Or use local Ollama
export OLLAMA_MODEL=llama3.2

# Or use OpenAI
export OPENAI_API_KEY=sk-...
```

---

## Basic Output Methods

Quick reference for common output methods:

```python
def test_output_demo(t: bt.TestCaseRun):
    # Headers
    t.h1("Main Title")
    t.h2("Section")

    # Text output
    t.tln("Tested line")              # Compared against snapshot
    t.iln("Info line")                # Shown but not tested
    t.key("Label:").tln("value")      # Key-value pair

    # Code blocks
    t.tcode("print('hello')", "python")

    # Assertions
    t.assertln("Check passed", condition)

    # Metrics
    t.tmetricln(0.95, tolerance=0.05)

    # Data
    t.tdf(dataframe)                  # Pandas DataFrame
    t.timage(path)                    # Image file
```

| Method | Description | Tested? |
|--------|-------------|---------|
| `t.tln(text)` | Text line | Yes |
| `t.iln(text)` | Info line | No |
| `t.h1()` - `t.h5()` | Headers | Yes |
| `t.tcode(text, lang)` | Code block | Yes |
| `t.tdf(df)` | DataFrame as table | Yes |
| `t.tmetricln(val, tolerance)` | Metric with tolerance | Yes |
| `t.assertln(msg, condition)` | Hard assertion | Yes |
| `t.timage(path)` | Embed image | Yes |

---

## Running Tests

```bash
# Run all tests
booktest

# Verbose output during execution
booktest -v

# Interactive review mode
booktest -v -i

# With AI diff review
booktest -R -i

# Parallel execution (8 cores)
booktest -p8

# Continue on failure (see all results)
booktest -c

# Specific test file
booktest test/examples/hello_book.py

# Specific test function
booktest test/examples/hello_book.py::test_hello
```

---

## More Examples

- **Simple examples:** [test/examples/](../test/examples/)
- **Data science examples:** [test/datascience/](../test/datascience/)
- **Getting started guide:** [getting-started.md](../getting-started.md)
- **Full feature reference:** [docs/features.md](features.md)
