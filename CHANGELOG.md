# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-30

### Added
- **Multi-LLM Support**: Added `ClaudeLlm` and `OllamaLlm` classes alongside existing `GptLlm`
- **Auto-detection**: `get_llm()` automatically selects provider based on environment variables
- **`set_llm_factory()`**: Configure which LLM type to use without immediate instantiation
- **`prompt_json()`**: New method for JSON responses with validation and automatic retry
- **Enhanced `booktest -l`**: Colorful test status display with durations (green ok, yellow DIFF, red FAIL)
- **Demo GIF**: Added animated demo to README for visual first impression
- **Use case gallery**: New `docs/use-cases.md` with problem-oriented recipes
- **CI/CD guide**: New `docs/ci-cd.md` with GitHub Actions, GitLab CI, CircleCI examples

### Changed
- `snapshot_env` now resets LLM cache to ensure correct environment variables after restore
- Improved `reviewln()` to use `prompt_json()` for more reliable JSON parsing
- Test duration display now uses human-readable format (ms, s, min)

### Fixed
- LLM client caching issue where environment variable changes weren't respected
- JSON parsing reliability in LLM review responses

## [1.0.14] - 2026-01-27

### Fixed
- Bug in `llm_review` where `t()` method and internal output field name collided

## [1.0.13] and earlier

See [GitHub releases](https://github.com/lumoa-oss/booktest/releases) for earlier versions.
