# CI/CD Integration Guide

This guide shows how to integrate booktest into your CI/CD pipeline.

## GitHub Actions

Create `.github/workflows/booktest.yml` in your repository:

```yaml
name: Booktest

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install booktest
          # If you have a requirements.txt or pyproject.toml:
          # pip install -r requirements.txt
          # or: pip install -e .

      - name: Run booktest
        run: booktest -c  # Continue on failure to see all results

      - name: Upload test books on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-books
          path: books/
          retention-days: 7
```

### With Poetry

If your project uses Poetry:

```yaml
name: Booktest

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: poetry install

      - name: Run booktest
        run: poetry run booktest -c

      - name: Upload test books on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-books
          path: books/
```

### With AI Review

If you want AI-assisted review in CI (requires API key):

```yaml
name: Booktest with AI Review

on:
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install booktest anthropic  # or: pip install booktest openai

      - name: Run booktest with AI review
        env:
          # Use Claude for AI reviews
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          # Or use OpenAI:
          # OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          # OPENAI_API_BASE: ${{ secrets.OPENAI_API_BASE }}
        run: booktest -R -c  # -R enables AI review

      - name: Upload test books on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-books
          path: books/
```

### Parallel Execution

For faster CI with parallel test execution:

```yaml
      - name: Run booktest in parallel
        run: booktest -p4 -c  # Run on 4 cores
```

## GitLab CI

Create `.gitlab-ci.yml` in your repository:

```yaml
stages:
  - test

booktest:
  stage: test
  image: python:3.11
  script:
    - pip install booktest
    - booktest -c
  artifacts:
    when: on_failure
    paths:
      - books/
    expire_in: 1 week
```

### With AI Review (GitLab)

```yaml
booktest:
  stage: test
  image: python:3.11
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY  # Set in GitLab CI/CD Variables
  script:
    - pip install booktest anthropic
    - booktest -R -c
  artifacts:
    when: on_failure
    paths:
      - books/
```

## CircleCI

Create `.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: pip install booktest
      - run:
          name: Run booktest
          command: booktest -c
      - store_artifacts:
          path: books/
          destination: test-books
          when: on_fail

workflows:
  test:
    jobs:
      - test
```

## Best Practices

### 1. Commit your `books/` directory

Booktest stores test output as markdown in `books/`. Commit this directory to track test evolution:

```bash
git add books/
git commit -m "Update test snapshots"
```

### 2. Review snapshot changes in PRs

When tests produce different output, the `books/` directory will show changes in the PR diff. Review these changes like code.

### 3. Use `-c` flag in CI

The `-c` (continue) flag ensures all tests run even if some fail, giving you a complete picture of the test suite status.

### 4. Upload artifacts on failure

Always upload the `books/` directory as an artifact when tests fail. This helps debug failures by showing the actual vs expected output.

### 5. Use parallel execution for speed

Use `-p N` to run tests on N cores. Start with `-p4` and adjust based on your CI runner.

### 6. Consider AI review for complex changes

The `-R` flag enables AI-assisted diff review, which can help triage large changesets. Only use this if you have an API key configured.

## Environment Variables

| Variable | Provider | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic | Claude API key for AI review |
| `ANTHROPIC_MODEL` | Anthropic | Model to use (default: claude-sonnet-4-20250514) |
| `OPENAI_API_KEY` | OpenAI/Azure | OpenAI API key for AI review |
| `OPENAI_API_BASE` | Azure | Azure OpenAI endpoint |
| `OPENAI_MODEL` | OpenAI/Azure | Model to use |
| `OLLAMA_HOST` | Ollama | Ollama server URL (default: http://localhost:11434) |
| `OLLAMA_MODEL` | Ollama | Model to use (default: llama3.2) |
