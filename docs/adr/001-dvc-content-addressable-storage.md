# ADR-001: Replace Git-Based Snapshot Storage with DVC Content-Addressable Storage

## Status
Proposed

## Context

Booktest currently stores test snapshots and cassettes directly in Git repositories under `_snapshots/` directories. These snapshots include:
- Environment variable dumps
- HTTP/HTTPX response cassettes
- Function call snapshots
- Human-readable test results with embedded gazette hashes

This approach creates several problems:
1. **Git noise**: Large snapshot files create bulky pull requests and frequent merge conflicts
2. **Review difficulty**: Changes to snapshots dominate PR diffs, obscuring actual code changes
3. **Storage inefficiency**: Binary and large JSON files are poorly suited for Git's delta compression
4. **Hash pollution**: Gazette hashes embedded in human-readable results force unnecessary re-creation

Despite these issues, the current system provides valuable features we must preserve:
- Review-driven testing workflow with rich Markdown/HTML reports
- Deterministic CI replay without live API calls
- Parallel test execution with dependency management
- Easy rollback to previous snapshot versions

## Decision

We will adopt a hybrid storage architecture that separates human-reviewable content from machine replay data, with automatic fallback to Git-based storage when DVC is not available:

### 1. Content-Addressable Storage (CAS) for Machine Data
Store replay payloads (cassettes, snapshots) in a remote content-addressable storage system using DVC (Data Version Control), keyed by SHA256 hash of content.

### 2. Git for Minimal Pointers
Keep only small manifest files or DVC pointer files in Git, reducing PR noise to 1-3 line changes per test update.

### 3. Separation of Concerns
- **Result files**: Optional, minimal Markdown documents for human review (no embedded hashes)
- **Gazette files**: Machine replay data stored in CAS, referenced by digest

### 4. Fallback Strategy
When DVC is not configured or unavailable, the system will:
- **Local Development**: Fall back to Git-based storage with a warning message
- **CI/CD**: Can be configured to either fail fast or use Git storage with size limits
- **Migration Path**: Allow gradual adoption where teams can start with Git and migrate to DVC later

### 5. Booktest CLI Workflow

The existing booktest commands will be enhanced to work with DVC storage:

- **Test execution**: `./do test` or `booktest test` - runs tests, fetching snapshots from CAS when available
- **Review mode**: `./do test -r` or `booktest test -r` - shows diffs between current and stored snapshots
- **Update/approve**: `./do test -u` or `booktest test -u` - updates snapshots with current results
- **Continuous mode**: `./do test -c` - continues on failure, useful for reviewing multiple changes
- **Parallel execution**: `./do test -p8` - runs tests in parallel with 8 workers

### 6. Storage Structure

#### Remote CAS Layout:
```
<remote>/booktest/blobs/
  env/sha256/ab/<sha256>     # Environment snapshots
  http/sha256/cd/<sha256>    # HTTP cassettes
  httpx/sha256/ef/<sha256>   # HTTPX cassettes
  func/sha256/01/<sha256>    # Function snapshots
```

#### Git Repository (Manifest Mode):
```yaml
# booktest.manifest.yaml
storage_mode: dvc  # or 'git' for fallback
testsuite/test_dir::test_topic_model:
  env:   "sha256:7b1a4f...e39"
  http:  "sha256:4c0f9b...21a"
  httpx: "sha256:a3d011...9fd"
  func:  "sha256:92b8ce...b55"
```

#### Fallback Mode Configuration:
```toml
# booktest.toml
[storage]
mode = "auto"  # auto-detect: use DVC if available, else Git
fallback_mode = "git"  # what to use when DVC unavailable
git_snapshot_size_limit = "100KB"  # warn if Git snapshots exceed this
require_dvc_in_ci = true  # fail in CI if DVC not configured
```

## Consequences

### Positive

1. **Minimal Git footprint**: PRs show only manifest changes (1-3 lines) instead of large snapshot diffs
2. **No merge conflicts**: Hash-based references eliminate content merge conflicts
3. **Preserved ergonomics**: Review-driven CLI and rich reports remain unchanged
4. **Efficient storage**: CAS deduplicates identical snapshots across tests and branches
5. **Clean separation**: Human-reviewable content separate from machine replay data
6. **CI determinism**: Tests replay from approved baselines without live API calls

### Negative

1. **Additional dependency**: Requires DVC or similar CAS tool installation
2. **Remote storage needed**: Must provision and manage remote storage (S3, GCS, etc.)
3. **Migration complexity**: Existing snapshots must be migrated to new system
4. **Network dependency**: Tests require network access to fetch snapshots
5. **Learning curve**: Developers must understand new manifest/pointer system

### Neutral

1. **Garbage collection**: Requires periodic cleanup of unreferenced blobs
2. **Two-stage commits**: Approve step now updates both manifest and remote storage
3. **CI changes**: Build pipelines must add `dvc pull` before test execution

## Implementation Plan

### Phase 1: Storage Backend with Fallback
- Implement CAS push/pull operations with DVC detection
- Add fallback to Git-based storage when DVC unavailable
- Create unified storage interface abstracting DVC vs Git
- Add staging/keep blob lifecycle
- Create manifest reader/writer

### Phase 2: CLI Integration
- Modify `booktest test` (or `./do test`) to detect storage mode and fetch appropriately
- Update `booktest test -u` (update/approve mode) to promote blobs and update manifest
- Enhance `booktest test -r` (review mode) to show meaningful diffs
- Add `--storage-mode` flag to force specific backend
- Implement size warnings for Git fallback mode

### Phase 3: Migration
- Script to extract existing snapshots to CAS
- Strip embedded hashes from result files
- Update `.gitignore` for local snapshot caches
- Add migration command: `booktest test --migrate-to-dvc` or similar
- Support incremental migration (some tests in Git, others in DVC)

### Phase 4: CI/CD
- Update pipelines to use `dvc pull` when available
- Add environment variable `BOOKTEST_REQUIRE_DVC` for strict mode
- Generate consolidated HTML report artifacts
- Implement mark-and-sweep garbage collection
- Add storage mode detection to CI status checks

## Alternatives Considered

### 1. Git LFS
- Pros: Simpler than DVC, integrates with Git
- Cons: Still creates PR noise, no content deduplication, requires LFS server

### 2. External Database
- Pros: Could provide richer querying
- Cons: Operational complexity, requires database maintenance, not file-oriented

### 3. Keep Current System
- Pros: No migration needed, well-understood
- Cons: Continued Git bloat, merge conflicts, poor reviewer experience

### 4. Remove Snapshots Entirely
- Pros: Eliminates storage problem
- Cons: Loses deterministic replay, review-driven workflow, regression detection

## References

- Original design document: `.ai/tasks/booktest-dvc-redesign.md`
- DVC documentation: https://dvc.org/
- Content-addressable storage pattern: https://en.wikipedia.org/wiki/Content-addressable_storage
- ADR format: https://adr.github.io/