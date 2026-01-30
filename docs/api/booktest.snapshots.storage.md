<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.snapshots.storage`
Storage abstraction layer for booktest snapshots. 

This module provides a unified interface for storing and retrieving test snapshots, supporting both Git-based storage (current) and DVC/CAS storage (new). 


---

## <kbd>function</kbd> `detect_storage_mode`

```python
detect_storage_mode(
    config: Optional[Dict[str, Any]] = None
) → <enum 'StorageMode'>
```

Detect which storage mode to use based on configuration and environment. 



**Args:**
 
 - <b>`config`</b>:  Optional configuration dictionary 



**Returns:**
 Detected or configured storage mode 


---

## <kbd>function</kbd> `create_storage`

```python
create_storage(
    mode: Optional[StorageMode] = None,
    config: Optional[Dict[str, Any]] = None
) → SnapshotStorage
```

Create appropriate storage backend based on mode and configuration. 



**Args:**
 
 - <b>`mode`</b>:  Explicit storage mode to use (overrides auto-detection) 
 - <b>`config`</b>:  Configuration dictionary 



**Returns:**
 Storage backend instance 


---

## <kbd>class</kbd> `StorageMode`
Available storage backends for snapshots. 





---

## <kbd>class</kbd> `SnapshotStorage`
Abstract base class for snapshot storage backends. 




---

### <kbd>method</kbd> `exists`

```python
exists(test_id: str, snapshot_type: str) → bool
```

Check if a snapshot exists for the given test and type. 



**Args:**
 
 - <b>`test_id`</b>:  Unique identifier for the test 
 - <b>`snapshot_type`</b>:  Type of snapshot (env, http, httpx, func) 



**Returns:**
 True if snapshot exists, False otherwise 

---

### <kbd>method</kbd> `fetch`

```python
fetch(test_id: str, snapshot_type: str) → Optional[bytes]
```

Fetch snapshot content for a given test and type. 



**Args:**
 
 - <b>`test_id`</b>:  Unique identifier for the test 
 - <b>`snapshot_type`</b>:  Type of snapshot (env, http, httpx, func) 



**Returns:**
 Snapshot content as bytes, or None if not found 

---

### <kbd>method</kbd> `get_manifest`

```python
get_manifest() → Dict[str, Dict[str, str]]
```

Get the current manifest of all snapshots. 



**Returns:**
  Dictionary mapping test_id -> snapshot_type -> hash 

---

### <kbd>method</kbd> `promote`

```python
promote(test_id: str, snapshot_type: str = None) → bool
```

Promote a snapshot from staging to permanent storage. 



**Args:**
 
 - <b>`test_id`</b>:  Unique identifier for the test 
 - <b>`snapshot_type`</b>:  Type of snapshot (unused for unified format, kept for compatibility) 



**Returns:**
 True if snapshots were updated (content changed), False otherwise 

---

### <kbd>method</kbd> `store`

```python
store(test_id: str, snapshot_type: str, content: bytes) → str
```

Store snapshot content and return its hash. 



**Args:**
 
 - <b>`test_id`</b>:  Unique identifier for the test 
 - <b>`snapshot_type`</b>:  Type of snapshot (env, http, httpx, func) 
 - <b>`content`</b>:  Snapshot content to store 



**Returns:**
 SHA256 hash of the stored content 

---

### <kbd>method</kbd> `update_manifest`

```python
update_manifest(updates: Dict[str, Dict[str, str]]) → None
```

Update the manifest with new snapshot hashes. 



**Args:**
 
 - <b>`updates`</b>:  Dictionary mapping test_id -> snapshot_type -> hash 


---

## <kbd>class</kbd> `GitStorage`
Git-based storage implementation with unified snapshot files. 

New format: Stores all snapshots for a test in a single .snapshots.json file Legacy format: Supports reading from _snapshots/ subdirectories for backward compatibility 

### <kbd>method</kbd> `__init__`

```python
__init__(
    base_path: str = 'books',
    frozen_path: str = None,
    is_resource: bool = False
)
```

Initialize Git storage backend. 



**Args:**
 
 - <b>`base_path`</b>:  Base directory for storing snapshots (usually books/.out) 
 - <b>`frozen_path`</b>:  Directory for reading frozen snapshots (usually books, defaults to base_path) 
 - <b>`is_resource`</b>:  Whether to use Pants resource system for reading (default: False) 




---

### <kbd>method</kbd> `exists`

```python
exists(test_id: str, snapshot_type: str) → bool
```

Check if snapshot exists in Git repository. 

Checks both base_path and frozen_path, and both new and legacy formats. Uses Pants-compatible file operations when is_resource=True. 

---

### <kbd>method</kbd> `fetch`

```python
fetch(test_id: str, snapshot_type: str) → Optional[bytes]
```

Fetch snapshot content from Git repository. 

Tries new .snapshots.json format first, then falls back to legacy _snapshots/ directory. Uses Pants-compatible file operations when is_resource=True. 

---

### <kbd>method</kbd> `get_manifest`

```python
get_manifest() → Dict[str, Dict[str, str]]
```

For Git storage, generate manifest by scanning snapshot files. 

Scans both new .snapshots.json files and legacy _snapshots/ directories. 

---

### <kbd>method</kbd> `promote`

```python
promote(test_id: str, snapshot_type: str = None) → bool
```

Promote snapshot file from base_path (.out/) to frozen_path (books/). 

This implements the same semantics as DVC storage: on test success, snapshots are copied from the working directory to the permanent location. 

Note: We copy rather than move to keep snapshots in .out/ for review mode. 

Also performs automatic cleanup: when promoting .snapshots.json for the first time, removes legacy _snapshots/ directory if it exists. 



**Args:**
 
 - <b>`test_id`</b>:  Test identifier 
 - <b>`snapshot_type`</b>:  Unused, kept for API compatibility 



**Returns:**
 True if snapshots were updated (file changed), False otherwise 

---

### <kbd>method</kbd> `store`

```python
store(test_id: str, snapshot_type: str, content: bytes) → str
```

Store snapshot content in unified .snapshots.json file. 

Uses atomic write with temporary file to prevent corruption. 

---

### <kbd>method</kbd> `update_manifest`

```python
update_manifest(updates: Dict[str, Dict[str, str]]) → None
```

For Git storage, this is a no-op since files are stored directly. Manifest is implicit in the file system. 


---

## <kbd>class</kbd> `DVCStorage`
DVC-based content-addressable storage implementation. Stores snapshots in remote CAS with manifest tracking in Git. 

### <kbd>method</kbd> `__init__`

```python
__init__(
    base_path: str = 'books',
    remote: str = 'booktest-remote',
    manifest_path: str = 'booktest.manifest.yaml',
    batch_dir: str = None
)
```

Initialize DVC storage backend. 



**Args:**
 
 - <b>`base_path`</b>:  Base directory for local cache 
 - <b>`remote`</b>:  DVC remote name 
 - <b>`manifest_path`</b>:  Path to manifest file 
 - <b>`batch_dir`</b>:  Optional batch directory for parallel test runs 




---

### <kbd>method</kbd> `exists`

```python
exists(test_id: str, snapshot_type: str) → bool
```

Check if snapshot exists in manifest. 

---

### <kbd>method</kbd> `fetch`

```python
fetch(test_id: str, snapshot_type: str) → Optional[bytes]
```

Fetch snapshot content from DVC storage. 

---

### <kbd>method</kbd> `get_manifest`

```python
get_manifest() → Dict[str, Dict[str, str]]
```

Get current manifest. 

---

### <kbd>classmethod</kbd> `is_available`

```python
is_available() → bool
```

Check if DVC is installed and available. 

---

### <kbd>method</kbd> `merge_batch_manifests`

```python
merge_batch_manifests(manifest_path: str, batch_dirs: list) → None
```

Merge manifest updates from parallel batch runs into main manifest. 



**Args:**
 
 - <b>`manifest_path`</b>:  Path to main manifest file 
 - <b>`batch_dirs`</b>:  List of batch directory paths 

---

### <kbd>method</kbd> `promote`

```python
promote(test_id: str, snapshot_type: str = None) → bool
```

Promote snapshots from staging to permanent storage. 



**Args:**
 
 - <b>`test_id`</b>:  Test identifier 
 - <b>`snapshot_type`</b>:  Type of snapshot. If None, promotes all types for this test. 



**Returns:**
 True if any snapshots were promoted (moved to cache), False otherwise 

---

### <kbd>method</kbd> `store`

```python
store(test_id: str, snapshot_type: str, content: bytes) → str
```

Store snapshot content in staging area atomically and update manifest. 

---

### <kbd>method</kbd> `update_manifest`

```python
update_manifest(updates: Dict[str, Dict[str, str]]) → None
```

Update manifest with new hashes. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
