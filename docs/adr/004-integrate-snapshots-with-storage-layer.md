# ADR-004: Integrate Snapshot System with Storage Layer

## Status

Proposed

## Context

Currently, the snapshot system has three separate concerns:

1. **Storage abstraction** (`storage.py`) - Git/DVC backend support
2. **Snapshot reporting** (`testcaserun.py`) - tracking and reporting snapshot usage
3. **Individual snapshotters** (requests, httpx, env, functions) - performing snapshots with direct file I/O

The snapshotters currently bypass the storage abstraction and use direct file operations:
- `frozen_snapshot_path()` / `out_snapshot_path()` for path resolution
- Direct `json.load()` / `json.dump()` operations
- Manual file existence checks

This creates several issues:
- Snapshot files cannot benefit from DVC content-addressable storage
- Storage logic is duplicated across snapshotters
- No unified interface for snapshot persistence
- Testing storage backends is difficult

## Decision

Integrate the snapshot system with the storage layer by:

1. **Make snapshotters storage-aware**: Each snapshotter (SnapshotRequests, SnapshotHttpx, etc.) should use the storage abstraction instead of direct file I/O

2. **Unified snapshot interface**: Create a common pattern for all snapshotters:
   ```python
   class SnapshotRequests:
       def __init__(self, t: TestCaseRun, ...):
           self.storage = t.get_storage()  # Get storage from test context

       def start(self):
           # Load snapshots via storage
           content = self.storage.fetch(self.t.test_id, "http")

       def stop(self):
           # Store snapshots via storage
           content = json.dumps(stored).encode('utf-8')
           hash_value = self.storage.store(self.t.test_id, "http", content)

           # Report with hash from storage
           self.t.report_snapshot_usage(
               snapshot_type="http",
               hash_value=hash_value,  # Use hash from storage layer
               state=state,
               details={...}
           )
   ```

3. **Storage initialization**: TestCaseRun should initialize and provide storage:
   ```python
   class TestCaseRun:
       def __init__(self, ...):
           self.storage = self._init_storage()

       def _init_storage(self):
           mode = self.config.get("storage.mode", "auto")
           if mode == "auto":
               # Auto-detect DVC, fallback to Git
               if DVCStorage.is_available():
                   return DVCStorage(...)
           elif mode == "dvc":
               return DVCStorage(...)
           return GitStorage(...)

       def get_storage(self):
           return self.storage
   ```

4. **Deprecate path helpers**: The `frozen_snapshot_path()`, `out_snapshot_path()`, and `have_snapshots_dir()` helpers become implementation details of GitStorage, not public API

5. **Hash reporting alignment**: The storage layer calculates content hashes (SHA256), which should be used directly in snapshot reporting instead of recalculating

## Benefits

1. **DVC support**: All snapshot types automatically work with DVC storage
2. **Consistency**: Single storage interface for all snapshot operations
3. **Testability**: Easy to inject mock storage for testing
4. **Performance**: Storage layer can optimize operations (batching, caching)
5. **Separation of concerns**: Snapshotters focus on snapshot logic, not storage details
6. **Hash consistency**: Single source of truth for content hashes

## Implementation Plan

### Phase 1: Storage Integration in TestCaseRun
1. Add `storage` field to TestCaseRun.__init__()
2. Implement `_init_storage()` method with auto-detection
3. Add `get_storage()` accessor method

### Phase 2: Migrate Snapshotters (one at a time)
For each snapshotter (requests, httpx, env, functions):
1. Update __init__ to accept/retrieve storage
2. Replace file loading with `storage.fetch()`
3. Replace file saving with `storage.store()`
4. Use storage-provided hash in `report_snapshot_usage()`
5. Update tests to verify storage integration
6. Maintain backward compatibility during migration

### Phase 3: Storage Abstraction Enhancements
1. Add `exists()` check to storage interface (already present)
2. Add batch operations if needed (fetch_many, store_many)
3. Consider snapshot metadata storage (currently separate)

### Phase 4: Path Helper Deprecation
1. Move path logic into GitStorage implementation
2. Keep helpers for backward compatibility but mark as deprecated
3. Update documentation to recommend storage API

## Migration Strategy

The migration should be gradual:
1. Keep existing path-based code working during transition
2. Migrate one snapshot type at a time with tests
3. Support both old and new snapshot locations during migration
4. GitStorage should handle legacy paths for frozen snapshots

## Example: Migrating SnapshotHttpx

**Before:**
```python
class SnapshotHttpx:
    def __init__(self, t: TestCaseRun, ...):
        self.snapshot_file = frozen_snapshot_path(t, "httpx.json")
        self.snapshot_out_file = out_snapshot_path(t, "httpx.json")

        if file_or_resource_exists(self.snapshot_file, t.resource_snapshots):
            with open_file_or_resource(self.snapshot_file, t.resource_snapshots) as f:
                snapshots = json.load(f)

    def stop(self):
        with open(self.snapshot_out_file, "w") as f:
            json.dump(stored, f, indent=4)
```

**After:**
```python
class SnapshotHttpx:
    def __init__(self, t: TestCaseRun, ...):
        self.storage = t.get_storage()
        self.test_id = t.test_id

        content = self.storage.fetch(self.test_id, "httpx")
        if content:
            snapshots = json.loads(content.decode('utf-8'))

    def stop(self):
        content = json.dumps(stored, indent=4).encode('utf-8')
        hash_value = self.storage.store(self.test_id, "httpx", content)

        self.t.report_snapshot_usage(
            snapshot_type="httpx",
            hash_value=hash_value,  # From storage, not recalculated
            state=state,
            details={...}
        )
```

## Configuration

Storage configuration in `booktest.toml` or test config:

```toml
[storage]
mode = "auto"  # auto | git | dvc
fallback_mode = "git"

# DVC-specific settings
[storage.dvc]
cache_dir = ".dvc/cache"
remote = "origin"  # optional
```

## Consequences

### Positive
- Unified storage abstraction across all snapshot types
- Automatic DVC support for all snapshots
- Cleaner separation of concerns
- Better testability with mock storage
- Performance optimization opportunities

### Negative
- Migration effort required for all snapshotters
- Need to maintain backward compatibility during transition
- Additional abstraction layer may add complexity

### Neutral
- Storage configuration becomes more important
- Users need to understand storage modes
- Documentation updates required

## Related Decisions

- ADR-001: DVC Content-Addressable Storage (foundation)
- ADR-002: Two-Dimensional Test Results (reporting)
- ADR-003: Snapshot Management Separation (reporting vs content)

## Notes

This ADR builds on ADR-001 by actually using the storage abstraction that was designed. It also complements ADR-003 by making the storage of snapshot content consistent with the reporting system.
