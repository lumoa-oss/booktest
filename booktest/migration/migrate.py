"""
Automatic migration from v1 (legacy) to v2 (pytest-style) filesystem layout.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import warnings

from booktest.config.config import get_fs_version, set_fs_version, PROJECT_CONFIG_FILE


def pytest_name_to_legacy_path(pytest_name: str) -> str:
    """
    Convert pytest-style name to legacy filesystem path.

    Examples:
        test/foo_test.py::test_bar → test/foo/bar
        test/foo_test.py::FooBook/test_bar → test/foo/class_name/bar
        test/examples/simple_book.py::test_hello → test/examples/simple/hello
    """
    # Import here to avoid circular dependency
    from booktest.config.naming import clean_test_postfix, clean_class_name, clean_method_name

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
    cleaned_file_name = clean_test_postfix(last_segment)

    file_part_segments[-1] = cleaned_file_name
    cleaned_file_path = "/".join(file_part_segments)

    if len(parts) == 2:
        # Could be standalone function or class method
        test_part = parts[1]

        # Check if it contains a class (has /)
        if "/" in test_part:
            # Class method: test/foo_test.py::FooBook/test_bar
            # Split on / to separate class from method
            class_method_parts = test_part.split("/")
            class_name = class_method_parts[0]  # First part before /
            method_name = class_method_parts[-1]  # Last part after /

            # Clean class name (convert CamelCase to snake_case and remove suffixes)
            cleaned_class_name = clean_class_name(class_name)

            # Check if class name is different from file name (excluding underscores)
            # This matches the logic in class_to_test_path
            if cleaned_file_name.replace("_", "") != cleaned_class_name.replace("_", ""):
                # Include class name in path
                path_parts = [cleaned_file_path, cleaned_class_name]
            else:
                # Class name same as file name, don't duplicate
                path_parts = [cleaned_file_path]

            # Clean method name (remove test_ prefix)
            cleaned_method = clean_method_name(method_name)
            if cleaned_method:
                path_parts.append(cleaned_method)
            else:
                path_parts.append(method_name)

            return "/".join(path_parts)
        else:
            # Standalone function: test/foo_test.py::test_bar
            method_name = test_part

            # Clean method name (remove test_ prefix)
            cleaned_method = clean_method_name(method_name)
            if cleaned_method:
                return f"{cleaned_file_path}/{cleaned_method}"
            else:
                return f"{cleaned_file_path}/{method_name}"

    else:
        # Fallback
        return pytest_name


def cleanup_empty_directories(base_path: Path, directories: set):
    """
    Remove empty directories after migration.
    Only removes directories if they contain no files or subdirectories.

    Args:
        base_path: Base directory (not removed even if empty)
        directories: Set of directories to check for cleanup
    """
    # Sort directories by depth (deepest first) to clean up from bottom to top
    sorted_dirs = sorted(directories, key=lambda d: len(d.parts), reverse=True)

    for directory in sorted_dirs:
        if not directory.exists():
            continue

        try:
            # Check if directory is empty (no files or subdirs)
            if not any(directory.iterdir()):
                directory.rmdir()
                print(f"Cleaned up empty directory: {directory.relative_to(base_path)}")

                # Also try to clean up parent directories if they're now empty
                parent = directory.parent
                while parent != base_path and parent.exists():
                    try:
                        if not any(parent.iterdir()):
                            parent.rmdir()
                            print(f"Cleaned up empty directory: {parent.relative_to(base_path)}")
                            parent = parent.parent
                        else:
                            break
                    except OSError:
                        break
        except OSError:
            # Directory not empty or cannot be removed
            pass


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
    legacy_dirs_to_cleanup = set()

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
                    # Track parent directory for cleanup
                    legacy_dirs_to_cleanup.add(old_file.parent)

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
                # Track parent directory for cleanup
                legacy_dirs_to_cleanup.add(old_dir.parent)

                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                print(f"Migrated directory: {old_dir.relative_to(base_path)} → {new_dir.relative_to(base_path)}")
                migrated_count += 1

    # Cleanup empty directories after migration
    if not dry_run and legacy_dirs_to_cleanup:
        cleanup_empty_directories(base_path, legacy_dirs_to_cleanup)

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
