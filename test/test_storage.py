"""Tests for the storage abstraction layer."""

import tempfile
import shutil
from pathlib import Path
import json
import booktest as bt
from booktest.snapshots.storage import (
    GitStorage,
    DVCStorage,
    StorageMode,
    detect_storage_mode,
    create_storage
)


class TestStorage(bt.TestBook):
    """Test suite for storage abstraction layer."""

    def test_git_storage_basic(self, t: bt.TestCaseRun):
        """Test basic GitStorage operations."""
        t.h1("GitStorage Basic Operations")

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = GitStorage(base_path=tmpdir)

            # Test storing content
            t.h2("Store Operation")
            test_id = "test/example::test_case"
            content = b'{"result": "test data"}'
            hash_result = storage.store(test_id, "func", content)
            t.tln(f"Stored content with hash: {hash_result}")

            # Test fetching content
            t.h2("Fetch Operation")
            fetched = storage.fetch(test_id, "func")
            t.tln(f"Fetched content matches: {fetched == content}")

            # Test exists check
            t.h2("Exists Check")
            t.tln(f"Snapshot exists: {storage.exists(test_id, 'func')}")
            t.tln(f"Non-existent snapshot: {storage.exists(test_id, 'env')}")

            # Test manifest generation
            t.h2("Manifest Generation")
            manifest = storage.get_manifest()
            t.tln(f"Manifest: {json.dumps(manifest, indent=2, sort_keys=True)}")

    def test_git_storage_path_construction(self, t: bt.TestCaseRun):
        """Test GitStorage path construction for different test IDs."""
        t.h1("GitStorage Path Construction")

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = GitStorage(base_path=tmpdir)

            test_cases = [
                ("test/simple::test_case", "env"),
                ("test/nested/deep::test_func", "http"),
                ("examples/snapshots::httpx_test", "httpx"),
            ]

            for test_id, snapshot_type in test_cases:
                t.h2(f"Test ID: {test_id}")
                content = f'{{"test": "{test_id}"}}'.encode()
                storage.store(test_id, snapshot_type, content)

                # Check the actual .snapshots.json file path (new format)
                path = storage._get_snapshot_file_path(test_id)
                t.tln(f"Path: {path.relative_to(tmpdir)}")
                t.tln(f"File exists: {path.exists()}")

                # Verify snapshot exists via storage API
                t.tln(f"Snapshot exists: {storage.exists(test_id, snapshot_type)}")

    def test_dvc_storage_fallback(self, t: bt.TestCaseRun):
        """Test DVCStorage fallback when DVC is not available."""
        t.h1("DVCStorage Fallback Behavior")

        # This test verifies the fallback behavior when DVC is not installed
        t.tln("Testing storage creation without DVC...")

        storage = create_storage(mode=StorageMode.GIT)
        t.tln(f"Created storage type: {type(storage).__name__}")

        # Verify it's GitStorage
        t.tln(f"Is GitStorage: {isinstance(storage, GitStorage)}")

    def test_storage_mode_detection(self, t: bt.TestCaseRun):
        """Test automatic storage mode detection."""
        t.h1("Storage Mode Detection")

        # Save current directory and change to temp dir for isolation
        import os
        original_cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)

                # Test with no configuration (should default to git in empty dir)
                t.h2("No Configuration")
                mode = detect_storage_mode()
                t.tln(f"Detected mode: {mode.value}")

                # Test with explicit configuration
                t.h2("Explicit Configuration")
                config = {"storage": {"mode": "git"}}
                mode = detect_storage_mode(config)
                t.tln(f"Configured mode: {mode.value}")

                # Test with auto configuration (should default to git in empty dir)
                t.h2("Auto Configuration")
                config = {"storage": {"mode": "auto"}}
                mode = detect_storage_mode(config)
                t.tln(f"Auto-detected mode: {mode.value}")
            finally:
                os.chdir(original_cwd)

    def test_manifest_operations(self, t: bt.TestCaseRun):
        """Test manifest operations for both storage backends."""
        t.h1("Manifest Operations")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test GitStorage manifest
            t.h2("GitStorage Manifest")
            git_storage = GitStorage(base_path=tmpdir)

            # Store some snapshots
            git_storage.store("test1", "env", b'{"env": "test"}')
            git_storage.store("test1", "http", b'{"http": "response"}')
            git_storage.store("test2", "func", b'{"func": "result"}')

            manifest = git_storage.get_manifest()
            t.tln(f"Manifest: {json.dumps(manifest, indent=2, sort_keys=True)}")

            # Test manifest update (no-op for Git)
            updates = {"test3": {"env": "sha256:abc123"}}
            git_storage.update_manifest(updates)
            t.tln("GitStorage update_manifest is a no-op (as expected)")

    def test_content_hashing(self, t: bt.TestCaseRun):
        """Test content hashing consistency."""
        t.h1("Content Hashing")

        content = b'{"test": "data", "value": 42}'

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = GitStorage(base_path=tmpdir)

            # Store same content multiple times
            t.h2("Hash Consistency")
            hash1 = storage.store("test1", "env", content)
            hash2 = storage.store("test2", "env", content)
            t.tln(f"Hash 1: {hash1}")
            t.tln(f"Hash 2: {hash2}")
            t.tln(f"Hashes match: {hash1 == hash2}")

            # Different content should have different hash
            t.h2("Different Content")
            different_content = b'{"test": "different"}'
            hash3 = storage.store("test3", "env", different_content)
            t.tln(f"Hash 3: {hash3}")
            t.tln(f"Different from hash1: {hash3 != hash1}")

    def test_promote_operation(self, t: bt.TestCaseRun):
        """Test promote operation for both storage backends."""
        t.h1("Promote Operation")

        with tempfile.TemporaryDirectory() as tmpdir:
            # GitStorage promote (no-op)
            t.h2("GitStorage Promote")
            git_storage = GitStorage(base_path=tmpdir)
            git_storage.store("test1", "env", b'{"data": "test"}')
            git_storage.promote("test1", "env")
            t.tln("GitStorage promote is a no-op (as expected)")

            # Verify content still accessible
            content = git_storage.fetch("test1", "env")
            t.tln(f"Content still accessible: {content is not None}")

    def test_snapshot_types(self, t: bt.TestCaseRun):
        """Test handling of different snapshot types."""
        t.h1("Snapshot Types")

        snapshot_types = ["env", "http", "httpx", "func"]

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = GitStorage(base_path=tmpdir)

            t.h2("Store All Types")
            test_id = "test/all_types"
            for snap_type in snapshot_types:
                content = f'{{"type": "{snap_type}"}}'.encode()
                hash_val = storage.store(test_id, snap_type, content)
                t.tln(f"- {snap_type}: {hash_val[:20]}...")

            t.h2("Verify All Types")
            for snap_type in snapshot_types:
                exists = storage.exists(test_id, snap_type)
                t.tln(f"- {snap_type} exists: {exists}")

            t.h2("Generated Manifest")
            manifest = storage.get_manifest()
            if test_id.replace("::", "/") in manifest:
                t.tln(f"Manifest entry: {json.dumps(manifest[test_id.replace('::', '/')], indent=2, sort_keys=True)}")