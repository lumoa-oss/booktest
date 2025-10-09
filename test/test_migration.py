"""
Test for filesystem migration from v1 (legacy) to v2 (pytest-style) naming.
"""
import os
import sys
import shutil
import tempfile
from pathlib import Path

import booktest as bt
from booktest.migrate import check_and_migrate, pytest_name_to_legacy_path
from booktest.config import set_fs_version, get_fs_version


class TestMigration(bt.TestBook):

    def test_legacy_to_pytest_migration(self, t: bt.TestCaseRun):
        """
        Test that migration correctly moves files from legacy naming to pytest-style naming.
        """
        t.h1("Migration Test Setup")

        # Create a temporary test environment
        tmpdir = Path(t.tmp_dir("test"))

        # Create test directory structure
        test_dir = tmpdir / "test"
        books_dir = tmpdir / "books"
        test_dir.mkdir(parents=True)
        books_dir.mkdir(parents=True)

        # Create config file with v1
        config_file = tmpdir / "booktest.ini"
        config_file.write_text("""
python_path=.
test_paths=test
books_path=books
fs_version=v1
""")

        t.tln(f"Created test environment at {tmpdir}")
        t.tln(f"Config file: {config_file}")

        # Create a simple test file
        test_file = test_dir / "migration_test.py"
        test_file.write_text('''
import booktest as bt

def test_hello(t: bt.TestCaseRun):
t.h1("Hello Test")
t.tln("This is a simple test")

@bt.snapshot_httpx()
def test_snapshot(t: bt.TestCaseRun):
t.h1("Snapshot Test")
t.tln("This test uses snapshots")
''')

        t.h1("Legacy Filesystem Structure")
        t.tln("Creating legacy v1 filesystem structure:")

        # Create legacy paths for the tests
        # test/migration_test.py::test_hello → test/migration/hello.md
        # test/migration_test.py::test_snapshot → test/migration/snapshot.md
        legacy_dir = books_dir / "test" / "migration"
        legacy_dir.mkdir(parents=True)

        # Create legacy .md files
        legacy_hello = legacy_dir / "hello.md"
        legacy_hello.write_text("""# Hello Test

This is a simple test
""")
        t.tln(f" - Created: books/test/migration/hello.md")

        legacy_snapshot = legacy_dir / "snapshot.md"
        legacy_snapshot.write_text("""# Snapshot Test

This test uses snapshots
""")
        t.tln(f" - Created: books/test/migration/snapshot.md")

        # Create legacy snapshot directory
        legacy_snapshot_dir = legacy_dir / "snapshot" / "_snapshots"
        legacy_snapshot_dir.mkdir(parents=True)
        metadata_file = legacy_snapshot_dir / "metadata.json"
        metadata_file.write_text('''{
"test_id": "test/migration/snapshot",
"snapshots": {
"httpx": {
  "hash": "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
  "state": "intact"
}
}
}''')
        t.tln(f" - Created: books/test/migration/snapshot/_snapshots/metadata.json")

        t.h1("Verify Legacy Structure")
        t.tln("Checking that legacy files exist:")
        t.tln(f" - hello.md exists: {legacy_hello.exists()}")
        t.tln(f" - snapshot.md exists: {legacy_snapshot.exists()}")
        t.tln(f" - snapshot/_snapshots exists: {legacy_snapshot_dir.exists()}")
        t.tln(f" - fs_version: {get_fs_version(str(config_file))}")

        # Read content before migration for comparison
        legacy_hello_content = legacy_hello.read_text()
        legacy_snapshot_content = legacy_snapshot.read_text()

        t.h1("Create Mock Tests Object")
        # Create a Tests object with mock test cases
        # We don't need actual test functions, just the names
        test_cases = [
            ("test/migration_test.py::test_hello", lambda: None),
            ("test/migration_test.py::test_snapshot", lambda: None),
        ]
        tests = bt.Tests(test_cases)

        t.tln(f"Created {len(tests.cases)} mock test(s):")
        for test_name, _ in tests.cases:
            legacy_path = pytest_name_to_legacy_path(test_name)
            new_path = test_name.replace("::", "/")
            t.tln(f" - {test_name}")
            t.tln(f"   Legacy: {legacy_path}")
            t.tln(f"   New: {new_path}")

        t.h1("Run Migration")
        # Change to temp directory
        old_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            t.tln("Running check_and_migrate()...")

            # Run migration
            result = check_and_migrate(
                base_dir="books",
                tests=tests,
                force=True
            )
        finally:
            os.chdir(old_cwd)

        t.tln(f"Migration completed: {result}")
        t.tln(f"fs_version after migration: {get_fs_version(str(config_file))}")

        t.h1("Verify New Structure")
        t.tln("Checking that new pytest-style files exist:")

        # New paths should be:
        # test/migration_test.py/test_hello.md
        # test/migration_test.py/test_snapshot.md
        new_test_dir = books_dir / "test" / "migration_test.py"
        new_hello = new_test_dir / "test_hello.md"
        new_snapshot = new_test_dir / "test_snapshot.md"
        new_snapshot_dir = new_test_dir / "test_snapshot" / "_snapshots"

        t.tln(f" - test_hello.md exists: {new_hello.exists()}")
        t.tln(f" - test_snapshot.md exists: {new_snapshot.exists()}")
        t.tln(f" - test_snapshot/_snapshots exists: {new_snapshot_dir.exists()}")

        if new_hello.exists():
            hello_content_match = new_hello.read_text() == legacy_hello_content
            t.tln(f" - test_hello.md content matches: {hello_content_match}")
        if new_snapshot.exists():
            snapshot_content_match = new_snapshot.read_text() == legacy_snapshot_content
            t.tln(f" - test_snapshot.md content matches: {snapshot_content_match}")

        t.h1("Verify Legacy Files Removed")
        t.tln("Checking that legacy files were moved (not copied):")
        t.tln(f" - legacy hello.md exists: {legacy_hello.exists()}")
        t.tln(f" - legacy snapshot.md exists: {legacy_snapshot.exists()}")
        t.tln(f" - legacy directory exists: {legacy_dir.exists()}")

        t.h1("Test Results")
        # Verify all assertions
        assert new_hello.exists(), "New hello.md file should exist"
        assert new_snapshot.exists(), "New snapshot.md file should exist"
        assert new_snapshot_dir.exists(), "New snapshot directory should exist"
        assert not legacy_hello.exists(), "Legacy hello.md should be moved (not exist)"
        assert not legacy_snapshot.exists(), "Legacy snapshot.md should be moved (not exist)"
        assert not legacy_dir.exists(), "Empty legacy directory should be cleaned up"
        assert get_fs_version(str(config_file)) == "v2", "fs_version should be updated to v2"

        t.tln("✓ All migration checks passed!")


    def test_pytest_name_conversion(self, t: bt.TestCaseRun):
        """
        Test the pytest_name_to_legacy_path conversion function.
        """
        t.h1("Testing pytest_name_to_legacy_path()")

        test_cases = [
            ("test/foo_test.py::test_bar", "test/foo/bar"),
            ("test/foo_test.py::FooBook/test_bar", "test/foo/bar"),
            ("test/examples/simple_book.py::test_hello", "test/examples/simple/hello"),
            ("test/migration_test.py::test_hello", "test/migration/hello"),
            ("test/migration_test.py::test_snapshot", "test/migration/snapshot"),
        ]

        t.tln("Testing conversions:")
        for pytest_name, expected_legacy in test_cases:
            actual = pytest_name_to_legacy_path(pytest_name)
            matches = actual == expected_legacy
            status = "✓" if matches else "✗"
            t.tln(f" {status} {pytest_name}")
            t.tln(f"   Expected: {expected_legacy}")
            t.tln(f"   Actual:   {actual}")

            assert matches, f"Conversion failed: {pytest_name} → {actual} (expected: {expected_legacy})"

        t.tln()
        t.tln("✓ All conversion tests passed!")
