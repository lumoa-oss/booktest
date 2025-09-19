"""
Storage abstraction layer for booktest snapshots.

This module provides a unified interface for storing and retrieving test snapshots,
supporting both Git-based storage (current) and DVC/CAS storage (new).
"""

import os
import json
import hashlib
import shutil
import subprocess
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Any, Union


class StorageMode(Enum):
    """Available storage backends for snapshots."""
    GIT = "git"
    DVC = "dvc"
    AUTO = "auto"


class SnapshotStorage(ABC):
    """Abstract base class for snapshot storage backends."""

    @abstractmethod
    def fetch(self, test_id: str, snapshot_type: str) -> Optional[bytes]:
        """
        Fetch snapshot content for a given test and type.

        Args:
            test_id: Unique identifier for the test
            snapshot_type: Type of snapshot (env, http, httpx, func)

        Returns:
            Snapshot content as bytes, or None if not found
        """
        pass

    @abstractmethod
    def store(self, test_id: str, snapshot_type: str, content: bytes) -> str:
        """
        Store snapshot content and return its hash.

        Args:
            test_id: Unique identifier for the test
            snapshot_type: Type of snapshot (env, http, httpx, func)
            content: Snapshot content to store

        Returns:
            SHA256 hash of the stored content
        """
        pass

    @abstractmethod
    def exists(self, test_id: str, snapshot_type: str) -> bool:
        """
        Check if a snapshot exists for the given test and type.

        Args:
            test_id: Unique identifier for the test
            snapshot_type: Type of snapshot (env, http, httpx, func)

        Returns:
            True if snapshot exists, False otherwise
        """
        pass

    @abstractmethod
    def get_manifest(self) -> Dict[str, Dict[str, str]]:
        """
        Get the current manifest of all snapshots.

        Returns:
            Dictionary mapping test_id -> snapshot_type -> hash
        """
        pass

    @abstractmethod
    def update_manifest(self, updates: Dict[str, Dict[str, str]]) -> None:
        """
        Update the manifest with new snapshot hashes.

        Args:
            updates: Dictionary mapping test_id -> snapshot_type -> hash
        """
        pass

    @abstractmethod
    def promote(self, test_id: str, snapshot_type: str) -> None:
        """
        Promote a snapshot from staging to permanent storage.

        Args:
            test_id: Unique identifier for the test
            snapshot_type: Type of snapshot (env, http, httpx, func)
        """
        pass


class GitStorage(SnapshotStorage):
    """
    Traditional Git-based storage implementation.
    Stores snapshots directly in the repository under _snapshots directories.
    """

    def __init__(self, base_path: str = "books"):
        """
        Initialize Git storage backend.

        Args:
            base_path: Base directory for storing snapshots
        """
        self.base_path = Path(base_path)

    def _get_snapshot_path(self, test_id: str, snapshot_type: str) -> Path:
        """Construct the file path for a snapshot."""
        # Convert test_id like "test/examples/snapshots::httpx" to path
        parts = test_id.replace("::", "/").split("/")
        snapshot_dir = self.base_path / "/".join(parts) / "_snapshots"
        return snapshot_dir / f"{snapshot_type}.json"

    def fetch(self, test_id: str, snapshot_type: str) -> Optional[bytes]:
        """Fetch snapshot content from Git repository."""
        path = self._get_snapshot_path(test_id, snapshot_type)
        if path.exists():
            return path.read_bytes()
        return None

    def store(self, test_id: str, snapshot_type: str, content: bytes) -> str:
        """Store snapshot content in Git repository."""
        path = self._get_snapshot_path(test_id, snapshot_type)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

        # Calculate and return SHA256 hash
        hash_obj = hashlib.sha256(content)
        return f"sha256:{hash_obj.hexdigest()}"

    def exists(self, test_id: str, snapshot_type: str) -> bool:
        """Check if snapshot exists in Git repository."""
        path = self._get_snapshot_path(test_id, snapshot_type)
        return path.exists()

    def get_manifest(self) -> Dict[str, Dict[str, str]]:
        """
        For Git storage, generate manifest by scanning snapshot files.
        This is mainly for compatibility with the abstract interface.
        """
        manifest = {}
        if not self.base_path.exists():
            return manifest

        for snapshot_file in self.base_path.glob("**/_snapshots/*.json"):
            # Extract test_id and snapshot_type from path
            relative_path = snapshot_file.relative_to(self.base_path)
            parts = relative_path.parts[:-2]  # Remove _snapshots/file.json
            test_id = "/".join(parts)
            snapshot_type = snapshot_file.stem

            # Calculate hash of current content
            content = snapshot_file.read_bytes()
            hash_obj = hashlib.sha256(content)
            hash_str = f"sha256:{hash_obj.hexdigest()}"

            if test_id not in manifest:
                manifest[test_id] = {}
            manifest[test_id][snapshot_type] = hash_str

        return manifest

    def update_manifest(self, updates: Dict[str, Dict[str, str]]) -> None:
        """
        For Git storage, this is a no-op since files are stored directly.
        Manifest is implicit in the file system.
        """
        pass

    def promote(self, test_id: str, snapshot_type: str) -> None:
        """
        For Git storage, promotion is a no-op since everything is committed.
        """
        pass


class DVCStorage(SnapshotStorage):
    """
    DVC-based content-addressable storage implementation.
    Stores snapshots in remote CAS with manifest tracking in Git.
    """

    def __init__(self, base_path: str = "books",
                 remote: str = "booktest-remote",
                 manifest_path: str = "booktest.manifest.yaml"):
        """
        Initialize DVC storage backend.

        Args:
            base_path: Base directory for local cache
            remote: DVC remote name
            manifest_path: Path to manifest file
        """
        self.base_path = Path(base_path)
        self.cache_dir = Path(".booktest_cache")
        self.manifest_path = Path(manifest_path)
        self.remote = remote
        self.staging_dir = self.cache_dir / "staging"
        self.staging_dir.mkdir(parents=True, exist_ok=True)

        # Check if DVC is available
        self._check_dvc_available()

    def _check_dvc_available(self) -> bool:
        """Check if DVC is installed and configured."""
        try:
            result = subprocess.run(
                ["dvc", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _compute_hash(self, content: bytes) -> str:
        """Compute SHA256 hash of content."""
        hash_obj = hashlib.sha256(content)
        return f"sha256:{hash_obj.hexdigest()}"

    def _get_cas_path(self, hash_str: str, snapshot_type: str) -> Path:
        """Construct CAS path from hash and type."""
        # Remove "sha256:" prefix
        hash_hex = hash_str.replace("sha256:", "")
        # Use first 2 chars for sharding
        shard = hash_hex[:2]
        return Path(snapshot_type) / "sha256" / shard / hash_hex

    def _load_manifest(self) -> Dict[str, Dict[str, str]]:
        """Load manifest from YAML file."""
        if not self.manifest_path.exists():
            return {}

        try:
            import yaml
            with open(self.manifest_path, 'r') as f:
                data = yaml.safe_load(f) or {}
                # Skip storage_mode key if present
                if "storage_mode" in data:
                    del data["storage_mode"]
                return data
        except ImportError:
            # Fall back to JSON if PyYAML not available
            import json
            with open(self.manifest_path, 'r') as f:
                data = json.load(f)
                if "storage_mode" in data:
                    del data["storage_mode"]
                return data

    def _save_manifest(self, manifest: Dict[str, Dict[str, str]]) -> None:
        """Save manifest to YAML file."""
        try:
            import yaml
            data = {"storage_mode": "dvc"}
            data.update(manifest)
            with open(self.manifest_path, 'w') as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=True)
        except ImportError:
            # Fall back to JSON if PyYAML not available
            import json
            data = {"storage_mode": "dvc"}
            data.update(manifest)
            with open(self.manifest_path, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)

    def fetch(self, test_id: str, snapshot_type: str) -> Optional[bytes]:
        """Fetch snapshot content from DVC storage."""
        manifest = self._load_manifest()

        if test_id not in manifest or snapshot_type not in manifest[test_id]:
            return None

        hash_str = manifest[test_id][snapshot_type]
        cas_path = self._get_cas_path(hash_str, snapshot_type)

        # Check local cache first
        local_path = self.cache_dir / cas_path
        if local_path.exists():
            return local_path.read_bytes()

        # Try to pull from DVC remote
        try:
            subprocess.run(
                ["dvc", "pull", str(cas_path)],
                cwd=self.cache_dir,
                capture_output=True,
                check=True,
                timeout=30
            )
            if local_path.exists():
                return local_path.read_bytes()
        except subprocess.SubprocessError:
            warnings.warn(f"Failed to fetch {test_id}:{snapshot_type} from DVC")

        return None

    def store(self, test_id: str, snapshot_type: str, content: bytes) -> str:
        """Store snapshot content in staging area."""
        hash_str = self._compute_hash(content)
        cas_path = self._get_cas_path(hash_str, snapshot_type)

        # Store in staging area
        staging_path = self.staging_dir / cas_path
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        staging_path.write_bytes(content)

        return hash_str

    def exists(self, test_id: str, snapshot_type: str) -> bool:
        """Check if snapshot exists in manifest."""
        manifest = self._load_manifest()
        return test_id in manifest and snapshot_type in manifest[test_id]

    def get_manifest(self) -> Dict[str, Dict[str, str]]:
        """Get current manifest."""
        return self._load_manifest()

    def update_manifest(self, updates: Dict[str, Dict[str, str]]) -> None:
        """Update manifest with new hashes."""
        manifest = self._load_manifest()

        for test_id, snapshots in updates.items():
            if test_id not in manifest:
                manifest[test_id] = {}
            manifest[test_id].update(snapshots)

        self._save_manifest(manifest)

    def promote(self, test_id: str, snapshot_type: str) -> None:
        """Promote snapshot from staging to permanent storage."""
        manifest = self._load_manifest()

        if test_id not in manifest or snapshot_type not in manifest[test_id]:
            return

        hash_str = manifest[test_id][snapshot_type]
        cas_path = self._get_cas_path(hash_str, snapshot_type)

        staging_path = self.staging_dir / cas_path
        if not staging_path.exists():
            return

        # Move from staging to cache
        cache_path = self.cache_dir / cas_path
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staging_path), str(cache_path))

        # Push to DVC remote
        try:
            subprocess.run(
                ["dvc", "push", str(cas_path)],
                cwd=self.cache_dir,
                capture_output=True,
                check=True,
                timeout=30
            )
        except subprocess.SubprocessError:
            warnings.warn(f"Failed to push {test_id}:{snapshot_type} to DVC")


def detect_storage_mode(config: Optional[Dict[str, Any]] = None) -> StorageMode:
    """
    Detect which storage mode to use based on configuration and environment.

    Args:
        config: Optional configuration dictionary

    Returns:
        Detected or configured storage mode
    """
    # Check explicit configuration first
    if config and "storage" in config:
        mode = config["storage"].get("mode", "auto")
        if mode != "auto":
            try:
                return StorageMode(mode)
            except ValueError:
                warnings.warn(f"Invalid storage mode: {mode}, falling back to auto")

    # Auto-detect based on environment
    # Check for DVC
    try:
        result = subprocess.run(
            ["dvc", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        has_dvc = result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        has_dvc = False

    # Check for .dvc directory or dvc.yaml
    has_dvc_project = Path(".dvc").exists() or Path("dvc.yaml").exists()

    # Check for manifest file
    has_manifest = Path("booktest.manifest.yaml").exists()

    if has_dvc and (has_dvc_project or has_manifest):
        return StorageMode.DVC

    if has_dvc_project and not has_dvc:
        warnings.warn(
            "DVC project detected but DVC is not installed. "
            "Falling back to Git storage. Install DVC for better performance."
        )

    return StorageMode.GIT


def create_storage(mode: Optional[StorageMode] = None,
                  config: Optional[Dict[str, Any]] = None) -> SnapshotStorage:
    """
    Create appropriate storage backend based on mode and configuration.

    Args:
        mode: Explicit storage mode to use (overrides auto-detection)
        config: Configuration dictionary

    Returns:
        Storage backend instance
    """
    if mode is None:
        mode = detect_storage_mode(config)

    if mode == StorageMode.AUTO:
        mode = detect_storage_mode(config)

    if mode == StorageMode.DVC:
        # Check if DVC is actually available
        dvc_storage = DVCStorage()
        if not dvc_storage._check_dvc_available():
            warnings.warn(
                "DVC storage requested but DVC is not available. "
                "Falling back to Git storage."
            )
            return GitStorage()
        return dvc_storage

    # Default to Git storage
    return GitStorage()