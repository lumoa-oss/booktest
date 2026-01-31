# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

See [docs/agent-guide.md](docs/agent-guide.md) for architecture details and code patterns.

## Commands

```bash
# Development setup
uv sync                    # Install/sync dependencies

# Testing (booktest tests itself)
./do test                  # Run all tests
./do test -p               # Print output
./do test -f               # Fail fast
./do test -c               # Continue on failure
./do test -r               # Review mode (shows diffs)
./do test -u               # Update snapshots
./do test <test_name>      # Run specific test

# Code quality
./do lint                  # Linter (pycodestyle)
./do coverage              # Coverage analysis
./do qa                    # Lint + tests

# Project version
./do version               # Print current version
./do version X.Y.Z         # Set version
```

## File Structure

- `booktest/` - Library code
- `test/` - Tests (booktest tests itself)
- `books/` - Generated test output (markdown snapshots tracked in Git)
- `do.py` - Development script
- `pyproject.toml` - Project configuration (PEP 621, hatchling build)
