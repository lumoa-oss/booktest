# Contributing to Booktest

Thanks for your interest in contributing to Booktest! This document provides guidelines for contributing.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lumoa-oss/booktest.git
   cd booktest
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   pip install poetry
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

## Running Tests

```bash
# Run all tests
./do test

# Run with verbose output
./do test -v

# Run specific test file
./do test test/examples/hello_book.py

# Run with coverage
./do coverage
```

## Code Style

We use `pycodestyle` for linting:

```bash
./do lint
```

Key guidelines:
- Follow PEP 8
- Keep lines under 80 characters where practical
- Use descriptive variable names
- Add docstrings for public functions and classes

## Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write tests for new functionality
   - Update documentation if needed
   - Run `./do lint` and `./do test`

3. **Commit with clear messages**
   ```bash
   git commit -m "Add feature X that does Y"
   ```

4. **Push and create a PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Guidelines

- Describe what your PR does and why
- Link any related issues
- Ensure tests pass
- Keep PRs focused - one feature or fix per PR

## Reporting Issues

When reporting bugs, please include:
- Booktest version (`pip show booktest`)
- Python version
- Operating system
- Minimal reproduction steps
- Expected vs actual behavior

## Questions?

- Open a [Discussion](https://github.com/lumoa-oss/booktest/discussions) for questions
- Check existing [Issues](https://github.com/lumoa-oss/booktest/issues) before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
