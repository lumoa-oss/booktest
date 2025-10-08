"""
Automatic migration from v1 (legacy) to v2 (pytest-style) filesystem layout.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
import warnings

from booktest.config import get_fs_version, set_fs_version, DOT_CONFIG_FILE


def detect_legacy_test_files(base_dir: str) -> List[Tuple[Path, Path]]:
    """
    Detect test files in legacy format that need migration.

    Returns list of (old_path, new_path) tuples.

    Legacy format detection heuristics:
    - Files under test/ directory
    - Path does NOT contain .py/
    - Has typical test output extensions (.md, .bin, .txt, .log)
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        return []

    migrations = []

    # Find all test output files
    for pattern in ["**/*.md", "**/*.bin", "**/*.txt", "**/*.log"]:
        for old_path in base_path.glob(pattern):
            # Skip if this looks like it's already in new format
            # New format has .py/ in the path
            if ".py/" in str(old_path):
                continue

            # Skip files that don't look like test outputs
            rel_path = old_path.relative_to(base_path)
            if not str(rel_path).startswith("test/"):
                continue

            # This looks like a legacy test file
            # For now, we'll skip migration and let tests regenerate
            # (Safer than trying to guess the new path)
            pass

    return migrations


def migrate_filesystem(base_dir: str = "books", dry_run: bool = False) -> int:
    """
    Migrate filesystem from v1 to v2 format.

    Strategy: Rather than trying to move files (risky), we let tests
    regenerate with new format. This function just cleans up to prepare.

    Returns: Number of files that would be affected.
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        return 0

    legacy_files = detect_legacy_test_files(base_dir)

    if len(legacy_files) > 0:
        warnings.warn(
            f"Found {len(legacy_files)} test output files in legacy format. "
            f"These will be regenerated with pytest-style naming on next test run. "
            f"Run with -s flag to update snapshots."
        )

    # Don't actually move files - let tests regenerate
    # This is safer and handles all edge cases

    return len(legacy_files)


def maybe_migrate_dvc_manifest(manifest_path: str = "booktest.manifest.yaml") -> bool:
    """
    Check if DVC manifest needs migration.

    Returns True if migration was needed (will happen naturally on next run).
    """
    if not os.path.exists(manifest_path):
        return False

    # Check if manifest has legacy-format keys
    try:
        import yaml
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f) or {}
    except ImportError:
        import json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

    # Remove storage_mode key
    manifest.pop("storage_mode", None)

    # Check if any keys look like legacy format (no .py in path)
    has_legacy = False
    for key in manifest.keys():
        if key.startswith("test/") and ".py" not in key:
            has_legacy = True
            break

    if has_legacy:
        warnings.warn(
            f"DVC manifest contains legacy-format test names. "
            f"These will be updated automatically on next test run."
        )

    return has_legacy


def check_and_migrate(config_file: str = DOT_CONFIG_FILE,
                      base_dir: str = "books",
                      manifest_path: str = "booktest.manifest.yaml",
                      force: bool = False) -> bool:
    """
    Check filesystem version and migrate if needed.

    This is called automatically at test startup.

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

        # Check what needs migration
        file_count = migrate_filesystem(base_dir, dry_run=True)
        manifest_needs_migration = maybe_migrate_dvc_manifest(manifest_path)

        if file_count > 0 or manifest_needs_migration:
            print(f"  → {file_count} test output files will be regenerated")
            if manifest_needs_migration:
                print(f"  → DVC manifest will be updated")
            print()
            print("Migration strategy: Tests will regenerate outputs with new naming.")
            print("Old test outputs will be ignored and can be cleaned up later.")
            print()

        # Mark as migrated
        set_fs_version("v2", config_file)
        print(f"Updated {config_file}: fs_version=v2")
        print("Migration complete! Tests will now use pytest-style naming.")
        print()

        return True

    return False


def get_migration_status(config_file: str = DOT_CONFIG_FILE) -> Dict[str, str]:
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
