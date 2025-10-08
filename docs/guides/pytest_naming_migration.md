# Pytest-Style Naming Migration Design

## Overview

Migrate booktest's test naming from current format to pytest-compatible format for better CLI ergonomics and standardization.

## Current vs Proposed

### Current Format
```
File: test/foo_test.py
Class: FooTestBook
Method: test_bar()

Current name: test/foo/bar
CLI usage: ./do test test/foo/bar
```

### Proposed Format
```
File: test/foo_test.py
Class: FooTestBook
Method: test_bar()

Proposed name: test/foo_test.py::FooTestBook::test_bar
CLI usage: ./do test test/foo_test.py::FooTestBook::test_bar
```

For standalone test functions:
```
File: test/simple_test.py
Function: test_example()

Proposed name: test/simple_test.py::test_example
CLI usage: ./do test test/simple_test.py::test_example
```

## Benefits

1. **Standard convention**: Matches pytest, familiar to Python developers
2. **Better autocomplete**: File-first approach works better with shell completion
3. **Clearer structure**: Explicit file → class → method hierarchy
4. **No ambiguity**: File path is literal, not cleaned/transformed

## Filesystem Mapping Challenge

### The Problem

The `:` character used in pytest format (`::`) creates filesystem issues:
- **Windows**: `:` is illegal in filenames
- **Unix**: Legal but awkward, breaks many tools
- **URLs**: Requires encoding

### Current Filesystem Usage

Test names are used for:
1. **Output files**: `{books_dir}/{test_name}.md`
2. **Cache files**: `{out_dir}/{test_name}.bin`
3. **Report files**: `{out_dir}/{test_name}.txt`
4. **Log files**: `{out_dir}/{test_name}.log`
5. **Snapshot directories**: `{out_dir}/{test_name}/_snapshots/`
6. **DVC manifest keys**: `test_name: {snapshot_type: hash}`
7. **Batch directories**: `{out_dir}/.batches/{test_name}/`

### Example Current Structure
```
books/
  test/
    examples/
      snapshots/
        httpx.md              # Output
        httpx.bin             # Cache
        httpx.txt             # Report
        httpx.log             # Log
        httpx/                # Snapshot dir
          _snapshots/
            metadata.json

booktest.manifest.yaml:
  test/examples/snapshots/httpx:
    httpx: sha256:abc123...
```

## Proposed Solution: Two-Layer Architecture

### Layer 1: Display/CLI Layer (pytest format)
- User-facing test names use pytest format
- CLI accepts pytest format
- Reporting shows pytest format
- Selection/filtering uses pytest format

### Layer 2: Filesystem Layer (encoded format)
- Internal filesystem paths use encoded safe names
- Bidirectional mapping between formats
- Maintains backwards compatibility

### Encoding Options

#### Option A: Replace `::` with `/` (simplest, recommended)
```
Display:    test/foo_test.py::FooTestBook::test_bar
Filesystem: test/foo_test.py/FooTestBook/test_bar

Display:    test/simple_test.py::test_example
Filesystem: test/simple_test.py/test_example
```

**Pros:**
- Natural, readable
- Works on all platforms
- Minimal changes to existing code
- Clean directory structure

**Cons:**
- File path includes `.py` in directory name (unusual but harmless)
- Could theoretically conflict if someone has `foo_test.py/` directory

#### Option B: Replace `::` with `__` (flat)
```
Display:    test/foo_test.py::FooTestBook::test_bar
Filesystem: test/foo_test.py__FooTestBook__test_bar

Display:    test/simple_test.py::test_example
Filesystem: test/simple_test.py__test_example
```

**Pros:**
- Flat structure (no nested dirs)
- Clear delimiter
- No ambiguity

**Cons:**
- Long filenames
- Less readable
- Loses hierarchical structure

#### Option C: Custom encoding with hash
```
Display:    test/foo_test.py::FooTestBook::test_bar
Filesystem: test/foo_test.py/FooTestBook/test_bar
Mapping:    .booktest_name_cache.json (display → filesystem)
```

**Pros:**
- Can handle any edge cases
- Future-proof

**Cons:**
- Requires mapping file
- Complex migration
- Harder to debug

### Recommendation: Option A (Replace `::` with `/`)

This provides the best balance of simplicity, readability, and compatibility.

## Implementation Plan

### Phase 1: Add Mapping Layer (No Breaking Changes)

**Files to modify:**
- `booktest/naming.py` - Add conversion functions
- `booktest/testcaserun.py` - Use display name for reporting, filesystem name internally
- `booktest/detection.py` - Generate pytest-style names
- `booktest/selection.py` - Accept both formats during transition

**New functions:**
```python
# booktest/naming.py

def to_pytest_name(module_path: str, class_name: str = None, method_name: str) -> str:
    """Convert to pytest-style name.

    Example:
        to_pytest_name("test.foo_test", "FooTestBook", "test_bar")
        → "test/foo_test.py::FooTestBook::test_bar"

        to_pytest_name("test.simple_test", method_name="test_example")
        → "test/simple_test.py::test_example"
    """
    path = module_path.replace(".", "/") + ".py"
    if class_name:
        return f"{path}::{class_name}::{method_name}"
    else:
        return f"{path}::{method_name}"

def to_filesystem_path(pytest_name: str) -> str:
    """Convert pytest name to safe filesystem path.

    Example:
        to_filesystem_path("test/foo_test.py::FooTestBook::test_bar")
        → "test/foo_test.py/FooTestBook/test_bar"
    """
    return pytest_name.replace("::", "/")

def from_filesystem_path(fs_path: str) -> str:
    """Convert filesystem path back to pytest name.

    Heuristic: If path contains '.py/', convert that to '.py::'
    Otherwise return as-is for backwards compatibility.
    """
    # Match pattern: {path}/{file}.py/{rest}
    import re
    match = re.match(r'(.*?\.py)/(.*)', fs_path)
    if match:
        return f"{match.group(1)}::{match.group(2).replace('/', '::')}"
    else:
        # Legacy format - return as-is
        return fs_path

def is_pytest_name(name: str) -> bool:
    """Check if name is pytest format."""
    return "::" in name
```

**TestCaseRun changes:**
```python
class TestCaseRun:
    def __init__(self, run, test_path, config, output):
        # test_path is now pytest format: "test/foo_test.py::test_bar"

        # For filesystem operations, use encoded path
        self.test_path = test_path  # Display name (pytest format)
        self.test_path_fs = to_filesystem_path(test_path)  # Filesystem name

        # Use test_path for display/reporting
        # Use test_path_fs for file operations
        relative_dir, name = path.split(self.test_path_fs)

        # ... rest of init uses test_path_fs for file operations
        self.out_file_name = path.join(self.out_base_dir, name + ".md")
        # etc.
```

### Phase 2: Update Detection (Generate New Format)

**detection.py changes:**
```python
def get_module_tests(test_suite_name, module_name):
    # OLD: test_cases.append((os.path.join(test_suite_name, clean_method_name(name)), member))

    # NEW: Generate pytest-style names
    module_path = module_name.replace(".", "/")
    for name in dir(module):
        member = getattr(module, name)
        if isinstance(member, types.FunctionType) and name.startswith("test_"):
            # Standalone function: test/foo_test.py::test_bar
            pytest_name = f"{module_path}.py::{name}"
            test_cases.append((pytest_name, member))
```

**TestBook changes:**
```python
class TestBook:
    def test_book_path(self):
        # Generate pytest-style name
        module = inspect.getmodule(type(self))
        module_path = module.__name__.replace(".", "/") + ".py"
        class_name = type(self).__name__

        if self.full_path:
            # Custom path specified - convert to pytest format
            # ...
        else:
            return f"{module_path}::{class_name}"

    def all_cases(self):
        for name in dir(self):
            method = getattr(self, name)
            if name.startswith("test_"):
                pytest_name = f"{self.test_book_path()}::{name}"
                yield (pytest_name, method)
```

### Phase 3: Migration Script

Create migration script to help users transition:

```python
#!/usr/bin/env python3
"""Migrate booktest filesystem from old to new naming convention."""

import os
import shutil
import json
from pathlib import Path
from booktest.naming import to_filesystem_path, from_filesystem_path

def migrate_directory(base_dir: str, dry_run: bool = True):
    """Migrate directory structure to new naming."""
    base_path = Path(base_dir)

    migrations = []

    # Find all test output files
    for old_path in base_path.rglob("*.md"):
        rel_path = old_path.relative_to(base_path)

        # Check if this looks like a test output file
        # Pattern: test/{path}/{name}.md
        if not str(rel_path).startswith("test/"):
            continue

        # Try to reconstruct pytest name
        # This is heuristic-based, may need manual review
        pytest_name = detect_pytest_name(str(rel_path))
        if pytest_name:
            new_fs_path = to_filesystem_path(pytest_name)
            new_path = base_path / new_fs_path

            migrations.append((old_path, new_path, pytest_name))

    # Show migration plan
    print(f"Found {len(migrations)} files to migrate")
    for old, new, name in migrations:
        print(f"  {old} → {new}")
        print(f"    (display name: {name})")

    if dry_run:
        print("\nDry run mode - no files were moved")
        print("Run with --execute to perform migration")
        return

    # Execute migration
    confirm = input("\nProceed with migration? [y/N] ")
    if confirm.lower() != 'y':
        print("Migration cancelled")
        return

    for old_path, new_path, name in migrations:
        # Move file
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(old_path, new_path)

        # Also move associated files (.bin, .txt, .log, dir)
        for suffix in [".bin", ".txt", ".log", ""]:
            old_file = old_path.with_suffix(suffix)
            if old_file.exists():
                new_file = new_path.with_suffix(suffix)
                shutil.move(old_file, new_file)

    print(f"\nMigrated {len(migrations)} test files")

def detect_pytest_name(rel_path: str) -> str:
    """Detect pytest name from old filesystem path.

    This is heuristic - may need manual adjustment.
    """
    # Remove .md extension
    path_no_ext = rel_path[:-3] if rel_path.endswith(".md") else rel_path

    # Pattern: test/foo/bar → test/foo_test.py::test_bar
    # This requires knowledge of original file structure
    # May need to scan actual .py files to determine correct mapping

    parts = path_no_ext.split("/")
    if len(parts) < 2:
        return None

    # Heuristic: assume test/module/method → test/module_test.py::test_method
    *module_parts, method = parts
    module_path = "/".join(module_parts)

    # Try to find corresponding .py file
    # ...

    return None  # Needs implementation based on actual file structure

def migrate_dvc_manifest(manifest_path: str, dry_run: bool = True):
    """Migrate DVC manifest keys to new naming."""
    import yaml

    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f) or {}

    storage_mode = manifest.pop("storage_mode", None)

    # Convert keys
    new_manifest = {}
    for old_key, value in manifest.items():
        # Detect pytest name for this key
        pytest_name = detect_pytest_name(old_key)
        if pytest_name:
            new_key = to_filesystem_path(pytest_name)
            new_manifest[new_key] = value
            print(f"  {old_key} → {new_key} (display: {pytest_name})")
        else:
            new_manifest[old_key] = value
            print(f"  {old_key} (unchanged - couldn't detect pytest name)")

    if storage_mode:
        new_manifest["storage_mode"] = storage_mode

    if dry_run:
        print("\nDry run - manifest not saved")
        return

    # Save
    with open(manifest_path, 'w') as f:
        yaml.safe_dump(new_manifest, f, default_flow_style=False, sort_keys=True)

    print(f"\nUpdated manifest: {manifest_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate booktest to pytest naming")
    parser.add_argument("--books-dir", default="books", help="Books directory")
    parser.add_argument("--manifest", default="booktest.manifest.yaml", help="DVC manifest")
    parser.add_argument("--execute", action="store_true", help="Actually perform migration")

    args = parser.parse_args()

    print("=== Booktest Naming Migration ===\n")

    print("Migrating output files...")
    migrate_directory(args.books_dir, dry_run=not args.execute)

    print("\nMigrating DVC manifest...")
    if os.path.exists(args.manifest):
        migrate_dvc_manifest(args.manifest, dry_run=not args.execute)
    else:
        print(f"  Manifest not found: {args.manifest}")
```

### Phase 4: Backwards Compatibility

During transition, support both formats:

```python
# booktest/selection.py

def normalize_test_name(name: str) -> str:
    """Normalize test name to internal format.

    Accepts:
    - New format: test/foo_test.py::test_bar
    - Old format: test/foo/bar

    Returns filesystem path.
    """
    if "::" in name:
        # New format
        return to_filesystem_path(name)
    else:
        # Old format - return as-is
        return name

def is_selected(case_name, selection):
    # Normalize both to filesystem format for comparison
    case_fs = normalize_test_name(case_name)

    if selection is None:
        return True

    for pattern in selection:
        pattern_fs = normalize_test_name(pattern)
        if case_fs.startswith(pattern_fs):
            return True

    return False
```

### Phase 5: Update Display/Reporting

**reports.py changes:**
```python
def report_case_result(printer, test_path, result, took_ms, snapshot_state_display=None):
    # test_path is now in pytest format
    # Display it directly
    printer(f"{test_path} {result} {took_ms} ms")
```

## Migration Path for Users

### Step 1: Update booktest (maintains backwards compatibility)
```bash
# Update to version with dual-format support
pip install --upgrade booktest

# Existing tests still work with old format
./do test test/foo/bar  # Still works
```

### Step 2: Run migration script (optional but recommended)
```bash
# Preview what would change
python -m booktest.migrate --books-dir books --manifest booktest.manifest.yaml

# Execute migration
python -m booktest.migrate --books-dir books --manifest booktest.manifest.yaml --execute

# Commit changes
git add books/ booktest.manifest.yaml
git commit -m "Migrate to pytest-style test naming"
```

### Step 3: Use new format in CLI
```bash
# New format works
./do test test/foo_test.py::test_bar

# Old format still works (maps internally)
./do test test/foo/bar  # Mapped to filesystem path

# Autocomplete works better with new format
./do test test/foo<TAB>  # Completes to test/foo_test.py
```

### Step 4: Update test discovery (automatic)
```bash
# New test runs generate pytest-style names automatically
./do test -s

# Output files created with new structure:
# books/test/foo_test.py/test_bar.md  (filesystem)
# Display: test/foo_test.py::test_bar  (CLI/reporting)
```

## Rollout Strategy

### Version N (Current)
- Only supports old format
- Example: `test/foo/bar`

### Version N+1 (Transition)
- Detection generates pytest format internally
- Filesystem mapping layer added
- CLI accepts both formats
- Display shows old format (for compatibility)
- Migration script available

### Version N+2 (Dual Display)
- Display shows new format by default
- Flag to show old format: `--legacy-names`
- Deprecation warnings for old format in CLI

### Version N+3 (New Default)
- New format is default
- Old format still supported for reading existing files
- Migration required for new test creation

### Version N+4 (Cleanup)
- Old format support removed from test creation
- Can still read old filesystem paths
- Full pytest compatibility

## Testing the Migration

### Test Scenarios

1. **New test on fresh install**
   - Create new test file
   - Run with `-s`
   - Verify pytest-style names in filesystem

2. **Existing test unchanged**
   - Don't run migration
   - Run existing tests
   - Should work without issues

3. **Migrated test**
   - Run migration script
   - Run tests
   - Verify old snapshots work
   - Create new snapshots

4. **Mixed environment**
   - Some tests migrated, some not
   - All should work
   - CLI accepts both formats

5. **DVC integration**
   - Migrate manifest
   - Run tests
   - Snapshots fetched correctly
   - New snapshots stored with new names

6. **Parallel execution**
   - Batch directories use new names
   - No conflicts
   - Manifest merge works

## Open Questions

1. **Class name in filesystem?**
   - Currently: Include class name in path
   - Alternative: Omit if class name matches file name
   - Recommendation: Always include for consistency

2. **Test_ prefix in method name?**
   - Currently: Strip `test_` prefix in old format
   - Proposed: Keep `test_` in pytest format
   - Recommendation: Keep it (matches pytest exactly)

3. **Migration timing?**
   - Force migration in major version?
   - Keep dual support indefinitely?
   - Recommendation: Deprecation path over 3-4 versions

4. **Backwards compatibility in DVC?**
   - Old manifest keys still work?
   - Transparent mapping?
   - Recommendation: Migration updates manifest, dual format support for 2-3 versions

## File Changes Summary

### New Files
- `booktest/migrate.py` - Migration script
- `docs/guides/pytest_naming_migration.md` - This document

### Modified Files
- `booktest/naming.py` - Add conversion functions
- `booktest/detection.py` - Generate pytest names
- `booktest/testcaserun.py` - Use dual naming (display + filesystem)
- `booktest/testbook.py` - Generate pytest names
- `booktest/selection.py` - Accept both formats
- `booktest/reports.py` - Display pytest names
- `booktest/storage.py` - Use filesystem names internally

### Minimal Changes
- Most code continues to work with filesystem paths internally
- Only entry/exit points (detection, display) need changes
- Storage layer agnostic to naming format

## Recommendation

**Proceed with Option A (Replace `::` with `/`)** using the phased migration approach:

1. Start with Phase 1 (add mapping layer) in next minor version
2. Provide migration script but keep it optional
3. Gradual transition over 3-4 versions
4. Maintain backwards compatibility throughout

This provides the best balance of:
- Improved UX (pytest compatibility)
- Minimal breaking changes
- Clear migration path
- Backwards compatibility

The key insight is that this is primarily a **naming convention change**, not a fundamental architectural change. The filesystem layer already uses paths; we're just changing how those paths are derived from test structure.