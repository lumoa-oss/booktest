# ADR-005: Early User Experience and CLI Flag Discoverability

## Status
Proposed

## Context

Booktest has two fundamentally different usage workflows:

1. **Testing workflow** (CI/CD, regression validation)
   - Run tests silently, fail on regressions
   - Goal: Automated validation, pass/fail determination
   - Default behavior: `booktest` → runs tests, returns exit code

2. **Interactive R&D workflow** (development, exploration)
   - Review outputs, debug failures, iterate on logic
   - Goal: Interactive development, understanding behavior
   - Required flags: `-v -i` (verbose + interactive)
   - For reviewing failures: `-v -i -c -w` (verbose + interactive + continue + review)

**The problem**: Booktest's default behavior optimizes for the testing workflow, but new users typically start with the interactive R&D workflow. This creates significant friction.

### The "WTF" Moments

When a new user follows the Quick Start guide and runs `booktest`:

```bash
# User's first experience
$ booktest
# [Tests run... some fail silently]
# Exit code: 1

# User: "What happened? Where are the results?"
```

**Confusion points identified**:

1. **Silent execution**: No output unless `-v` (verbose) is provided
   - Tests run but user sees nothing
   - Failures happen but no indication of what failed or why
   - Counter-intuitive: "I ran tests, show me the results!"

2. **Non-interactive by default**: Tests run and exit immediately
   - No chance to review failures
   - No prompt to accept/reject changes
   - User must know to add `-i` flag

3. **Flag discovery is hard**: Users need to run `booktest --help` and parse 30+ flags
   - Unix-style composable flags (good for experts, intimidating for beginners)
   - No contextual hints about common workflows
   - Documentation uses flags like `-v -i -c -w` without explanation

4. **Review mode is hidden**: `-w` (or `--review`) is not obvious
   - After tests fail, users don't know how to review failures
   - Must run again with different flags to see what broke

5. **Two-step workflow isn't obvious**:
   - Step 1: Run tests (`booktest -v -i`)
   - Step 2: Review failures (`booktest -w` or re-run with `-v -i -c -w`)
   - Users expect one command

### Flag System Deep Dive

Booktest uses Unix-style single-letter flags that compose:sh

**Execution control**:
- `-v`: Verbose (show test output)
- `-i`: Interactive (pause on failures)
- `-I`: Always interactive (pause even on success)
- `-c`: Continue (don't stop on first failure, skip successful tests)
- `-f`: Fail fast (stop on first error)

**Update control**:
- `-u`: Update on success (auto-accept passing tests)
- `-a`: Accept all (auto-accept even differing tests)
- `-r`: Refresh (re-run test dependencies)
- `-s`: Complete snapshots (capture missing snapshots)
- `-S`: Refresh snapshots (discard old, capture new)

**Review workflow**:
- `-w` / `--review`: Review previous run's failures

**Other**:
- `-p`, `-p2`, `-p4`, `-p8`: Parallel execution
- `-l`: List tests
- `--view`: View test outputs in markdown viewer

**Common combinations**:
- `booktest -v -i`: Interactive development (see output, pause on failures)
- `booktest -v -i -c -w`: Review all failures interactively
- `booktest -u`: CI mode (auto-accept passing tests)
- `booktest -u -c`: CI mode with full run (don't stop on first failure)
- `booktest -p8`: Parallel testing (8 workers)

### Real-World User Journeys

**Journey 1: First-time user (from README Quick Start)**
```bash
# Step 1: User writes first test
$ cat > test/test_hello.py << EOF
import booktest as bt
def test_hello(t: bt.TestCaseRun):
    t.h1("My First Test")
    t.tln("Hello, World!")
EOF

# Step 2: User runs it (following README advice)
$ booktest -v -i
# Output appears! Test passes! Interactive prompt asks to accept.
# ✅ Good experience

# BUT: If they run without flags (natural first instinct)
$ booktest
# [Silent execution, exit code 0]
# User: "Did anything happen?" ❌ Confusing
```

**Journey 2: User with failing tests**
```bash
# User makes a change that breaks tests
$ booktest
# [Some tests fail, exit code 1]
# User: "What failed? Why?" ❌

# User tries verbose
$ booktest -v
# [Shows output, but exits on first failure]
# User: "I want to see ALL failures" ❌

# User discovers continue flag
$ booktest -v -c
# [Shows all failures, exits]
# User: "How do I review and accept/reject changes?" ❌

# User discovers interactive + continue
$ booktest -v -i -c
# [Interactive review of each failure]
# ✅ Finally works, but took 4 attempts

# Alternative: User discovers review mode
$ booktest -w
# [Reviews previous failures]
# ✅ This also works, but non-obvious
```

**Journey 3: User in R&D iteration loop**
```bash
# User is developing a new model evaluation pipeline
# They want to:
# 1. Run tests verbosely (see outputs)
# 2. Continue on failures (see all issues)
# 3. Review each failure interactively
# 4. Iterate quickly

# They need: booktest -v -i -c -w
# But discover this through trial and error
```

**Journey 4: User setting up CI**
```bash
# Real-world CI pattern (from production usage - before auto-report):
booktest -p8 || booktest -v -L -w -c

# This means:
# 1. Run tests in parallel with 8 workers (-p8)
# 2. If that fails, re-run with detailed review mode:
#    -v: Show verbose output
#    -L: Show debug logs
#    -w: Review mode (show failures from previous run)
#    -c: Continue through all failures

# Problem: The fallback re-runs tests unnecessarily
# Problem: Users must know the `-v -L -w -c` spell
```

**With auto-report, CI becomes much simpler**: Just `booktest -p8` is enough. The failure report prints automatically without re-running tests.

### Comparison to Other Tools

**pytest**:
```bash
$ pytest              # Verbose by default, shows failures
$ pytest -v           # More verbose
$ pytest --pdb        # Interactive debugging
```
- Default is verbose
- Clear `-v` means "more verbose"
- Interactive debugging is explicit (`--pdb`)

**jest**:
```bash
$ jest                # Shows results by default
$ jest --watch        # Interactive mode
$ jest --updateSnapshot  # Update snapshots
```
- Default shows results
- Interactive mode is explicit
- Snapshot updates are explicit

**cargo test**:
```bash
$ cargo test          # Shows results by default
$ cargo test -- --show-output  # Show test output
```
- Default shows results

**Booktest**:
```bash
$ booktest            # Silent by default ❌
$ booktest -v         # Verbose
$ booktest -v -i      # Verbose + interactive
```
- Default is silent (optimized for CI, not humans)
- Requires flags for basic visibility

## Decision

We will improve the early user experience through a combination of changes:

### 1. Auto-Print Failure Report on Failure (RECOMMENDED)

**Key insight from real CI usage**: The pattern `booktest -p8 || booktest -v -L -w -c` works well, but users shouldn't need to know the second spell.

**Solution**: Automatically print a detailed failure report when tests fail, eliminating the need for the `-v -L -w -c` spell entirely.

```bash
$ booktest
# [Tests run]
test/test_hello.py::test_hello PASS 123 ms
test/test_model.py::test_evaluation FAIL 2341 ms
test/test_agent.py::test_step1 DIFF 891 ms

2 passed, 1 failed, 1 diff

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

test/test_model.py::test_evaluation FAIL 2341 ms

Expected output:
  Accuracy: 92.3%
  F1 Score: 0.87

Actual output:
  Accuracy: 87.1%  ← Changed (was 92.3%, Δ-5.2%)
  F1 Score: 0.84   ← Changed (was 0.87, Δ-0.03)

Diff:
  - Accuracy: 92.3%
  + Accuracy: 87.1%
  - F1 Score: 0.87
  + F1 Score: 0.84

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

test/test_agent.py::test_step1 DIFF 891 ms

[Full diff shown...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 To review interactively, run: booktest -w
💡 To accept all changes, run: booktest -u -c
💡 To see full output, run: booktest -v
```

**When to print report**:
- Exit code is non-zero (failures or diffs)
- Not running in interactive mode (`-i` not set)
- Can be disabled with `auto_report=false` in config

**Configuration**:
```ini
# .booktest
auto_report=true           # Print failure report on failure (default: true)
```

**Benefit**: Eliminates the need for users to know `-v -L -w -c`. The report is printed automatically when needed, both locally and in CI.

### 2. Contextual Hints in CLI Output

Add helpful tips when tests run without common flags:

```bash
$ booktest -v  # User ran verbose but not interactive
# [Tests run]
test/test_hello.py::test_hello PASS 123 ms
test/test_model.py::test_evaluation FAIL 2341 ms

Tip: Use 'booktest -i' to review failures interactively
     Or run 'booktest -w' to review the failures from this run
```

**When to show tips**:
- Show when exit code is non-zero (failures or diffs)
- Only if auto-report didn't show (i.e., in verbose mode but not interactive)
- User can disable with `tips=false` in config

### 3. Improved Help Output with Workflow Sections

Reorganize `booktest --help` to group flags by workflow, including the real CI pattern:

```bash
$ booktest --help
usage: booktest [-h] [test_cases ...]

booktest - review-driven testing for data science

Common workflows:
  booktest -v -i                      Interactive development (verbose + pause on failures)
  booktest -w                         Review failures from previous run
  booktest -p8                        Parallel testing (auto-report shows failures)
  booktest -u -c                      CI mode (auto-accept changes, continue on failure)

Visibility:
  -v            Show test output (verbose)
  -L            Show debug logs

Interactive control:
  -i            Pause on failures for review
  -I            Pause on every test (even successes)
  -w, --review  Review failures from previous run

Execution control:
  -c            Continue on failure (don't stop at first error)
  -f            Fail fast (stop at first error)
  -r            Refresh test dependencies (ignore cache)

Update control:
  -u            Auto-accept passing tests
  -a            Auto-accept all tests (including diffs)
  -s            Complete missing snapshots
  -S            Refresh all snapshots (discard old)

Parallel execution:
  -p, -p2, -p4, -p8, -p16    Run tests in parallel
  --parallel-count N          Run tests with N workers

Other:
  -l            List test cases
  --view        View test outputs in markdown viewer
  --help        Show this help message

Test selection:
  test_cases    Test file, class, or function to run (default: all tests)
                Examples:
                  booktest test/test_foo.py
                  booktest test/test_foo.py::TestClass
                  booktest test/test_foo.py::TestClass/test_method

For more: https://github.com/lumoa-oss/booktest
```

### 4. Smart Auto-Report Generation

Automatically print detailed failure reports without requiring the `-v -L -w -c` spell:

```python
def print_failure_report_if_needed(config, exit_code, out_dir, exp_dir, cases):
    """
    Automatically print failure report when tests fail.
    Replaces the need for 'booktest -v -L -w -c' fallback.
    """
    # Don't print report if:
    # - All tests passed
    # - Already in interactive mode (user is actively reviewing)
    # - User disabled auto-report
    if exit_code == 0:
        return

    if config.get("interactive"):
        return

    if not config.get("auto_report", True):
        return

    # Print the report (equivalent to -v -L -w -c logic)
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    # Call the review function with non-interactive flag
    review_config = config.copy()
    review_config["verbose"] = True
    review_config["print_logs"] = True
    review_config["interactive"] = False

    review(exp_dir, out_dir, review_config, None, cases)

    # Show helpful tips at the end
    print()
    print("💡 To review interactively, run: booktest -w")
    print("💡 To accept all changes, run: booktest -u -c")
    print("💡 To see full output during test run, use: booktest -v")
```

### 5. Documentation Updates

Update the README and Quick Start guide to:

1. **Lead with the R&D workflow first** (most common entry point)
   ```bash
   # Start here: Interactive development
   booktest -v -i
   ```

2. **Explain flag composition philosophy**
   - Each flag does one thing
   - Combine flags for different workflows
   - Common combinations provided as examples

3. **Create a "Flags Cheat Sheet" section**
   ```markdown
   ## Common Flag Combinations

   **Interactive Development** (most common for new users):
   ```bash
   booktest -v -i        # Verbose + pause on failures
   ```

   **Review Failures**:
   ```bash
   booktest -w           # Review failures from last run
   booktest -v -i -c -w  # Re-run and review all failures
   ```

   **CI/CD**:
   ```bash
   booktest -p8          # Parallel testing (auto-report shows failures)
   booktest -u -c        # Auto-accept changes, continue on failure
   ```

   **Parallel Execution**:
   ```bash
   booktest -p8          # Run with 8 parallel workers
   ```
   ```

4. **Add a "Understanding Exit Codes" section**
   ```markdown
   ## Exit Codes

   - `0`: All tests passed
   - `1`: Test failures (real errors)
   - `255`: Diffs detected (outputs changed but no errors)

   In CI with `-u` flag, exit code 255 is expected (auto-accepting changes).
   Only fail CI on exit code 1.
   ```

### 6. Interactive First-Run Wizard (Future Enhancement)

For first-time users, offer an optional interactive setup:

```bash
$ booktest --setup
Welcome to Booktest! Let's set up your preferences.

What's your primary use case?
  1. Interactive development (R&D, exploration)
  2. Automated testing (CI/CD)
  3. Both (I'll use different flags for different contexts)

> 1

Great! I'll set your default workflow to: booktest -v -i

This means:
  -v: Verbose (show test outputs)
  -i: Interactive (pause on failures for review)

You can always override with different flags.

Create .booktest config with these defaults? [Y/n] y

✓ Created .booktest with:
  verbose=true
  interactive=true
  auto_report=true

Run 'booktest' to start testing!
```

### 7. Config File Defaults

Allow users to set defaults in `.booktest`:

```ini
# .booktest
verbose=true
interactive=true
auto_report=true           # Print failure reports on failure (default: true)
tips=true                  # Show contextual tips (disable with tips=false)
```

This lets users configure "interactive by default" or disable auto-reports if they prefer the old behavior.

## Consequences

### Positive

1. **Eliminates "magic spells"**
   - Users no longer need to memorize `-v -L -w -c` to debug failures
   - Auto-report shows what failed without extra commands
   - CI simplifies from `booktest -p8 || booktest -v -L -w -c` to just `booktest -p8`
   - No wasteful test re-runs

2. **Reduced friction for new users**
   - Failure reports appear automatically when needed
   - Contextual tips guide users to the right flags
   - Help output organized by workflow, not alphabetically
   - Users can find solutions without reading full docs

3. **Preserves Unix philosophy**
   - Flags remain composable
   - No breaking changes to existing behavior
   - Power users keep full control
   - Auto-report can be disabled

4. **Better discoverability**
   - Common workflows shown explicitly (including real CI pattern)
   - Reports appear when needed
   - Users learn by doing

5. **Maintains flexibility**
   - Config file allows personal defaults
   - Auto-report can be disabled if needed
   - Tips can be disabled for experts
   - Works consistently in CI and local development

### Negative

1. **More output by default**
   - Auto-reports add significant output on failures
   - Some users may prefer silent failures
   - Mitigated: Can be disabled with `auto_report=false`

2. **More code complexity**
   - Auto-report generation logic needed
   - Context detection logic needed
   - Help text becomes longer
   - Mitigated: Logic is isolated, can be toggled off

3. **Potential for confusion**
   - Some users may not understand why they see auto-reports
   - Reports might be overwhelming for first-time users
   - Mitigated: Reports are optional, tips explain what to do next

### Neutral

1. **Documentation maintenance**
   - Need to keep tips in sync with docs
   - More examples to maintain
   - Help text becomes longer

2. **User education shift**
   - From "read docs first" to "learn by doing"
   - Some users prefer comprehensive docs upfront

## Alternatives Considered

### Alternative 1: Change Default to Verbose

**Proposal**: Make `-v` (verbose) the default behavior

**Pros**:
- Users see output immediately
- Matches pytest, jest, cargo behavior
- No surprising silent execution

**Cons**:
- Breaking change for existing users
- CI logs become noisier by default
- Users who want silent execution need to add flag

**Decision**: Rejected. Breaking change too disruptive. Tips provide better balance.

### Alternative 2: Separate Commands for Different Workflows

**Proposal**:
- `booktest test` → silent CI mode
- `booktest dev` → verbose interactive mode
- `booktest review` → review mode

**Pros**:
- Clear intent from command name
- No flag memorization needed
- Matches modern CLI tools (e.g., `cargo build` vs `cargo test`)

**Cons**:
- Breaking change for existing users
- More commands to document
- Loses Unix composability

**Decision**: Rejected. Too radical a departure from current design. Could be revisited in 2.0.

### Alternative 3: Interactive Wizard Always

**Proposal**: Always show interactive wizard on first run, require user choice

**Pros**:
- Forces user to understand workflows
- Sets expectations upfront

**Cons**:
- Annoying for experienced users
- Blocks CI if not handled carefully
- Requires user input (not always available)

**Decision**: Rejected. Make wizard opt-in (`--setup`), not mandatory.

### Alternative 4: Do Nothing

**Proposal**: Keep current behavior, rely on documentation

**Pros**:
- No changes needed
- No risk of breaking anything
- Documentation already exists

**Cons**:
- New users continue to struggle
- High barrier to entry
- Poor first impression

**Decision**: Rejected. User experience issues are real and impact adoption.

## Implementation Plan

### Phase 1: Auto-Print Failure Report (HIGH PRIORITY)
**Goal**: Eliminate the need for `-v -L -w -c` spell

1. Add `print_failure_report_if_needed()` function to test runner
2. Hook into test execution exit flow (after results calculated)
3. Call `review()` function in non-interactive mode when:
   - Exit code is non-zero (failures or diffs)
   - Not already in interactive mode
   - `auto_report=true` in config (default)
4. Add config option:
   - `auto_report=true` (default)
5. Show helpful tips after report
6. Test with various failure scenarios

**Expected outcome**: `booktest` with failures automatically prints detailed report. No more memorizing flags. Works the same locally and in CI.

### Phase 2: Help Text Reorganization
1. Reorganize help output with workflow sections
2. Add "Common workflows" section at top
3. Show `booktest -p8` as the simple CI pattern (no fallback needed)
4. Group flags by purpose
5. Add examples to test selection

### Phase 3: Contextual Tips
1. Add tip detection logic to test runner
2. Show tips after test runs based on context
3. Only show if auto-report didn't already appear
4. Add `tips=false` config option

### Phase 4: Documentation Updates
1. Update README with R&D workflow first
2. Add "Flags Cheat Sheet" section
3. Document simplified CI pattern: just `booktest -p8`
4. Add "Understanding Exit Codes" section
5. Document auto-report feature
6. Update Quick Start guide with explanations

### Phase 5: Config File Defaults (Optional)
1. Support defaults in `.booktest` config
2. Document all config options (including auto_report)
3. Add `booktest --setup` wizard (optional)

### Phase 6: Validation
1. User testing with new users
2. Gather feedback on auto-report helpfulness
3. Measure reduction in "how do I see failures" questions
4. Iterate on report format
5. Update based on real usage patterns

## Success Metrics

1. **Reduced time-to-understand-failures**
   - Measure: Time from test failure to understanding what failed
   - Current: ~10 minutes (trial and error with flags)
   - Target: < 30 seconds (auto-report appears immediately)

2. **Reduced "magic spell" memorization**
   - Measure: Users running `booktest -v -L -w -c` explicitly
   - Current: Required for debugging
   - Target: Rarely needed (auto-report handles it)

3. **Reduced flag-related support questions**
   - Measure: GitHub issues/discussions about "how do I see output"
   - Target: 70% reduction (was 50%, higher with auto-report)

4. **Simplified CI usage**
   - Measure: CI configs using just `booktest -p8`
   - Current: Requires `booktest -p8 || booktest -v -L -w -c` pattern
   - Target: Simple `booktest -p8` with auto-report handling failures

5. **User satisfaction**
   - Measure: Survey responses about "ease of getting started"
   - Target: 8/10 satisfaction score

## References

- Booktest README: Quick Start guide
- CLI implementation: `booktest/cli.py`, `booktest/tests.py`
- Review implementation: `booktest/review.py`
- Previous CI pattern: `booktest -p8 || booktest -v -L -w -c` (wasteful re-runs)
- New CI pattern: `booktest -p8` (with auto-report)
- User feedback: GitHub issues #XXX, #YYY (to be added)
- Comparison tools: pytest, jest, cargo test
- Unix philosophy: Composable single-purpose tools

## Related ADRs

- ADR-002: Test Isolation vs Result States (review workflow)
- ADR-003: Snapshot Management Separation (storage and review)

## Appendix: Before and After Comparison

### Local Development

**Before (current behavior)**:
```bash
$ booktest
test/test_model.py::test_evaluation FAIL 2341 ms
# Exit, no details shown - "computer says no"

$ booktest -v -L -w -c   # User must know this spell
# [Detailed review shown]
```

**After (with auto-report)**:
```bash
$ booktest
test/test_model.py::test_evaluation FAIL 2341 ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Detailed review shown automatically]

💡 To review interactively, run: booktest -w
```

### CI Configuration

**Before (with wasteful re-run)**:
```yaml
- name: Run tests
  run: |
    booktest -p8 || booktest -v -L -w -c
```
- Requires knowing the `-v -L -w -c` spell
- Re-runs all tests sequentially on failure (slow!)
- If parallel run takes 5 minutes and fails, re-run takes another 10 minutes

**After (with auto-report)**:
```yaml
- name: Run tests
  run: booktest -p8
```
- Simple and obvious
- No re-runs - failure report prints immediately
- Failure details shown right away
- Total time: just the parallel run (5 minutes)
