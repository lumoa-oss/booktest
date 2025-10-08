"""
Automatic migration from v1 (legacy) to v2 (pytest-style) filesystem layout.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import warnings

from booktest.config import get_fs_version, set_fs_version, PROJECT_CONFIG_FILE


def pytest_name_to_legacy_path(pytest_name: str) -> str:
    """
    Convert pytest-style name to legacy filesystem path.

    Examples:
        test/foo_test.py::test_bar → test/foo/bar
        test/foo_test.py::FooBook/test_bar → test/foo/bar
        test/examples/simple_book.py::test_hello → test/examples/simple/hello
    """
    # Remove .py extension and split on ::
    if "::" not in pytest_name:
        # Not pytest format, return as-is
        return pytest_name

    # Split file path and test path
    parts = pytest_name.split("::")
    file_part = parts[0].replace(".py", "")

    # Clean file name: remove _test, _book, _suite suffixes
    file_part_segments = file_part.split("/")
    last_segment = file_part_segments[-1]

    # Remove common suffixes
    for suffix in ["_test", "_book", "_suite"]:
        if last_segment.endswith(suffix):
            last_segment = last_segment[:-len(suffix)]
            break

    file_part_segments[-1] = last_segment
    cleaned_file_path = "/".join(file_part_segments)

    if len(parts) == 2:
        # Standalone function: test/foo_test.py::test_bar
        method_name = parts[1]
        # Remove test_ prefix
        if method_name.startswith("test_"):
            method_name = method_name[5:]  # Remove "test_"

        return f"{cleaned_file_path}/{method_name}"

    elif len(parts) == 3:
        # Class method: test/foo_test.py::FooBook/test_bar
        # Last part is the method name
        method_name = parts[-1]
        if method_name.startswith("test_"):
            method_name = method_name[5:]

        return f"{cleaned_file_path}/{method_name}"

    else:
        # Fallback
        return pytest_name


def migrate_test_files(tests, base_dir: str = "books", dry_run: bool = False) -> int:
    """
    Migrate test output files from legacy to pytest-style paths.

    Uses actual test discovery to know what files to migrate where.

    Returns: Number of files migrated.
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        return 0

    migrated_count = 0

    # Get all test cases
    for test_name, test_method in tests.cases:
        # Convert pytest name to legacy path
        legacy_path = pytest_name_to_legacy_path(test_name)

        # Skip if same (shouldn't happen but be safe)
        # Convert :: to / for filesystem comparison
        new_path = test_name.replace("::", "/")
        if legacy_path == new_path:
            continue

        # Check for files at legacy location
        for ext in [".md", ".bin", ".txt", ".log"]:
            old_file = base_path / f"{legacy_path}{ext}"
            new_file = base_path / f"{new_path}{ext}"

            if old_file.exists():
                if dry_run:
                    print(f"Would migrate: {old_file} → {new_file}")
                    migrated_count += 1
                else:
                    # Create parent directory
                    new_file.parent.mkdir(parents=True, exist_ok=True)

                    # Move file
                    shutil.move(str(old_file), str(new_file))
                    print(f"Migrated: {old_file.relative_to(base_path)} → {new_file.relative_to(base_path)}")
                    migrated_count += 1

        # Also migrate associated directory if it exists
        old_dir = base_path / legacy_path
        new_dir = base_path / new_path

        if old_dir.is_dir() and not new_dir.exists():
            if dry_run:
                print(f"Would migrate directory: {old_dir} → {new_dir}")
                migrated_count += 1
            else:
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                print(f"Migrated directory: {old_dir.relative_to(base_path)} → {new_dir.relative_to(base_path)}")
                migrated_count += 1

    return migrated_count


def migrate_dvc_manifest_keys(manifest_path: str = "booktest.manifest.yaml",
                               tests=None,
                               dry_run: bool = False) -> int:
    """
    Migrate DVC manifest keys from legacy to pytest-style format.

    Returns: Number of keys migrated.
    """
    if not os.path.exists(manifest_path):
        return 0

    if tests is None:
        # Can't migrate without knowing test structure
        return 0

    # Build mapping from legacy paths to new paths
    legacy_to_new = {}
    for test_name, test_method in tests.cases:
        legacy_path = pytest_name_to_legacy_path(test_name)
        new_path = test_name.replace("::", "/")
        if legacy_path != new_path:
            legacy_to_new[legacy_path] = new_path

    # Load manifest
    try:
        import yaml
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f) or {}
    except ImportError:
        import json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

    # Extract storage_mode
    storage_mode = manifest.pop("storage_mode", "dvc")

    # Migrate keys
    new_manifest = {}
    migrated_count = 0

    for old_key, value in manifest.items():
        if old_key in legacy_to_new:
            new_key = legacy_to_new[old_key]
            new_manifest[new_key] = value
            if not dry_run:
                print(f"Migrated manifest key: {old_key} → {new_key}")
            migrated_count += 1
        else:
            # Keep unchanged
            new_manifest[old_key] = value

    if migrated_count > 0 and not dry_run:
        # Save updated manifest
        new_manifest["storage_mode"] = storage_mode

        try:
            import yaml
            with open(manifest_path, 'w') as f:
                yaml.safe_dump(new_manifest, f, default_flow_style=False, sort_keys=True)
        except ImportError:
            import json
            with open(manifest_path, 'w') as f:
                json.dump(new_manifest, f, indent=2, sort_keys=True)

    return migrated_count


def check_and_migrate(config_file: str = PROJECT_CONFIG_FILE,
                      base_dir: str = "books",
                      manifest_path: str = "booktest.manifest.yaml",
                      tests=None,
                      force: bool = False) -> bool:
    """
    Check filesystem version and migrate if needed.

    This is called automatically at test startup.
    Uses booktest.ini (project config) for fs_version tracking.

    Args:
        config_file: Path to config file (default: booktest.ini)
        base_dir: Base directory for test outputs (default: books)
        manifest_path: Path to DVC manifest
        tests: Tests object with discovered tests (needed for migration)
        force: Force migration even if already on v2

    Returns: True if migration was performed or scheduled.
    """
    current_version = get_fs_version(config_file)

    if current_version == "v2" and not force:
        # Already on v2, nothing to do
        return False

    if current_version == "v1" or force:
        # Need to migrate
        print("Detected legacy filesystem layout (v1)")
        print("Migrating to pytest-style naming (v2)...")
        print()

        if tests is None:
            # Can't do actual migration without test discovery
            # Just mark as migrated and let tests regenerate
            print("⚠️  Test discovery not available - files will regenerate on next run")
            print()
        else:
            # Perform actual migration
            print("Migrating test output files...")
            file_count = migrate_test_files(tests, base_dir, dry_run=False)

            if file_count > 0:
                print(f"✓ Migrated {file_count} files")
            else:
                print("✓ No legacy files found")
            print()

            # Migrate DVC manifest
            print("Migrating DVC manifest keys...")
            manifest_count = migrate_dvc_manifest_keys(manifest_path, tests, dry_run=False)

            if manifest_count > 0:
                print(f"✓ Migrated {manifest_count} manifest keys")
            else:
                print("✓ No legacy manifest keys found")
            print()

        # Mark as migrated
        set_fs_version("v2", config_file)
        print(f"✓ Updated {config_file}: fs_version=v2")
        print()
        print("Migration complete! Tests now use pytest-style naming.")
        print()

        return True

    return False


def get_migration_status(config_file: str = PROJECT_CONFIG_FILE) -> Dict[str, str]:
    """
    Get current migration status information.
    """
    current_version = get_fs_version(config_file)

    status = {
        "fs_version": current_version,
        "config_file": config_file,
        "needs_migration": current_version == "v1"
    }

    return status
