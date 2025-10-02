# Snapshot Refactoring Plan: Remove Printing from Test Results

## Overview

This document details all snapshot generation points in booktest and how they currently print to test results. The goal is to remove this printing and replace it with proper reporting to the snapshot management system.

## Current Snapshot Types and Their Printing

### 1. HTTP Requests (`booktest/requests.py`)

**Class:** `SnapshotRequests`
**Entry point:** `snapshot_requests()` context manager
**Printing location:** Line 396-400

```python
# Current implementation (requests.py:396-400)
def stop(self):
    # ... save snapshots ...
    if len(snapshots) > 0:
        self.t.h1("request snaphots:")
        for i in snapshots:
            self.t.tln(f" * {i.request.url()} - {i.hash()}")
```

**What gets printed:**
```markdown
# request snaphots:
 * https://api.example.com/users - sha256:abc123...
 * https://api.example.com/posts - sha256:def456...
```

**Refactoring needed:**
- Remove `h1()` and `tln()` calls
- Add `self.t.report_snapshot_usage("http", hash, state)`
- Track all recorded requests for reporting

### 2. HTTPX Requests (`booktest/httpx.py`)

**Class:** `SnapshotHttpx`
**Entry point:** `snapshot_httpx()` context manager
**Printing location:** Line 328-332

```python
# Current implementation (httpx.py:328-332)
def stop(self):
    # ... save snapshots ...
    if len(snapshots) > 0:
        self.t.h1("httpx snaphots:")
        for i in snapshots:
            self.t.tln(f" * {i.request.url()} - {i.hash()}")
```

**What gets printed:**
```markdown
# httpx snaphots:
 * https://api.example.com/data - sha256:ghi789...
```

**Refactoring needed:**
- Remove `h1()` and `tln()` calls
- Add `self.t.report_snapshot_usage("httpx", hash, state)`
- Track all recorded requests for reporting

### 3. Environment Variables (`booktest/env.py`)

**Class:** `SnapshotEnv`
**Entry point:** `snapshot_env()` context manager
**Printing location:** Line 69-71

```python
# Current implementation (env.py:69-71)
def stop(self):
    # ... save snapshots ...
    if len(self.env_diff) > 0:
        self.t.h1("env snaphots:")
        for name, value in self.env_diff.items():
            self.t.tln(f" * {name}={value}")
```

**What gets printed:**
```markdown
# env snaphots:
 * DATABASE_URL=postgresql://localhost/test
 * API_KEY=test_key_123
```

**Refactoring needed:**
- Remove `h1()` and `tln()` calls
- Add `self.t.report_snapshot_usage("env", hash, state)`
- Calculate aggregate hash for all env vars

### 4. Function Calls (`booktest/functions.py`)

**Class:** `SnapshotFunctions`
**Entry point:** `snapshot_functions()` context manager
**Printing location:** Line 207-226

```python
# Current implementation (functions.py:207-226)
def stop(self):
    # ... save snapshots ...
    if len(all_hashes) > 0:
        self.t.h1("function call snapshots:")
        for function, hashes in all_hashes.items():
            aggregate_hash = self._calculate_aggregate(hashes)
            self.t.tln(f" * {function} - {aggregate_hash}:")
            for hash in hashes[:3]:  # Show first 3
                self.t.tln(f"   * {hash}")
            if len(hashes) > 3:
                self.t.tln(f"   * ...")
                self.t.tln(f"   * {len(hashes)} unique call in total")
```

**What gets printed:**
```markdown
# function call snapshots:
 * get_user_data - sha256:xyz789...:
   * sha256:aaa111...
   * sha256:bbb222...
   * sha256:ccc333...
   * ...
   * 15 unique call in total
```

**Refactoring needed:**
- Remove all `h1()` and `tln()` calls
- Add `self.t.report_snapshot_usage("func", aggregate_hash, state)`
- Store detailed call information in metadata, not test results

### 5. Mock Functions (`booktest/functions.py`)

**Entry point:** `mock_functions()` context manager
**Printing:** None (good!)

**Note:** `mock_functions()` doesn't currently print anything, so no refactoring needed.

### 6. Mock Environment (`booktest/env.py`)

**Entry points:** `mock_env()` and `mock_missing_env()`
**Printing:** None (good!)

**Note:** Mock functions don't print, only snapshot functions do.

## Refactoring Strategy

### Step 1: Add Snapshot Reporting API to TestCaseRun

```python
# Add to booktest/testcaserun.py

class TestCaseRun:
    def __init__(self, ...):
        # ... existing init ...
        self.snapshot_usage = {}  # Track snapshot usage

    def report_snapshot_usage(self,
                              snapshot_type: str,
                              hash_value: str,
                              state: SnapshotState,
                              details: dict = None):
        """Report snapshot usage for this test."""
        self.snapshot_usage[snapshot_type] = {
            'hash': hash_value,
            'state': state.value,
            'details': details or {},
            'timestamp': time.time()
        }

    def get_snapshot_state(self) -> SnapshotState:
        """Determine overall snapshot state from tracked usage."""
        if not self.snapshot_usage:
            return SnapshotState.INTACT

        states = [SnapshotState[u['state'].upper()]
                 for u in self.snapshot_usage.values()]

        if any(s == SnapshotState.FAIL for s in states):
            return SnapshotState.FAIL
        if any(s == SnapshotState.UPDATED for s in states):
            return SnapshotState.UPDATED

        return SnapshotState.INTACT
```

### Step 2: Refactor Each Snapshot Type

#### 2.1 Refactor `SnapshotRequests` (requests.py)

```python
# OLD (requests.py:396-400)
def stop(self):
    # ... save logic ...
    if len(snapshots) > 0:
        self.t.h1("request snaphots:")
        for i in snapshots:
            self.t.tln(f" * {i.request.url()} - {i.hash()}")

# NEW
def stop(self):
    # ... save logic ...

    # Determine state based on what happened
    if self.complete_snapshots or self.refresh_snapshots:
        state = SnapshotState.UPDATED  # We created/updated snapshots
    else:
        state = SnapshotState.INTACT   # We used existing snapshots

    # Calculate aggregate hash for all requests
    aggregate_hash = self._calculate_aggregate_hash(snapshots)

    # Report to system instead of printing
    self.t.report_snapshot_usage(
        snapshot_type="http",
        hash_value=aggregate_hash,
        state=state,
        details={
            'count': len(snapshots),
            'urls': [s.request.url() for s in snapshots],
            'hashes': [s.hash() for s in snapshots]
        }
    )
```

#### 2.2 Refactor `SnapshotHttpx` (httpx.py)

```python
# Similar refactoring to SnapshotRequests
def stop(self):
    # ... save logic ...

    if self.complete_snapshots or self.refresh_snapshots:
        state = SnapshotState.UPDATED
    else:
        state = SnapshotState.INTACT

    aggregate_hash = self._calculate_aggregate_hash(snapshots)

    self.t.report_snapshot_usage(
        snapshot_type="httpx",
        hash_value=aggregate_hash,
        state=state,
        details={
            'count': len(snapshots),
            'urls': [s.request.url() for s in snapshots],
            'hashes': [s.hash() for s in snapshots]
        }
    )
```

#### 2.3 Refactor `SnapshotEnv` (env.py)

```python
# OLD (env.py:69-71)
def stop(self):
    # ... save logic ...
    if len(self.env_diff) > 0:
        self.t.h1("env snaphots:")
        for name, value in self.env_diff.items():
            self.t.tln(f" * {name}={value}")

# NEW
def stop(self):
    # ... save logic ...

    if self.complete_snapshots or self.refresh_snapshots:
        state = SnapshotState.UPDATED
    else:
        state = SnapshotState.INTACT

    # Calculate hash of all env vars
    env_hash = self._calculate_env_hash(self.env_diff)

    self.t.report_snapshot_usage(
        snapshot_type="env",
        hash_value=env_hash,
        state=state,
        details={
            'count': len(self.env_diff),
            'variables': list(self.env_diff.keys())
            # Don't include values in details for security
        }
    )
```

#### 2.4 Refactor `SnapshotFunctions` (functions.py)

```python
# OLD (functions.py:207-226)
def stop(self):
    # ... save logic ...
    if len(all_hashes) > 0:
        self.t.h1("function call snapshots:")
        for function, hashes in all_hashes.items():
            aggregate_hash = self._calculate_aggregate(hashes)
            self.t.tln(f" * {function} - {aggregate_hash}:")
            # ... print details ...

# NEW
def stop(self):
    # ... save logic ...

    if self.complete_snapshots or self.refresh_snapshots:
        state = SnapshotState.UPDATED
    else:
        state = SnapshotState.INTACT

    # Calculate aggregate hash for all function calls
    function_summaries = {}
    for function, hashes in all_hashes.items():
        function_summaries[function] = {
            'aggregate_hash': self._calculate_aggregate(hashes),
            'count': len(hashes),
            'unique_calls': len(set(hashes))
        }

    overall_hash = self._calculate_overall_hash(function_summaries)

    self.t.report_snapshot_usage(
        snapshot_type="func",
        hash_value=overall_hash,
        state=state,
        details={
            'functions': function_summaries
        }
    )
```

### Step 3: Update TestCaseRun.end() to Use Snapshot State

```python
# In testcaserun.py:end()

# OLD: Always assume INTACT
snapshot_state = SnapshotState.INTACT

# NEW: Get actual state from tracked usage
snapshot_state = self.get_snapshot_state()

# Create two-dimensional result with real snapshot state
two_dim_result = TwoDimensionalTestResult(
    success=success_state,
    snapshotting=snapshot_state
)
```

### Step 4: Write Snapshot Metadata

```python
# Add to TestCaseRun.end(), after close()

def end(self):
    # ... existing logic ...

    # Write snapshot metadata to separate file
    if self.snapshot_usage:
        metadata_file = self.file("_snapshots/metadata.json")
        os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

        with open(metadata_file, 'w') as f:
            json.dump({
                'test_id': self.test_path,
                'snapshots': self.snapshot_usage,
                'result': {
                    'success': success_state.value,
                    'snapshotting': snapshot_state.value
                },
                'timestamp': time.time()
            }, f, indent=2)

    # ... rest of end() logic ...
```

## Migration Path

### Phase 1: Add Reporting (Non-Breaking)
1. Add `report_snapshot_usage()` to TestCaseRun
2. Add reporting calls to all snapshot classes
3. Keep existing printing (both happen in parallel)
4. Generate metadata files alongside test results

### Phase 2: Optional Flag (Transition)
1. Add `--no-snapshot-output` flag to suppress printing
2. Document new approach
3. Encourage teams to try new mode

### Phase 3: Default Change (Breaking)
1. Change default to not print snapshots
2. Add `--legacy-snapshot-output` flag to restore old behavior
3. Update documentation and examples

### Phase 4: Remove Legacy Code
1. Remove printing code entirely
2. Remove legacy flag
3. Clean up

## Testing Strategy

### Test Each Snapshot Type

Create tests that verify:
1. Snapshot usage is reported correctly
2. Metadata files are generated
3. Test results don't contain snapshot output
4. Snapshot state (INTACT/UPDATED/FAIL) is detected correctly

### Example Test

```python
def test_snapshot_reporting(t: bt.TestCaseRun):
    """Verify snapshot reporting works without printing."""
    t.h1("Snapshot Reporting Test")

    # Use snapshots
    with bt.snapshot_requests(t):
        response = requests.get("http://example.com")

    # Test result should NOT contain snapshot data
    t.tln("Response received successfully")

    # After test ends, verify metadata was written
    # (This would be checked by test framework)
```

## Files to Modify

1. **booktest/testcaserun.py**
   - Add `snapshot_usage` tracking
   - Add `report_snapshot_usage()` method
   - Add `get_snapshot_state()` method
   - Update `end()` to write metadata

2. **booktest/requests.py**
   - Remove printing from `SnapshotRequests.stop()`
   - Add reporting call

3. **booktest/httpx.py**
   - Remove printing from `SnapshotHttpx.stop()`
   - Add reporting call

4. **booktest/env.py**
   - Remove printing from `SnapshotEnv.stop()`
   - Add reporting call

5. **booktest/functions.py**
   - Remove printing from `SnapshotFunctions.stop()`
   - Add reporting call

6. **Test files**
   - Update expectations to not include snapshot output
   - Add new tests for snapshot reporting

## Open Questions

1. **Metadata file location**: Should be `_snapshots/metadata.json` or elsewhere?
2. **Hash calculation**: How to handle aggregate hashes for multiple requests/functions?
3. **Security**: Should env var values be in metadata or just variable names?
4. **Backward compatibility**: How long to support `--legacy-snapshot-output`?

## Success Criteria

- [ ] No snapshot data printed to test results
- [ ] All snapshot usage reported via API
- [ ] Metadata files generated with snapshot info
- [ ] Snapshot state (INTACT/UPDATED/FAIL) correctly detected
- [ ] Two-dimensional results reflect actual snapshot state
- [ ] All existing tests pass with updated expectations
- [ ] Documentation updated
- [ ] Migration guide written