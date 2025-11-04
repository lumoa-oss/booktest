# Snapshot Storage Inconsistency and Proposed Solution

## Problem Statement

### Current Behavior Inconsistency

**DVC Storage** (`DVCStorage.promote()`):
- Snapshots stored in staging area during test execution (`.booktest_cache/staging/`)
- On test success/acceptance: `promote()` moves snapshots from staging to cache
- Snapshots are automatically updated and pushed to remote
- ✅ **Semantics: Snapshots update automatically on success**

**Git Storage** (`GitStorage.promote()`):
- Snapshots stored in `test_name/_snapshots/` subdirectory during test execution
- On test success/acceptance: `promote()` does **nothing** (it's a no-op)
- Snapshots remain in `.out/` directory, never moved to `books/`
- ❌ **Semantics: Snapshots do NOT update automatically on success**

### The Core Issue

The two storage backends have **completely different semantics** for snapshot management:
- DVC: staging → permanent (on success)
- Git: write once, never promote

This violates the principle that storage backend should be an implementation detail that doesn't change user-visible behavior.

## Design Problem

### Moving Test Results (Current Behavior)

When accepting test results:
1. ✅ **Clear**: Move `test_name.md` from `.out/` to `books/`
2. ✅ **Clear**: Move `test_name/` directory from `.out/` to `books/`

### Moving Snapshots (Current Behavior)

When accepting test results:
3. ❓ **Fuzzy**: What to do with `test_name/_snapshots/` subdirectory?
   - It's part of the test result directory
   - But it contains snapshot data that should be managed separately
   - Moving the entire directory means snapshots are "accepted" implicitly
   - Not moving it means snapshots are lost

## Proposed Solution

### Separate Snapshot Storage

Move snapshots to a **separate location** that's managed independently of test results:

**Option A: Snapshot Directory**
```
books/
├── test_name.md                    # Test result (markdown)
├── test_name/                      # Test auxiliary files
│   ├── data.csv
│   └── image.png
└── test_name.snapshots/            # Snapshot storage (separate)
    ├── requests.json
    ├── httpx.json
    └── env.json
```

**Option B: Single Snapshot File** (Recommended)
```
books/
├── test_name.md                    # Test result (markdown)
├── test_name/                      # Test auxiliary files
│   ├── data.csv
│   └── image.png
└── test_name.snapshots.json        # All snapshots in one file
```

### Benefits

1. **Clear Semantics**: Snapshots are explicitly separate from test results
2. **Unified Promotion**: Both DVC and Git storage can implement promotion consistently:
   - During test: Write to `.out/test_name.snapshots.json`
   - On success: Move `.out/test_name.snapshots.json` → `books/test_name.snapshots.json`
3. **Fewer PR Changes**: One JSON file per test instead of multiple files in subdirectories
4. **Cleaner Structure**: No hidden `_snapshots/` subdirectories mixed with test data

### Implementation Strategy

#### Phase 1: Add Snapshot File Support (Git Storage)

```python
class GitStorage(SnapshotStorage):
    def __init__(self, base_path: str = "books/.out", frozen_path: str = "books"):
        self.base_path = Path(base_path)
        self.frozen_path = Path(frozen_path)
        self.use_snapshot_files = True  # New option

    def _get_snapshot_file_path(self, test_id: str) -> Path:
        """Get path to consolidated snapshot file."""
        parts = test_id.replace("::", "/").split("/")
        return self.base_path / f"{'/'.join(parts)}.snapshots.json"

    def fetch(self, test_id: str, snapshot_type: str) -> Optional[bytes]:
        """Fetch from snapshot file first, fallback to legacy _snapshots/ dir."""
        # Try snapshot file first (new format)
        snapshot_file = self._get_snapshot_file_path(test_id)
        frozen_file = self.frozen_path / snapshot_file.relative_to(self.base_path)

        if frozen_file.exists():
            snapshots = json.loads(frozen_file.read_bytes())
            if snapshot_type in snapshots:
                return json.dumps(snapshots[snapshot_type]).encode()

        # Fallback to legacy _snapshots/ directory
        return self._fetch_legacy(test_id, snapshot_type)

    def store(self, test_id: str, snapshot_type: str, content: bytes) -> str:
        """Store in snapshot file (new format)."""
        snapshot_file = self._get_snapshot_file_path(test_id)

        # Load existing snapshots or create new
        if snapshot_file.exists():
            snapshots = json.loads(snapshot_file.read_bytes())
        else:
            snapshots = {}

        # Update snapshot type
        snapshots[snapshot_type] = json.loads(content)

        # Write atomically
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = snapshot_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(snapshots, indent=2))
        temp_file.replace(snapshot_file)

        # Calculate hash
        return f"sha256:{hashlib.sha256(content).hexdigest()}"

    def promote(self, test_id: str, snapshot_type: str) -> None:
        """Move snapshot file from .out/ to books/ on success."""
        source = self._get_snapshot_file_path(test_id)
        dest = self.frozen_path / source.relative_to(self.base_path)

        if source.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)  # Copy instead of move (keep in .out for review)
```

#### Phase 2: Migration Path

1. **Backward compatibility**: Support reading from both formats
   - Try `test_name.snapshots.json` first
   - Fallback to `test_name/_snapshots/` directory
2. **Gradual migration**: Convert on next snapshot update
   - When storing new snapshot, use new format
   - Old snapshots remain until regenerated
3. **Migration tool**: Convert existing `_snapshots/` to `.snapshots.json`

#### Phase 3: Update Acceptance Flow

Modify test result acceptance to handle snapshot files:

```python
def accept_test_result(test_id: str):
    # Move markdown file
    move_file(f".out/{test_id}.md", f"books/{test_id}.md")

    # Move auxiliary directory if exists
    if exists(f".out/{test_id}/"):
        move_dir(f".out/{test_id}/", f"books/{test_id}/")

    # Move snapshot file if exists (NEW)
    if exists(f".out/{test_id}.snapshots.json"):
        move_file(f".out/{test_id}.snapshots.json", f"books/{test_id}.snapshots.json")
```

## Migration Example

### Before (Legacy Format)
```
books/
└── test/
    └── examples/
        └── snapshots_book.py/
            └── test_requests/
                ├── _snapshots/          # Hidden subdirectory
                │   ├── requests.json
                │   └── env.json
                └── data.csv
```

### After (New Format)
```
books/
└── test/
    └── examples/
        └── snapshots_book.py/
            ├── test_requests.md
            ├── test_requests.snapshots.json  # All snapshots in one file
            └── test_requests/
                └── data.csv              # Only test data, no snapshots
```

### Snapshot File Content
```json
{
  "requests": [
    {
      "method": "GET",
      "url": "https://api.example.com/data",
      "response": {...}
    }
  ],
  "env": {
    "API_KEY": "test-key",
    "ENV": "production"
  }
}
```

## Benefits Summary

| Aspect | Current (DVC) | Current (Git) | Proposed |
|--------|---------------|---------------|----------|
| Promotion | ✅ Works | ❌ No-op | ✅ Works |
| Semantics | Consistent | Inconsistent | Consistent |
| PR Changes | Manifest file | Many files | Single file |
| Structure | Staging + Cache | `_snapshots/` | `.snapshots.json` |
| Clarity | Good | Confusing | Excellent |

## Next Steps

1. Implement `GitStorage` with snapshot file support
2. Add backward compatibility for `_snapshots/` directories
3. Update promotion logic to move `.snapshots.json` files
4. Test with existing test suite
5. Document migration path for users
6. Consider similar approach for DVC storage (optional)
