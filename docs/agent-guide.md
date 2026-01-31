# Agent Guide - Booktest Architecture

This guide is for coding agents (Claude Code, Copilot, etc.) working on the booktest codebase.

## Project Overview

Booktest is a review-driven testing tool for data science. It performs snapshot testing where results are not strictly right/wrong but require expert review. Test outputs are captured as markdown, tracked in Git, and reviewed like code diffs.

## Architecture

### Core Components

**TestCaseRun** (`booktest/core/testcaserun.py`): The main API for writing tests. Provides methods for:
- Printing results to markdown files: `h1()`, `h2()`, `md()`, `code()`
- Managing test state and caching: `cache()`, `cache_fs()`
- Snapshotting HTTP requests, functions, and environment variables
- Tolerance metrics: `tmetric()`, `assertln()`
- AI-assisted review: `start_review()`

**TestBook** (`booktest/testbook.py`): Base class for test suite objects that groups related tests.

**TestSuite** (`booktest/testsuite.py`): Organizes multiple test books into suites.

**Tests** (`booktest/tests.py`): CLI interface and test execution:
- Test discovery and selection
- Parallel execution management
- Review mode for approving snapshot changes
- Result reporting

### LLM Integration (`booktest/llm/`)

**llm.py**: Abstract LLM interface with implementations:
- `GptLlm` — Azure OpenAI (default fallback)
- `ClaudeLlm` — Anthropic Claude
- `OllamaLlm` — Local models via Ollama
- Auto-detection via `get_llm()` based on environment variables

**llm_review.py**: LLM-assisted review:
- `reviewln()` — Assert LLM answer matches expected
- `ireviewln()` — Record LLM answer without assertion
- `treviewln()` — Record answer in tested output (snapshot)
- `review_test_diff()` — AI-powered review of test diffs

### Dependency System (`booktest/dependencies.py`)

- `@depends_on` decorator for test dependencies
- Tests return objects (like Make targets), other tests consume them
- Resource pools for shared resources (ports, connections)
- Parallel scheduling respects dependency graph

### Snapshot System

- `snapshot_requests()` / `snapshot_httpx()`: Mock and record HTTP calls
- `snapshot_functions()`: Mock function calls
- `snapshot_env()`: Mock environment variables
- Snapshots stored in `books/` (Git) or DVC for large files

### Test Organization

Tests in `test/` are detected automatically:
- Files ending with `_test.py`
- Functions starting with `test_`
- Classes inheriting from `TestBook` or `TestSuite`

Results stored as markdown in `books/`, tracked in Git.

## Key Patterns

### Writing Tests
```python
import booktest as bt

class MyTests(bt.TestBook):
    def test_example(self, r: bt.TestCaseRun):
        r.h1("Test Title")
        result = r.cache(lambda: expensive_computation())
        r.code(result, lang="json")
```

### Dependencies
```python
@bt.depends_on(port=bt.port())
def test_with_port(r: bt.TestCaseRun, port):
    r.md(f"Using port: {port}")
```

### Snapshot Testing
```python
def test_api(r: bt.TestCaseRun):
    with bt.snapshot_requests(r):
        response = requests.get("http://api.example.com/data")
        r.code(response.json())
```

### LLM Review
```python
def test_output(t: bt.TestCaseRun):
    r = t.start_review()
    r.iln(some_output)
    r.reviewln("Is output correct?", "Yes", "No")
```

## Environment Variables

### Azure OpenAI
| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | API key |
| `OPENAI_API_BASE` | Azure endpoint URL |
| `OPENAI_DEPLOYMENT` | Deployment name (default: gpt35turbo) |
| `OPENAI_MODEL` | Model name |
| `OPENAI_API_VERSION` | API version |

### Anthropic
| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key (triggers auto-detection) |
| `ANTHROPIC_MODEL` | Model (default: claude-sonnet-4-20250514) |

### Ollama
| Variable | Purpose |
|----------|---------|
| `OLLAMA_HOST` | Server URL (default: localhost:11434) |
| `OLLAMA_MODEL` | Model (default: llama3.2) |
