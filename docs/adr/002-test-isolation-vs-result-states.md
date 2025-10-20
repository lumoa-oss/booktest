# ADR-002: Separate Test Isolation from Result States

## Status
Proposed

## Context

Currently in booktest, there are two distinct but conflated concepts:

### 1. Test Result States (Success/Failure/Difference)
- **OK**: Test passed, output matches expectations
- **DIFF**: Test output differs from expectations, requires human review
- **FAIL**: Test crashed or had assertion failures

### 2. Test Isolation/Boxing (Deterministic Replay)
Whether a test can run in complete isolation without external dependencies:
- **Isolated/Boxed**: All external calls (HTTP, env vars, functions) are recorded in gazettes and can be replayed deterministically
- **Non-isolated**: Test makes live external calls and cannot be replayed deterministically

### Current Problem

These concepts are currently mixed because cassette/snapshot hashes are embedded in test result files. When external dependencies change:
1. Cassette hash changes (isolation breaks)
2. Test result shows DIFF (forces human review)
3. Human must review even when actual test logic is unchanged
4. Many tests require manual approval for purely mechanical changes

This conflation causes:
- **False positives**: Tests marked as DIFF when only external dependencies changed
- **Review fatigue**: Humans reviewing mechanical cassette updates
- **CI instability**: Tests failing due to external service changes rather than logic errors
- **Git noise**: Cassette hashes pollute human-readable test results

## Decision

We will use a two-dimensional approach that clearly separates test logic outcomes from snapshot management:

### 1. Two-Dimensional Test Results
Each test returns two orthogonal values:

```python
class TestResult:
    success: SuccessState      # Test logic outcome
    snapshotting: SnapshotState  # Snapshot integrity outcome

class SuccessState(Enum):
    OK = "ok"       # Test logic passed, output matches expectations
    DIFF = "diff"   # Test logic output differs, needs human review
    FAIL = "fail"   # Test logic failed (exceptions, assertions)

class SnapshotState(Enum):
    INTACT = "intact"    # Snapshots are current and valid
    UPDATED = "updated"  # Snapshots were refreshed during this run
    FAIL = "fail"        # Snapshot mechanism failed
```

### 2. Test Isolation Modes (Configuration)
Tests can be configured to run in different isolation modes:
- **HERMETIC**: Test runs with snapshots, deterministic replay
- **INTEGRATED**: Test makes live external calls, no snapshots
- **AUTO**: Use snapshots when available, fall back to live calls

### 3. State Matrix
```
OK + INTACT   = ✅ Perfect - test passed, snapshots valid
OK + UPDATED  = ✅ Test passed, snapshots auto-refreshed
OK + FAIL     = ⚠️  Test passed but snapshot update failed

DIFF + INTACT = ❓ Test output changed, snapshots unchanged (human review)
DIFF + UPDATED= ❓ Test output changed, snapshots updated (human review)
DIFF + FAIL   = ❓ Test output changed, snapshot update failed

FAIL + *      = ❌ Test failed (snapshot state irrelevant)
```

#### Phase 2: Automatic Snapshot Management
- **Smart auto-updates**: `OK + UPDATED` scenarios don't require human review
- **Selective refresh**: Only update snapshots for tests that pass (`OK` success state)
- **Failure isolation**: Snapshot failures don't affect test success determination

#### Phase 3: CI/Review Workflow
```yaml
# Review requirements based on two-dimensional results
OK + INTACT:   No review needed - test passed, snapshots valid
OK + UPDATED:  No review needed - test passed, snapshots auto-refreshed
OK + FAIL:     Warning only - test passed but snapshot update failed

DIFF + INTACT: Human review required - test logic may have changed
DIFF + UPDATED: Human review required - test logic changed, snapshots updated
DIFF + FAIL:   Human review required - test logic changed, snapshot update failed

FAIL + *:      Test failed - fix test logic first, then address snapshots
```

#### Phase 4: Developer Experience
```bash
# New CLI commands
./do test --mode=hermetic          # Run with snapshots only (fail if missing)
./do test --mode=integrated        # Run with live external calls
./do test --refresh-snapshots      # Force snapshot updates for passing tests
./do test --require-hermetic       # CI mode - fail if any tests go INTEGRATED

# Two-dimensional status reporting
./do test --status
# Output:
# test/api::login     OK/INTACT    ✅ Ready
# test/api::search    DIFF/UPDATED ❓ Review needed
# test/db::migrate    OK/UPDATED   ✅ Snapshots refreshed
# test/net::timeout   FAIL/FAIL    ❌ Fix test logic
```

## Consequences

### Positive

1. **Reduced review fatigue**: Only `DIFF` success states require human review
2. **Automatic snapshot management**: `OK + UPDATED` scenarios auto-update without review
3. **Clear separation**: Test logic success independent of snapshot management
4. **Better debugging**: Can distinguish test failures from snapshot issues
5. **Actionable results**: Each state combination has clear next steps
6. **Backward compatibility**: Current OK/DIFF/FAIL maps to success dimension

### Negative

1. **Complexity increase**: Additional state to track and understand
2. **Migration effort**: Existing tests need isolation classification
3. **Tooling updates**: CLI and reporting tools need updates
4. **Learning curve**: Teams need to understand isolation concepts

### Neutral

1. **Storage requirements**: Isolation state adds metadata but gazette storage already planned
2. **Configuration**: Teams can choose their isolation policies per project

## Implementation Plan

### Phase 1: Two-Dimensional Results (2-3 weeks)
- Update TestResult to include both success and snapshotting states
- Modify TestCaseRun.end() to return two-dimensional results
- Update CLI reporting to show both dimensions
- Modify storage layer integration

### Phase 2: Automatic Snapshot Management (2-3 weeks)
- Implement smart snapshot refresh logic for `OK + UPDATED` scenarios
- Add snapshot hash comparison and update mechanisms
- Create mode-based test execution (HERMETIC/INTEGRATED/AUTO)
- Update review CLI to handle two-dimensional states

### Phase 3: CI/CD Integration (1-2 weeks)
- Add CI policies for two-dimensional results
- Implement automated snapshot promotion for `OK + UPDATED`
- Update reporting dashboards
- Add filtering by success/snapshot states

### Phase 4: Migration and Tooling (1-2 weeks)
- Create migration path from current single-dimensional results
- Add backward compatibility layer
- Documentation and examples
- Team training on two-dimensional results

## Examples

### Before (Current State)
```
test/auth::login    DIFF    # Single dimension - was it logic or snapshots?
```
External API response changes → Test shows DIFF → Human must review even mechanical changes

### After (Two-Dimensional Results)
```
test/auth::login    OK/UPDATED    # Test logic passed, snapshots refreshed
test/search::query  DIFF/INTACT   # Test logic changed, needs human review
test/db::conn       FAIL/FAIL     # Test failed, snapshot update also failed
```

**Clear decision matrix:**
- `OK/UPDATED` → Auto-approve, no human review needed
- `DIFF/*` → Human review required for test logic changes
- `FAIL/*` → Fix test logic first, snapshot state secondary

**Clean separation:**
- Test result files contain only human-reviewable test output
- Snapshot metadata managed separately by storage layer
- Snapshot refreshes don't trigger false positive reviews

## Alternatives Considered

### 1. Keep Current System
- Pros: No changes needed, well understood
- Cons: Continued review fatigue, Git noise, CI instability

### 2. Remove All Snapshots
- Pros: Eliminates complexity
- Cons: Loses deterministic replay, regression detection, review-driven workflow

### 3. Manual Gazette Management Only
- Pros: Simple implementation
- Cons: Doesn't solve automatic update problem, still requires manual intervention

### 4. Different Terminology
- **"Mocked/Stubbed/Live"**: Less precise, doesn't align with industry standards
- **"Offline/Online"**: Ambiguous, could confuse with network connectivity
- **"Sealed/Open"**: Not widely recognized terminology

## Industry Alignment

This proposal aligns with established testing terminology:

- **Google's Test Sizes**: Uses "hermetic" for fully isolated tests
- **Bazel**: Distinguishes between "hermetic" and "non-hermetic" tests
- **Martin Fowler's Test Pyramid**: Discusses isolation levels in testing
- **Netflix/Spotify**: Use similar isolation classifications for microservices testing

## References

- Google Testing Blog: "Test Sizes" - https://testing.googleblog.com/2010/12/test-sizes.html
- Bazel Test Encyclopedia: https://bazel.build/reference/test-encyclopedia
- Martin Fowler: "Test Pyramid" - https://martinfowler.com/articles/practical-test-pyramid.html
- Original design document: `.ai/tasks/booktest-dvc-redesign.md`
- ADR-001: DVC Content-Addressable Storage