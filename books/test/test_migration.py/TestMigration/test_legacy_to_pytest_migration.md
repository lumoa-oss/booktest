# Migration Test Setup

Created test environment at books/.out/test/test_migration.py/TestMigration/test_legacy_to_pytest_migration.tmp/test
Config file: books/.out/test/test_migration.py/TestMigration/test_legacy_to_pytest_migration.tmp/test/booktest.ini

# Legacy Filesystem Structure

Creating legacy v1 filesystem structure:
 - Created: books/test/migration/hello.md
 - Created: books/test/migration/snapshot.md
 - Created: books/test/migration/snapshot/_snapshots/metadata.json

# Verify Legacy Structure

Checking that legacy files exist:
 - hello.md exists: True
 - snapshot.md exists: True
 - snapshot/_snapshots exists: True
 - fs_version: v1

# Create Mock Tests Object

Created 2 mock test(s):
 - test/migration_test.py::test_hello
   Legacy: test/migration/hello
   New: test/migration_test.py/test_hello
 - test/migration_test.py::test_snapshot
   Legacy: test/migration/snapshot
   New: test/migration_test.py/test_snapshot

# Run Migration

Running check_and_migrate()...
Migration completed: True
fs_version after migration: v2

# Verify New Structure

Checking that new pytest-style files exist:
 - test_hello.md exists: True
 - test_snapshot.md exists: True
 - test_snapshot/_snapshots exists: True
 - test_hello.md content matches: True
 - test_snapshot.md content matches: True

# Verify Legacy Files Removed

Checking that legacy files were moved (not copied):
 - legacy hello.md exists: False
 - legacy snapshot.md exists: False
 - legacy directory exists: False

# Test Results

✓ All migration checks passed!
