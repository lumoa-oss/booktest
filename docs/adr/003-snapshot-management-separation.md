# ADR-003: Separate Snapshot Management from Test Results

## Status
Proposed

## Context

Currently, booktest embeds snapshot data directly in test result files. This creates several problems:

### Current Behavior
```python
def test_api_call(t):
    with snapshot_requests(t):
        response = requests.get("https://api.example.com/data")
        t.tln(f"Response: {response.json()}")  # Printed to test result
```

**Generated test result file:**
```markdown
# Test Result
Response: {"id": 123, "name": "example", ...}

# Snapshot Data (embedded)
HTTP Request: GET https://api.example.com/data
Response: {"id": 123, "name": "example", ...}
Hash: sha256:abc123...
```

### Problems

1. **Noise**: Snapshot data pollutes human-readable test results
2. **Git churn**: Snapshot changes cause test result diffs
3. **Forced recreation**: When snapshots change, entire test results must be recreated
4. **Coupling**: Can't update snapshots without updating test results
5. **No metadata**: Can't track which snapshots were used/produced without parsing results

## Decision

We will separate snapshot management into three distinct layers:

### 1. Test Result Files (Human-Readable)
**Purpose**: Show what the test verified, not how external dependencies were mocked

**Content**:
- Test logic output only
- Assertions and validations
- Calculated results and metrics
- NO snapshot data, NO hashes

**Example:**
```markdown
# Authentication Test
✅ Login successful
Response time: 245ms
Token format: Valid JWT
```

### 2. Snapshot Metadata (Machine-Readable)
**Purpose**: Track snapshot usage and state changes

**Storage**: Separate metadata file per test (e.g., `test.snapshots.json`)

**Content:**
```json
{
  "test_id": "test/auth::login",
  "snapshots": {
    "http": {
      "hash": "sha256:abc123...",
      "path": "_snapshots/http.json",
      "state": "intact",  // or "updated", "missing"
      "used_at": "2025-01-18T10:30:00Z"
    },
    "env": {
      "hash": "sha256:def456...",
      "path": "_snapshots/env.json",
      "state": "intact",
      "used_at": "2025-01-18T10:30:00Z"
    }
  },
  "result": {
    "success": "ok",
    "snapshotting": "intact"
  }
}
```

### 3. Snapshot Content (CAS)
**Purpose**: Store actual replay data (cassettes, env dumps, function recordings)

**Storage**: Content-addressable storage (from ADR-001)

**Content**: The actual snapshot data
```json
// _snapshots/http.json (stored in CAS)
{
  "requests": [
    {
      "method": "GET",
      "url": "https://api.example.com/data",
      "response": {"id": 123, "name": "example"}
    }
  ]
}
```

## Implementation Strategy

### Phase 1: Snapshot Reporting API

Add snapshot reporting methods to TestCaseRun:

```python
class TestCaseRun:
    def __init__(self):
        self.snapshot_usage = {}  # Track snapshot usage

    def report_snapshot_usage(self, snapshot_type: str,
                              hash_value: str,
                              state: SnapshotState):
        """Report that a snapshot was used during this test."""
        self.snapshot_usage[snapshot_type] = {
            'hash': hash_value,
            'state': state,
            'timestamp': datetime.now().isoformat()
        }

    def report_snapshot_created(self, snapshot_type: str,
                                hash_value: str,
                                path: str):
        """Report that a new snapshot was created."""
        self.snapshot_usage[snapshot_type] = {
            'hash': hash_value,
            'path': path,
            'state': SnapshotState.UPDATED,
            'timestamp': datetime.now().isoformat()
        }
```

### Phase 2: Update Snapshot Functions

Modify snapshot functions to use reporting instead of printing:

```python
# OLD: Prints to test result
def snapshot_requests(t: TestCaseRun):
    # ... record requests ...
    t.tln(f"Recorded {len(requests)} HTTP requests")  # Noise!

# NEW: Reports to system
def snapshot_requests(t: TestCaseRun):
    storage = get_storage()

    # Check existing snapshot
    existing = storage.fetch(t.test_id, "http")

    if existing:
        # Use existing snapshot for replay
        t.report_snapshot_usage("http", existing.hash, SnapshotState.INTACT)
        return replay_from_snapshot(existing)
    else:
        # Record new snapshot
        recorded = record_requests()
        new_hash = storage.store(t.test_id, "http", recorded)
        t.report_snapshot_created("http", new_hash, "_snapshots/http.json")
        return recorded
```

### Phase 3: Snapshot Metadata Persistence

At test end, write snapshot metadata to separate file:

```python
def end(self):
    # ... existing logic ...

    # Write snapshot metadata separately
    if self.snapshot_usage:
        metadata_path = self.file("_snapshots/metadata.json")
        write_json(metadata_path, {
            'test_id': self.test_path,
            'snapshots': self.snapshot_usage,
            'result': {
                'success': two_dim_result.success.value,
                'snapshotting': two_dim_result.snapshotting.value
            },
            'timestamp': datetime.now().isoformat()
        })

    return rv, interaction
```

### Phase 4: Snapshot State Detection

Determine snapshot state based on usage tracking:

```python
def determine_snapshot_state(self) -> SnapshotState:
    """Determine overall snapshot state from usage tracking."""
    if not self.snapshot_usage:
        return SnapshotState.INTACT  # No snapshots used

    states = [s['state'] for s in self.snapshot_usage.values()]

    # If any snapshot failed, overall state is FAIL
    if any(s == SnapshotState.FAIL for s in states):
        return SnapshotState.FAIL

    # If any snapshot was updated, overall state is UPDATED
    if any(s == SnapshotState.UPDATED for s in states):
        return SnapshotState.UPDATED

    # All snapshots intact
    return SnapshotState.INTACT
```

## User Perspective Changes

### Before (Current)
```bash
$ booktest test/auth::login -v
# Test Result
✅ Login successful
Response: {"token": "eyJ..."}

# Snapshot: HTTP Request  ← Noise in test result!
GET https://api.example.com/login
Response: {"token": "eyJ..."}
Hash: sha256:abc123...

test/auth::login OK in 15ms
```

### After (Proposed)
```bash
$ booktest test/auth::login -v
# Test Result
✅ Login successful
Token format: Valid JWT

test/auth::login OK/INTACT in 15ms

# Snapshot info available separately
$ booktest snapshots test/auth::login
Snapshots for test/auth::login:
  http:  sha256:abc123... (intact, last used 2s ago)
  env:   sha256:def456... (intact, last used 2s ago)
```

### Snapshot Commands
```bash
# View snapshot usage
booktest snapshots [test_pattern]

# View snapshot details
booktest snapshots test/auth::login --details

# Compare snapshot changes
booktest snapshots --diff

# Clean unused snapshots
booktest snapshots --gc
```

## Benefits

1. **Clean test results**: Only show test logic output, not infrastructure details
2. **Independent updates**: Update snapshots without touching test results
3. **Queryable metadata**: Can inspect snapshot state without parsing test files
4. **Better tooling**: Snapshot management commands separate from test execution
5. **Reduced Git noise**: Snapshot metadata changes don't pollute test result diffs
6. **Proper layering**: Clear separation between what (test result) and how (snapshots)

## Migration Path

### Step 1: Add Reporting (Non-Breaking)
- Add `report_snapshot_usage()` methods to TestCaseRun
- Update snapshot functions to call reporting methods
- Keep existing printing for backward compatibility

### Step 2: Metadata Generation (Additive)
- Generate `.snapshots.json` metadata files alongside tests
- Users can inspect these to understand snapshot usage
- Test results still include snapshot info (backward compatible)

### Step 3: Remove Printing (Breaking Change)
- Remove snapshot data from test result output
- Announce breaking change with migration guide
- Provide `--legacy-snapshot-output` flag for transition period

### Step 4: Full Separation (Complete)
- Snapshot management fully independent
- Clean test results with no infrastructure noise
- Snapshot commands for inspection and management

## Example: End-to-End Flow

### Writing Test
```python
def test_user_profile(t: bt.TestCaseRun):
    """Test user profile retrieval."""
    with bt.snapshot_requests(t):  # Auto-reports snapshot usage
        user = get_user_profile(123)

    # Test result only contains verification
    t.h1("User Profile Test")
    t.tln(f"Name: {user.name}")
    t.tln(f"Email format: {'valid' if '@' in user.email else 'invalid'}")
```

### Test Execution
```bash
$ booktest test/profile::test_user_profile -v
# User Profile Test
Name: John Doe
Email format: valid

test/profile::test_user_profile OK/INTACT in 12ms

# Snapshot metadata written to:
# books/test/profile/_snapshots/metadata.json
```

### Snapshot Inspection
```bash
$ booktest snapshots test/profile::test_user_profile
Snapshots for test/profile::test_user_profile:
  http: sha256:7b1a4f... (intact)
    └─ GET /api/users/123

$ booktest snapshots test/profile::test_user_profile --show
HTTP Snapshot (sha256:7b1a4f...):
  Request: GET /api/users/123
  Response: {"id": 123, "name": "John Doe", ...}
```

## Open Questions

1. **Metadata storage location**: Same directory as test results, or separate `_snapshots/` dir?
2. **Metadata format**: JSON, YAML, or custom format?
3. **Snapshot inspection UI**: CLI only, or also web UI?
4. **Backward compatibility period**: How long to support both modes?

## References

- ADR-001: DVC Content-Addressable Storage
- ADR-002: Two-Dimensional Test Results
- Original design: `.ai/tasks/booktest-dvc-redesign.md`