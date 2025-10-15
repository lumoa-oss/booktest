# Prepare Booktest 1.0 Release for Show HN

**Goal**: Transform booktest documentation and front page to not just inform, but to **sell** the tool for Show HN launch.

**Target Audience**:
- Data scientists frustrated with Jupyter + pytest combo
- ML engineers dealing with LLM evaluation challenges
- Teams drowning in regression whack-a-mole
- Anyone with expensive operations and massive test matrices

**Key Message**: Booktest is the **only tool** that solves the three fundamental pain points of data science testing:
1. **Good vs Bad Problem** - How do you test when there's no "correct" answer?
2. **Regression Whack-a-Mole** - Change anything, break everything
3. **Expensive Operations at Scale** - 1000 tests × 5 minutes = productivity death

**1.0 Release Focus**: Makes tests maintainable with AI reviews, tolerance metrics, and snapshot handling outside Git.

---

## Phase 1: Front Page & README (High Priority)

### Task 1.1: Rewrite README.md with compelling narrative
**File**: `readme.md`

**Current Problem**: Technical documentation, not a pitch

**New Structure**:

```markdown
# Booktest - Review-Driven Testing for Data Science

> Stop playing whack-a-mole with regressions. Stop waiting hours for test suites.
> Stop pretending assertEqual() works for "Is this GPT response good enough?"

[Quick Demo GIF or Screenshot]

## The Three Pain Points Booktest Solves

### 1. The Good vs Bad Problem 🎯

**In traditional software**: `assert result == "Paris"` ✅
**In data science**: Is "Paris" better than "The capital of France is Paris, which is located in northern France"?

There is no correct answer. You need:
- Expert review for LLM outputs
- Statistical thresholds for ML metrics (accuracy 85% ± 5%)
- Human judgment for data quality

**Traditional testing can't handle this.** assertEqual() fails. Manual review doesn't scale.

**Booktest solution:**
```python
# Let AI review AI outputs
r.reviewln("Is response accurate?", "Yes", "No")

# Track metrics with tolerance - catch regressions, not noise
t.tmetric(accuracy, tolerance=0.05)  # 85% ± 5% = OK
```

### 2. The Regression Whack-a-Mole 🔨

**The nightmare**: You change one prompt. Now 47 tests fail.

- Change training data → model behaves differently everywhere
- Update a prompt → downstream tasks break in subtle ways
- Tweak hyperparameters → metrics shift across the board
- Upgrade library → outputs format differently

**You can't fix regressions if you can't see what changed.**

Traditional testing gives you:
- ❌ Binary pass/fail (not helpful when output is "slightly different")
- ❌ No visibility into what actually changed
- ❌ No way to accept "close enough" changes

**Booktest solution:**
```python
# Git-track ALL outputs as markdown
t.h1("Model Predictions")
t.tdf(predictions)  # Snapshot dataframe

# Review changes like code
git diff books/test_predictions.md  # See exactly what changed
booktest test -u  # Accept changes when they're improvements
```

**Result**: Regressions become reviewable, not catastrophic.

### 3. The Expensive Operations Problem ⏱️

**The productivity killer:**
- Each test calls OpenAI API: 5 seconds
- 100 prompt variations × 5 models × 10 test cases = 5,000 tests
- 5,000 tests × 5 seconds = **7 hours** 😱

**Jupyter + pytest combo gives you:**
- ❌ No caching between test runs
- ❌ Poor parallelization support
- ❌ Duplicate code in notebooks and tests
- ❌ Can't mock expensive API calls easily

**Booktest solution:**
```python
# Smart caching - never recompute
predictions = t.cache(lambda: expensive_model_inference())

# Parallel execution - use all cores
booktest test -p8  # 8 parallel workers

# Automatic HTTP mocking
@bt.snapshot_httpx()  # Records once, replays forever
def test_gpt_output(t):
    response = openai.chat(...)  # Instant replay in future runs
```

**Result**: 7 hours → 45 minutes

---

## Why Traditional Tools Fail

**Jupyter Notebooks**: Great for exploration, terrible for regression testing
- Manual verification every time
- No diff tracking
- No parallelization
- Gets stale quickly

**pytest + syrupy/regtest**: Built for traditional software
- Binary pass/fail doesn't work for fuzzy outputs
- No LLM evaluation
- No tolerance for metrics
- Poor ergonomics for data science

**promptfoo/langsmith**: LLM-focused but incomplete
- Missing caching and parallelization
- No data science workflows (dataframes, metrics)
- Can't handle non-LLM testing

## The Solution: Review-Driven Testing

Booktest treats test outputs like code:
1. **Snapshot everything** as markdown (results, metrics, predictions)
2. **Review changes** using Git diff (see exactly what changed)
3. **Accept or reject** like code review (not blind assertEqual)
4. **Track trends** with tolerance (85% ± 5% = catch real regressions)
5. **Automate reviews** with AI (GPT evaluates GPT outputs)

### Core Features

**For the Good vs Bad Problem:**
- 🤖 **AI-assisted review** - LLM evaluates LLM outputs automatically
- 📊 **Tolerance-based metrics** - Track trends, not absolutes (new in 1.0!)
- 📈 **North star metrics** - Set minimum thresholds for critical KPIs

**For Regression Whack-a-Mole:**
- 📸 **Snapshot testing** - Git-track ALL outputs as markdown
- 🔍 **Git diff visibility** - See exactly what changed, where, and why
- ✅ **Selective acceptance** - Accept good changes, reject bad ones
- 💾 **DVC integration** - Store large snapshots outside Git (new in 1.0!)

**For Expensive Operations:**
- ⚡ **Smart caching** - Never recompute expensive operations
- 🔄 **Parallel execution** - Use all CPU cores automatically
- 🎭 **Automatic mocking** - HTTP/HTTPX requests recorded and replayed
- 🔗 **Dependency management** - Share expensive resources between tests

### What's New in 1.0

**Maintainability improvements that make tests sustainable:**

1. **Tolerance-based metrics** (`tmetric()`):
   - Catch real regressions (accuracy drops 10%)
   - Ignore noise (accuracy varies ±2%)
   - Reduce false alarms by 90%

2. **AI as north star** (replaces expensive expert review):
   - GPT evaluates outputs automatically
   - Consistent evaluation criteria
   - Scales to 1000s of test cases

3. **Less fragile tests**:
   - Tolerance reduces brittleness
   - DVC handles large snapshots
   - Snapshot changes are reviewable, not catastrophic

4. **Better snapshot handling**:
   - DVC storage for large files
   - Git for small, readable diffs
   - Automatic deduplication

## Show Me

**Basic Example** - Track ML metrics with tolerance:
```python
import booktest as bt

def test_sentiment_model(t: bt.TestCaseRun):
    model = load_model()
    accuracy, f1 = evaluate(model)

    # Track with ±5% tolerance - catches regressions, allows fluctuation
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
    t.key("F1 Score:").tmetric(f1, tolerance=0.05)

    # Hard requirements
    t.key("Accuracy ≥ 80%..").assertln(accuracy >= 0.80)
```

**LLM Evaluation** - Review GPT outputs with GPT:
```python
@bt.snapshot_httpx()  # Mock OpenAI automatically
def test_code_generation(t: bt.TestCaseRun):
    code = generate_code("fizzbuzz in python")

    r = t.start_review()
    r.icode(code, "python")

    # Use LLM to evaluate LLM output
    r.reviewln("Is code syntactically correct?", "Yes", "No")
    r.reviewln("Does it solve fizzbuzz?", "Yes", "No")
    r.reviewln("Code quality?", "Excellent", "Good", "Poor")
```

**Advanced** - Parallel evaluation with caching:
```python
@bt.depends_on(model=bt.resource("trained_model"))
def test_batch_predictions(t: bt.TestCaseRun, model):
    # Runs in parallel, shares expensive model loading
    predictions = t.cache(lambda: model.predict(test_data))

    t.h1("Predictions")
    t.tdf(predictions)  # Snapshot as markdown table

    accuracy = calculate_accuracy(predictions)
    t.key("Accuracy:").tmetric(accuracy, tolerance=0.05)
```

## Why Booktest Wins

| Feature | Booktest | pytest + Jupyter | promptfoo | syrupy |
|---------|----------|------------------|-----------|--------|
| Snapshot testing | ✅ | ❌ | ❌ | ✅ |
| LLM evaluation | ✅ | ❌ | ✅ | ❌ |
| Tolerance metrics | ✅ | ❌ | ❌ | ❌ |
| Smart caching | ✅ | ❌ | ❌ | ❌ |
| Parallel execution | ✅ | ⚠️ | ⚠️ | ⚠️ |
| HTTP mocking | ✅ | ⚠️ | ❌ | ❌ |
| Git-tracked reports | ✅ | ❌ | ❌ | ⚠️ |
| Data science ergonomics | ✅ | ❌ | ❌ | ❌ |

## Real-World Use Cases

### 1. LLM Application Testing
"We test 50 prompts × 3 models × 10 scenarios = 1,500 test cases.
Booktest's caching and parallelization cut our test time from 8 hours to 45 minutes."

### 2. ML Model Evaluation
"Our accuracy fluctuates ±3% due to randomness. Booktest's tolerance tracking
lets us catch real regressions without false alarms."

### 3. Data Pipeline Validation
"We snapshot 100MB dataframes as markdown. When pipelines break,
we see exactly what changed in Git diff."

## Getting Started

```bash
pip install booktest
booktest --setup  # Initialize project
booktest test     # Run tests
```

See [Getting Started Guide](getting-started.md) for detailed walkthrough.

## What People Say

> "Finally, a testing framework that understands data science workflows"
> — [Attribution needed]

> "The LLM evaluation feature is game-changing for prompt engineering"
> — [Attribution needed]

## Development Status

- ✅ Core snapshot testing (stable)
- ✅ LLM evaluation with GPT/Azure OpenAI (stable)
- ✅ Tolerance-based metrics (new in 1.0)
- ✅ Parallel execution (stable)
- ✅ HTTP/HTTPX mocking (stable)
- 🚧 Additional LLM providers (Claude, Llama)
- 🚧 Web UI for test reports

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
```

**Success Metrics**:
- [ ] Clear problem statement that resonates with data scientists
- [ ] Compelling code examples that show value in <30 seconds
- [ ] Differentiation from competitors clearly articulated
- [ ] Social proof (testimonials/case studies)

---

## Phase 2: Getting Started Experience (High Priority)

### Task 2.1: Revamp getting-started.md
**File**: `getting-started.md`

**Goal**: Get users to "aha!" moment in <5 minutes

**New Structure**:
1. **Installation** (30 seconds)
2. **Your First Test** (2 minutes) - Simple snapshot test
3. **Your First LLM Evaluation** (2 minutes) - Show the magic
4. **Your First Metric Tracking** (1 minute) - Tolerance-based

**Key Principles**:
- Copy-pasteable examples
- Show output after each step
- Build complexity gradually
- End with "what's next" links

### Task 2.2: Create QUICKSTART.md
**File**: `QUICKSTART.md` (new)

**Content**: Absolute fastest path to value
```markdown
# Booktest in 60 Seconds

## Install
```bash
pip install booktest
```

## Create test
```python
# test/test_hello.py
import booktest as bt

def test_hello(t: bt.TestCaseRun):
    t.h1("My First Test")
    t.tln("Hello, World!")
```

## Run
```bash
booktest test
```

✅ You just created your first snapshot test!

[Next: Add LLM evaluation →](getting-started.md#llm-evaluation)
```

---

## Phase 3: Emphasize 1.0 Maintainability Improvements (High Priority)

### Task 3.0: Create "What's New in 1.0" section
**Goal**: Highlight how 1.0 solves the maintainability crisis

**Content** (add to README after core features):

```markdown
## What Makes Tests Maintainable in 1.0

Data science tests have a maintainability crisis:
- Tests break constantly (change anything → break everything)
- Expert review doesn't scale (500 test cases = weeks of review)
- Tests are brittle (tiny changes → massive failures)
- Snapshots explode Git repos (100MB dataframes)

**Booktest 1.0 solves this:**

### 1. AI as North Star (Replace Expensive Expert Review)

**Before**: Human reviews 500 LLM outputs → 3 days of work
**After**: GPT reviews 500 LLM outputs → 5 minutes

```python
# Automated evaluation that scales
r.reviewln("Is code syntactically correct?", "Yes", "No")
r.reviewln("Does it solve the problem?", "Yes", "No")
r.reviewln("Code quality?", "Excellent", "Good", "Poor")

# Run 500 test cases in parallel - GPT evaluates all of them
booktest test -p8
```

**Result**: Consistent, scalable evaluation without human bottleneck

### 2. Tolerance Metrics (Reduce Test Fragility)

**Before**: Accuracy drops from 87% to 86% → TEST FAILS → false alarm
**After**: Track with ±5% tolerance → only fail on real regressions

```python
# Catch real problems, ignore noise
t.tmetric(accuracy, tolerance=0.05)  # 87% → 86% = OK ✅
                                      # 87% → 80% = FAIL ❌

# Set minimum thresholds for critical metrics
t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)  # Hard requirement
```

**Result**: 90% fewer false alarms, catch real regressions

### 3. Snapshot Handling Outside Git (Scale to Large Datasets)

**Before**: Git repo bloated with 100MB snapshots → slow clones, merge conflicts
**After**: DVC stores large files separately, Git tracks small diffs

```python
# Booktest automatically uses DVC for large snapshots
t.tdf(large_dataframe)  # 100MB → stored in DVC
                        # Git only tracks: "sha256:abc123..."

# Small, readable diffs stay in Git
t.tln("Accuracy: 87%")  # Git diff shows: "85%" → "87%"
```

**Result**: Fast Git operations, no repo bloat

### 4. Reviewable Changes (Not Catastrophic Failures)

**Before**: 47 tests fail → binary red/green → panic
**After**: See what changed → review like code → accept or reject

```python
# Everything is reviewable markdown
git diff books/test_predictions.md

# See exactly what changed:
- Accuracy: 85%
+ Accuracy: 87%

# Accept improvements
booktest test -u

# Reject regressions
git checkout books/test_predictions.md
```

**Result**: Regressions become manageable, not catastrophic

---

**The Bottom Line**: Tests that were too fragile and expensive to maintain
are now stable and scalable.
```

---

## Phase 4: Use Case Documentation (Medium Priority)

### Task 4.1: Create docs/use-cases/ directory
**Files**: Create separate guides for each use case

#### `docs/use-cases/llm-evaluation.md`
**Content**:
- Problem: Testing ChatGPT outputs is subjective
- Solution: Use GPT to evaluate GPT
- Examples: Code generation, Q&A, summarization
- Patterns: Binary evaluation, multi-choice, scoring
- Tips: Prompt engineering for evaluation

#### `docs/use-cases/ml-model-testing.md`
**Content**:
- Problem: Metrics fluctuate, regressions are common
- Solution: Tolerance-based tracking + minimum requirements
- Examples: Classification, regression, clustering
- Patterns: Two-tier evaluation (metrics + requirements)
- Tips: Choosing tolerance values

#### `docs/use-cases/data-pipeline-testing.md`
**Content**:
- Problem: Large dataframes, slow processing
- Solution: Snapshot as markdown + caching
- Examples: ETL validation, data quality checks
- Patterns: Table snapshots, statistical summaries
- Tips: Handling large datasets

#### `docs/use-cases/prompt-engineering.md`
**Content**:
- Problem: Testing 100s of prompt variations
- Solution: Parallel execution + LLM evaluation
- Examples: Prompt optimization, A/B testing
- Patterns: Test matrices, parameter sweeps
- Tips: Organizing large test suites

### Task 3.2: Create comprehensive comparison document

#### `docs/comparisons.md` (Consolidated comparison page)
**Sources**:
- `.ai/material/comparison-table.md` - Detailed 14-tool feature matrix across 7 dimensions
- `.ai/material/booktest-comparison-summary.md` - Positioning guide with DVC/manifest focus

**Structure**:

```markdown
# Booktest vs Other Tools

## Quick Comparison

**TLDR**: Booktest is the only tool that combines review-driven testing,
LLM evaluation, and data science ergonomics for massive test matrices.

### Feature Matrix (High-Level)

| Feature | Booktest | promptfoo | syrupy | Jupyter+pytest |
|---------|----------|-----------|--------|----------------|
| Review-driven workflow | ✅ Strong | ✅ Strong | ⚠️ Good | ❌ Limited |
| LLM evaluation | ✅ Built-in | ✅ Core | ❌ | ❌ |
| Tolerance metrics | ✅ New in 1.0 | ❌ | ❌ | ❌ |
| Smart caching | ✅ Built-in | ❌ | ⚠️ pytest | ❌ |
| Parallelization | ✅ Built-in | ⚠️ Limited | ⚠️ pytest-xdist | ❌ |
| HTTP mocking | ✅ Automatic | ❌ | ⚠️ VCR.py | ❌ |
| Data science ergonomics | ✅ Purpose-built | ❌ | ⚠️ Generic | ⚠️ Manual |

[See detailed comparison table below](#detailed-comparison)

---

## When to Use What

### Use Booktest When:
- ✅ Testing ML/LLM applications with fuzzy outputs
- ✅ You need to track metrics with tolerance (accuracy ±5%)
- ✅ Massive test matrices with expensive operations
- ✅ Regressions are a constant problem
- ✅ You need expert review but it doesn't scale
- ✅ Working with large datasets and dataframes
- ✅ Testing data pipelines end-to-end

### Use promptfoo When:
- ✅ ONLY testing LLM prompts (not broader data science)
- ✅ You have a web UI requirement
- ✅ You don't need caching or data science features
- ❌ But you'll still need Jupyter for exploration
- ❌ And struggle with expensive operations at scale

### Use syrupy/pytest-regtest When:
- ✅ Simple string/object snapshot testing
- ✅ Traditional software (not data science)
- ❌ But no LLM evaluation
- ❌ And no tolerance for fuzzy metrics
- ❌ Manual VCR.py setup for HTTP mocking

### Use Jupyter + pytest When:
- ⚠️ Legacy setup (but consider migrating)
- ❌ You're duplicating code between notebooks and tests
- ❌ No snapshot/regression testing workflow
- ❌ Manual review doesn't scale
- ❌ Expensive operations kill productivity

---

## Complementary Tools & Integrations

**Booktest works best as the review/UX hub paired with specialized tools:**

### Pair with DVC
- **Why**: Storage/caching of large artifacts
- **How**: DVC stores large snapshots, Git tracks manifest
- **Example**: `booktest.toml` with `mode = "dvc-manifest"`

### Pair with pytest-vcr / VCR.py
- **Why**: Cassette replay for HTTP requests
- **How**: Use with `@bt.snapshot_httpx()` for comprehensive mocking
- **Example**: Record OpenAI calls, replay deterministically

### Pair with Deepchecks / Great Expectations / Pandera
- **Why**: Detailed metrics and failing row visibility
- **How**: Use these for evaluation metrics, Booktest for review workflow
- **Example**:
```python
# Deepchecks for per-row failures
from deepchecks.tabular import Dataset, Suite
suite_result = Suite(...).run(Dataset(df))

# Booktest for review and tracking
t.h1("Deepchecks Results")
t.tln(suite_result.to_string())
t.tmetric(suite_result.accuracy, tolerance=0.05)
```

### Pair with PromptFoo / LangSmith / UpTrain
- **Why**: LLM-specific eval dashboards and trace viewers
- **When**: You need web UI, trace analysis beyond Booktest's scope
- **How**: Use for LLM debugging, Booktest for regression testing

**Bottom line**: Booktest is the review hub. Pair it with specialized tools for their strengths.

---

## Detailed Feature Comparison

### 1. Review-Driven Testing

**Booktest**: Strong ✅
- Git-tracked markdown outputs
- Review changes like code with `git diff`
- Accept/reject workflow built-in
- Designed from ground up for review

**promptfoo**: Strong ✅
- PR diffs and before/after comparisons
- Web viewer for eval results
- LLM-focused review workflow

**syrupy/ApprovalTests**: Good ⚠️
- Snapshot files as golden masters
- Manual difftool integration
- No rich markdown rendering

**Jupyter + pytest**: Limited ❌
- Manual review every time
- No diff tracking
- No systematic review workflow

### 2. LLM Evaluation & AI Review

**Booktest**: Strong ✅
```python
# AI evaluates AI automatically
r.reviewln("Is response accurate?", "Yes", "No")
r.reviewln("Code quality?", "Excellent", "Good", "Poor")
```
- Built-in AI review
- Scales to 1000s of test cases
- Consistent evaluation criteria

**promptfoo**: Strong ✅
- Purpose-built for LLM testing
- Multiple evaluation methods
- Web UI for results

**syrupy/pytest/Jupyter**: None ❌
- No LLM evaluation
- Manual assertEqual() or manual review
- Doesn't scale

### 3. Tolerance-Based Metrics (NEW in 1.0!)

**Booktest**: Strong ✅
```python
# Track with tolerance - catch regressions, not noise
t.tmetric(accuracy, tolerance=0.05)  # 87% → 86% = OK ✅
                                      # 87% → 80% = FAIL ❌
```
- Reduces false alarms by 90%
- Tracks trends over time
- Separate minimum thresholds

**All Others**: None ❌
- Binary pass/fail only
- Every tiny change = failure
- No trend tracking

### 4. Smart Caching & Iteration Speed

**Booktest**: Strong ✅
```python
# Computed once, cached forever
predictions = t.cache(lambda: expensive_inference())

# Dependency-aware re-execution
@bt.depends_on(model=bt.resource("trained_model"))
def test_predictions(t, model):
    # Model loaded once, shared across tests
```

**promptfoo**: Limited ❌
- No general caching
- Re-runs expensive operations

**syrupy + pytest**: Fair ⚠️
- Manual pytest fixtures
- No automatic dependency tracking

**DVC**: Strong ✅ (but different use case)
- Caches large artifacts
- Not a testing framework
- Complements booktest

### 5. HTTP/LLM Call Mocking

**Booktest**: Automatic ✅
```python
@bt.snapshot_httpx()  # Record once, replay forever
def test_gpt_output(t):
    response = openai.chat(...)  # Instant replay
```
- Automatic recording and replay
- No cassette management
- Works with httpx and requests

**All Others**: Manual VCR.py ❌
- Separate library setup
- Manual cassette naming
- Parallel test conflicts

### 6. Parallelization & Dependencies

**Booktest**: Strong ✅
```python
booktest test -p8  # Use all 8 cores

# Automatic dependency resolution
@bt.depends_on(data=bt.resource("training_data"))
def test_model(t, data):
    # Data loaded once, shared intelligently
```

**promptfoo**: Limited ❌
- Parallel evals but no dependencies
- Not a pipeline manager

**pytest-xdist**: Fair ⚠️
- Parallel tests
- No smart dependency sharing
- Complex resource setup

### 7. Data Science Ergonomics

**Booktest**: Purpose-Built ✅
```python
# Dataframes as markdown tables
t.tdf(predictions_df)

# Metrics with units
t.tmetric(latency, tolerance=5, unit="ms")

# Sample outputs with checks
t.iln(" ✓ Correct prediction")
t.iln(" ✗ Wrong prediction (expected X)")
```

**Jupyter**: Manual ❌
- Great for exploration
- Terrible for regression testing
- No automation

**Generic pytest**: Poor ❌
- Built for traditional software
- No dataframe support
- No metric tracking

---

## Detailed Comparison Table

[Insert full comparison table from .ai/material/comparison-table.md here]

**Key Dimensions**:
1. Review-driven development support
2. Review ergonomics (human-readable outputs)
3. Intermediate caching & iteration speed
4. Regression testing capabilities
5. Snapshotting of external resources
6. Parallelization & dependency resolution
7. Multi-purpose for DS/AI workflows

**Tools Compared**:
- Booktest (baseline)
- PromptFoo (LLM-focused)
- Syrupy/pytest-snapshot (generic snapshots)
- ApprovalTests (manual approval)
- VCR.py (HTTP cassettes)
- DVC (artifact versioning)
- MLflow (experiment tracking)
- Great Expectations (data validation)
- Deepchecks (ML validation)
- OpenAI Evals (LLM benchmarking)
- DeepEval (LLM testing)
- UpTrain (LLMOps)
- LangSmith (LangChain ecosystem)
- Guardrails (LLM validation)

---

## Migration Guides

### From Jupyter + pytest

**Pain points you're feeling:**
- Duplicate code in notebooks and test files
- Manual review doesn't scale
- No snapshot/regression workflow
- Expensive operations kill productivity

**Migration path:**
1. Keep Jupyter for exploration
2. Move regression tests to booktest
3. Use `t.cache()` for expensive operations
4. Review outputs like code with Git

**Example transformation:**

**Before (Jupyter + pytest):**
```python
# In notebook: manual verification
predictions = model.predict(test_data)
display(predictions)  # Manual review every time

# In test file: duplicate code
def test_predictions():
    predictions = model.predict(test_data)  # Re-computed
    assert accuracy > 0.80  # Binary pass/fail
```

**After (Booktest):**
```python
def test_predictions(t: bt.TestCaseRun):
    # Computed once, cached forever
    predictions = t.cache(lambda: model.predict(test_data))

    # Snapshot for review
    t.h1("Predictions")
    t.tdf(predictions)

    # Track metrics with tolerance
    accuracy = calculate_accuracy(predictions)
    t.tmetric(accuracy, tolerance=0.05)  # Track trend

    # Hard threshold
    t.assertln("Accuracy ≥ 80%", accuracy >= 0.80)
```

[See full migration guide →](migrations/from-jupyter-pytest.md)

### From promptfoo

**Why consider booktest:**
- Need broader data science workflows (not just LLM)
- Want caching and parallelization for expensive ops
- Testing data pipelines, not just prompts
- Need tolerance metrics for ML models

**What you'll gain:**
- Smart caching (7hr → 45min)
- Dataframe snapshotting
- Metric tracking with tolerance
- Broader testing capabilities

**What you'll miss:**
- Web UI (but Git diff is often better)
- Some promptfoo-specific features

[See full comparison →](#booktest-vs-promptfoo)

---

## Bottom Line

**Choose Booktest if:**
- Testing has the three pain points (Good vs Bad, Regression Whack-a-Mole, Expensive Operations)
- You're doing data science, not just traditional software
- You need tests that are maintainable, not just functional

**Booktest is the first tool built for data science testing realities.**
```

**Source Material**:
- Use comparison table from `.ai/material/comparison-table.md` for detailed feature-by-feature analysis
- Use `.ai/material/booktest-comparison-summary.md` for:
  - Positioning Booktest as the "review/UX hub" that complements other tools
  - Emphasizing DVC integration and minimal Git footprint
  - Showing how to pair Booktest with Deepchecks/GE/Pandera for metrics
  - Integrating VCR.py/pytest-vcr for cassette replay
  - When to use PromptFoo/LangSmith/UpTrain for LLM-specific dashboards
- Emphasize the three pain points in each comparison
- Show code examples demonstrating differences
- Focus on "when to use what" rather than "why we're better"
- Position Booktest as complementary to specialized tools (not competitive)

---

## Phase 4: Visual Assets (Medium Priority)

### Task 4.1: Create demo GIF/video
**Goal**: Show booktest workflow in 30 seconds

**Script**:
1. Write test with `test_gpt.py`
2. Run `booktest test` - shows DIFF
3. View markdown output in books/
4. Git diff shows changes
5. Accept changes with -u flag

**Tools**: asciinema, terminalizer, or OBS

### Task 4.2: Create comparison diagrams
**Content**:
- Workflow comparison: booktest vs jupyter+pytest
- Architecture diagram: booktest components
- Feature matrix visualization

### Task 4.3: Screenshot gallery
**Content**:
- Test output examples
- LLM review in action
- Metric tracking dashboard
- Git diff of results

---

## Phase 5: Show HN Post (High Priority)

### Task 5.1: Draft Show HN post
**File**: `.ai/show-hn-draft.md`

**Template**:
```markdown
# Show HN: Booktest – Review-driven testing for data science

Hi HN! After years of frustration testing ML/LLM applications, I built Booktest.

Data science testing has three fundamental problems that traditional tools can't solve:

## 1. The Good vs Bad Problem

In traditional software: `assert result == "Paris"` ✅

In data science: Is "Paris" better than "The capital of France is Paris,
which is located in northern France and serves as the economic and cultural
center of the country"?

**There's no correct answer.** You need expert review, statistical thresholds,
human judgment. assertEqual() doesn't work. Manual review doesn't scale.

Booktest solution: Let AI review AI outputs, track metrics with tolerance.

```python
# GPT evaluates GPT automatically
r.reviewln("Is response accurate?", "Yes", "No")

# Track with ±5% tolerance - catch regressions, not noise
t.tmetric(accuracy, tolerance=0.05)  # 85% ± 5% = OK
```

## 2. The Regression Whack-a-Mole

Change one prompt → 47 tests fail.
Update training data → model behaves differently everywhere.
Tweak hyperparameters → metrics shift across the board.

Traditional testing: ❌ Binary pass/fail, ❌ No visibility into changes

Booktest treats test outputs like code:
- Git-track everything as markdown
- Review changes with `git diff`
- Accept good changes, reject bad ones

```python
t.tdf(predictions)  # Snapshot dataframe as markdown
# Later: git diff shows exactly what changed
booktest test -u    # Accept improvements
```

## 3. The Expensive Operations Problem

Reality: 100 prompts × 5 models × 10 cases = 5,000 tests × 5 sec = **7 hours**

Jupyter + pytest: No caching, poor parallelization, duplicate code

Booktest solution:

```python
# Smart caching - computed once, cached forever
predictions = t.cache(lambda: expensive_inference())

# Parallel execution
booktest test -p8  # Use all 8 cores

# Automatic mocking
@bt.snapshot_httpx()  # Record once, replay forever
def test_gpt(t):
    response = openai.chat(...)  # Instant in future runs
```

**Result: 7 hours → 45 minutes**

---

## What's New in 1.0

Just released tolerance-based metrics that make tests maintainable:
- Catch real regressions (10% drop)
- Ignore natural variation (±2%)
- Reduce false alarms by 90%

Plus DVC integration for large snapshot storage outside Git.

## Try It

```bash
pip install booktest
booktest --setup
booktest test
```

Docs: https://github.com/lumoa-oss/booktest

Built this because nothing else solved all three problems. Would love feedback
from fellow data scientists/ML engineers dealing with these pain points!

---

**Why not promptfoo/langsmith?** LLM-only, missing data science workflows
**Why not pytest-regtest/syrupy?** No LLM evaluation, no tolerance metrics
**Why not Jupyter?** Great for exploration, terrible for regression testing

Booktest is the first tool that gets data science testing right.
```

**Success Metrics**:
- [ ] Clear, relatable problem statement
- [ ] Compelling solution with code example
- [ ] Differentiation from existing tools
- [ ] Call to action
- [ ] Under 300 words (HN attention span)

### Task 5.2: Prepare for HN traffic
**Checklist**:
- [ ] README.md polished and compelling
- [ ] Getting started guide tested by outsiders
- [ ] Example tests in repo work out-of-box
- [ ] Issues template set up for bug reports
- [ ] Contributing guide for potential contributors
- [ ] Performance: docs load fast, examples run quick
- [ ] Monitoring: Track GitHub stars, pip downloads

---

## Phase 6: Social Proof (Low Priority, High Impact)

### Task 6.1: Collect testimonials
**Sources**:
- Internal Lumoa usage
- Early adopters
- Beta testers

**Format**:
> "Quote about specific problem booktest solved"
> — Name, Title, Company

### Task 6.2: Create case studies
**Structure** (1-2 pages each):
1. Company/team background
2. Problem they faced
3. How they use booktest
4. Results (time saved, bugs caught, etc)
5. Key quote

**Target**: 2-3 case studies before Show HN launch

### Task 6.3: Build community presence
**Actions**:
- [ ] Post examples on Twitter/X
- [ ] Share use cases on r/MachineLearning
- [ ] Answer questions on StackOverflow
- [ ] Write blog posts about patterns

---

## Phase 7: Polish & Refinement (Medium Priority)

### Task 7.1: Improve code examples in docs
**Audit**:
- [ ] All examples run without errors
- [ ] Examples show real-world patterns
- [ ] Examples are copy-pasteable
- [ ] Examples build on each other
- [ ] Examples cover edge cases

### Task 7.2: Add troubleshooting guide
**File**: `docs/troubleshooting.md`

**Content**:
- Common errors and solutions
- Performance optimization tips
- Debugging techniques
- FAQ

### Task 7.3: Create migration guides
**Files**:
- `docs/migrations/from-pytest.md`
- `docs/migrations/from-jupyter.md`
- `docs/migrations/from-promptfoo.md`

**Content**: Step-by-step conversion process

### Task 7.4: Improve API documentation
**Goal**: Every public method documented with examples

**Audit**:
- [ ] OutputWriter methods
- [ ] TestCaseRun methods
- [ ] LlmReview methods
- [ ] Decorator functions
- [ ] Configuration options

---

## Phase 8: Launch Preparation (High Priority)

### Task 8.1: Pre-launch checklist
**Timeline**: 1 week before Show HN

- [ ] README.md finalized and reviewed
- [ ] Getting started guide tested with 3+ outsiders
- [ ] Show HN post drafted and reviewed
- [ ] Demo video/GIF created
- [ ] GitHub issues/discussions enabled
- [ ] Contributing guide published
- [ ] Code of conduct added
- [ ] License clearly stated (MIT)
- [ ] Changelog up to date
- [ ] Version 1.0.0 tagged
- [ ] PyPI package published
- [ ] Website/docs deployed (if applicable)

### Task 8.2: Launch day preparation
**Actions**:
- [ ] Schedule Show HN post for optimal time (Tuesday-Thursday, 9-11am PT)
- [ ] Monitor comments for first 2 hours
- [ ] Have team ready to answer questions
- [ ] Track metrics (stars, downloads, issues)
- [ ] Prepare follow-up blog post
- [ ] Thank commenters and contributors

### Task 8.3: Post-launch plan
**First Week**:
- [ ] Respond to all GitHub issues within 24h
- [ ] Fix critical bugs immediately
- [ ] Collect feedback for v1.1
- [ ] Write blog post: "What we learned from Show HN"
- [ ] Share success stories on social media

**First Month**:
- [ ] Implement top feature requests
- [ ] Publish case studies
- [ ] Build community presence
- [ ] Plan v1.1 roadmap

---

## Success Metrics

### Quantitative
- **GitHub Stars**: Target 500+ in first week
- **PyPI Downloads**: Target 1000+ in first month
- **GitHub Issues**: <5 critical bugs in first week
- **Response Time**: <24h for all issues
- **Documentation Clarity**: 0 "how do I get started" questions

### Qualitative
- Positive sentiment on HN (70%+ of comments)
- Users able to run first test in <5 minutes
- Clear differentiation from competitors understood
- Community members contributing examples/docs

---

## Priority Matrix

| Phase | Priority | Estimated Effort | Impact |
|-------|----------|------------------|--------|
| Phase 1: Front Page & README | 🔴 HIGH | 2-3 days | 🔥 CRITICAL |
| Phase 2: Getting Started | 🔴 HIGH | 1-2 days | 🔥 CRITICAL |
| Phase 3: 1.0 Maintainability | 🔴 HIGH | 1 day | 🔥 CRITICAL |
| Phase 5: Show HN Post | 🔴 HIGH | 1 day | 🔥 CRITICAL |
| Phase 8: Launch Prep | 🔴 HIGH | 2-3 days | 🔥 CRITICAL |
| Phase 4: Use Cases | 🟡 MEDIUM | 3-4 days | 📈 HIGH |
| Phase 6: Visual Assets | 🟡 MEDIUM | 2-3 days | 📈 HIGH |
| Phase 7: Polish | 🟡 MEDIUM | 2-3 days | 📈 MEDIUM |
| Phase 9: Social Proof | 🟢 LOW | Ongoing | 📈 HIGH |

**Critical Path** (Minimum Viable Launch):
1. Phase 1 → 2 → 3 → 5 → 8 = ~1.5 weeks of focused work
2. Phases 4, 6, 7, 9 can happen in parallel or post-launch

**Key Messages to Nail**:
1. **Three Pain Points**: Good vs Bad, Regression Whack-a-Mole, Expensive Operations
2. **1.0 Value**: Maintainability (AI reviews, tolerance metrics, DVC, reviewability)
3. **Differentiation**: First tool that solves all three + makes tests sustainable

---

## Timeline Recommendation

### Week 1: Foundation
- Days 1-2: Rewrite README.md (Phase 1)
- Days 3-4: Revamp getting-started.md (Phase 2)
- Day 5: Create QUICKSTART.md, demo GIF (Phases 2, 4)

### Week 2: Launch Materials
- Days 1-2: Create use case docs (Phase 3)
- Day 3: Draft Show HN post (Phase 5)
- Days 4-5: Pre-launch checklist (Phase 8)

### Week 3: Polish & Launch
- Days 1-2: Final polish, external review
- Day 3: Launch preparation
- Day 4: **SHOW HN POST** 🚀
- Day 5: Monitor and respond

---

## Messaging Cheat Sheet

**Use these talking points consistently across all documentation:**

### The Three Pain Points (The Hook)

**1. Good vs Bad Problem**
- "assertEqual() doesn't work when there's no correct answer"
- "Is 'Paris' better than a full sentence? You need expert judgment"
- "Manual review doesn't scale to 1000 test cases"

**2. Regression Whack-a-Mole**
- "Change one prompt, break 47 tests"
- "Binary pass/fail hides what actually changed"
- "You can't fix what you can't see"

**3. Expensive Operations**
- "5,000 tests × 5 seconds = 7 hours of waiting"
- "No caching = recomputing everything every time"
- "Poor parallelization = wasted CPU cores"

### The Solution (The Value Prop)

**Review-Driven Testing**
- "Treat test outputs like code"
- "Review changes, don't just pass/fail"
- "Git diff shows exactly what changed"

**Core Innovation**
- "Snapshot everything as markdown"
- "AI evaluates AI outputs automatically"
- "Tolerance metrics catch real regressions, ignore noise"

### The 1.0 Pitch (What's New)

**Maintainability Crisis Solved**
- "AI as north star replaces expensive expert review"
- "Tolerance metrics reduce false alarms by 90%"
- "DVC handles large snapshots outside Git"
- "Tests that were too fragile are now stable"

### Differentiation (Why Not X?)

**vs Jupyter + pytest**
- "No duplicate code, built-in LLM evaluation, smart caching"

**vs promptfoo/langsmith**
- "Full data science workflows, not just LLM evaluation"

**vs syrupy/pytest-regtest**
- "LLM evaluation, tolerance metrics, data science ergonomics"

### Sound Bites (For Social Media)

- "Stop pretending assertEqual() works for 'Is this good enough?'"
- "Change one prompt, break 47 tests. We've all been there."
- "7 hours → 45 minutes. Same test suite."
- "Git diff for test outputs. Finally."
- "Let AI review AI. It's 2024."

### Anti-Patterns to Avoid

**Don't say:**
- ❌ "Yet another testing framework"
- ❌ "Better pytest" (we're fundamentally different)
- ❌ "Snapshot testing library" (undersells the full value)

**Do say:**
- ✅ "First tool built for data science testing realities"
- ✅ "Review-driven testing framework"
- ✅ "Testing for when there's no correct answer"

---

## Next Steps

1. **Review this plan** - Adjust priorities based on team capacity
2. **Assign tasks** - Who owns what?
3. **Set deadlines** - When do we launch?
4. **Start with README** - Biggest impact, sets tone for everything
5. **Get external feedback early** - Test messaging with potential users
6. **Practice the pitch** - Make sure the three pain points resonate

**Recommended Launch Date**: 2-3 weeks from now
**Critical Path Owner**: [Assign]
**Launch Day Coordinator**: [Assign]

**Pre-Flight Checklist**:
- [ ] Can explain each pain point in <30 seconds
- [ ] README hooks reader in first paragraph
- [ ] Show HN post tested with 3+ data scientists
- [ ] Demo GIF shows "aha!" moment clearly
- [ ] All code examples are copy-pasteable and tested
