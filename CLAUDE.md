# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Booktest is a review-driven testing tool that combines Jupyter notebook style data science development with traditional regression testing. It performs snapshot testing for data science applications where results are not strictly right/wrong but require expert review.

## Common Development Commands

### Testing
```bash
# Run all tests using booktest's own test framework
./do test

# Run tests with specific options
./do test -p  # Print output
./do test -f  # Fail fast on first error
./do test -c  # Continue on failure
./do test -r  # Review mode - shows diffs for snapshot changes
./do test -u  # Update snapshots to current results

# Run tests using Poetry
poetry run booktest test

# Run a single test or test group
./do test <test_name>
```

### Code Quality
```bash
# Run linter (pycodestyle)
./do lint

# Run coverage analysis
./do coverage

# Run quality assurance (lint + tests)
./do qa
```

### Development Setup
```bash
# Enter Poetry shell environment
poetry shell

# Install dependencies
poetry install
```

## Architecture Overview

### Core Components

**TestCaseRun** (`booktest/testcaserun.py`): The main API for writing tests. Provides methods for:
- Printing results to markdown files with `h1()`, `h2()`, `md()`, `code()`
- Managing test state and caching with `cache()` and `cache_fs()`
- Snapshotting HTTP requests, functions, and environment variables
- Comparing results against stored snapshots

**TestBook** (`booktest/testbook.py`): Base class for test suite objects that groups related tests together.

**TestSuite** (`booktest/testsuite.py`): Base class for organizing multiple test books into suites.

**Tests** (`booktest/tests.py`): Manages CLI interface and test execution, including:
- Test discovery and selection
- Parallel execution management
- Review mode for approving snapshot changes
- Result reporting

### Key Features

**Two-Level Caching**:
- Memory cache for fast repeated runs
- Filesystem cache for persistence between sessions

**Dependency Management** (`booktest/dependencies.py`):
- `@depends_on` decorator for test dependencies
- Resource pools for managing shared resources like ports
- Support for async dependencies

**Snapshot Testing**:
- `snapshot_requests()`: Mock HTTP requests and store responses
- `snapshot_httpx()`: Mock httpx async requests
- `snapshot_functions()`: Mock function calls
- `snapshot_env()`: Mock environment variables

### Test Organization

Tests are organized in the `test/` directory and detected automatically using naming conventions:
- Test files must end with `_test.py`
- Test functions must start with `test_`
- Test classes inherit from `TestBook` or `TestSuite`

Results are stored as markdown files in the `books/` directory, allowing Git tracking of test output evolution.

## Important Patterns

### Writing Tests
```python
import booktest as bt

class MyTests(bt.TestBook):
    def test_example(self, r: bt.TestCaseRun):
        r.h1("Test Title")
        result = r.cache(lambda: expensive_computation())
        r.code(result, lang="json")
```

### Using Dependencies
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

## File Structure

- `booktest/`: Main library code
- `test/`: Test files using booktest
- `books/`: Generated test output (markdown files)
- `examples/`: Example projects demonstrating booktest usage
- `do.py`: Main development script for running tests and tools
- `pyproject.toml`: Poetry configuration and dependencies