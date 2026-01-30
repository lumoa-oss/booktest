<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.migration.migrate`
Automatic migration from v1 (legacy) to v2 (pytest-style) filesystem layout. 

**Global Variables**
---------------
- **PROJECT_CONFIG_FILE**

---

## <kbd>function</kbd> `pytest_name_to_legacy_path`

```python
pytest_name_to_legacy_path(pytest_name: str) → str
```

Convert pytest-style name to legacy filesystem path. 



**Examples:**
  test/foo_test.py::test_bar → test/foo/bar  test/foo_test.py::FooBook/test_bar → test/foo/class_name/bar  test/examples/simple_book.py::test_hello → test/examples/simple/hello 


---

## <kbd>function</kbd> `cleanup_empty_directories`

```python
cleanup_empty_directories(base_path: Path, directories: set)
```

Remove empty directories after migration. Only removes directories if they contain no files or subdirectories. 



**Args:**
 
 - <b>`base_path`</b>:  Base directory (not removed even if empty) 
 - <b>`directories`</b>:  Set of directories to check for cleanup 


---

## <kbd>function</kbd> `migrate_test_files`

```python
migrate_test_files(tests, base_dir: str = 'books', dry_run: bool = False) → int
```

Migrate test output files from legacy to pytest-style paths. 

Uses actual test discovery to know what files to migrate where. 

Returns: Number of files migrated. 


---

## <kbd>function</kbd> `migrate_dvc_manifest_keys`

```python
migrate_dvc_manifest_keys(
    manifest_path: str = 'booktest.manifest.yaml',
    tests=None,
    dry_run: bool = False
) → int
```

Migrate DVC manifest keys from legacy to pytest-style format. 

Returns: Number of keys migrated. 


---

## <kbd>function</kbd> `check_and_migrate`

```python
check_and_migrate(
    config_file: str = 'booktest.ini',
    base_dir: str = 'books',
    manifest_path: str = 'booktest.manifest.yaml',
    tests=None,
    force: bool = False
) → bool
```

Check filesystem version and migrate if needed. 

This is called automatically at test startup. Uses booktest.ini (project config) for fs_version tracking. 



**Args:**
 
 - <b>`config_file`</b>:  Path to config file (default: booktest.ini) 
 - <b>`base_dir`</b>:  Base directory for test outputs (default: books) 
 - <b>`manifest_path`</b>:  Path to DVC manifest 
 - <b>`tests`</b>:  Tests object with discovered tests (needed for migration) 
 - <b>`force`</b>:  Force migration even if already on v2 

Returns: True if migration was performed or scheduled. 


---

## <kbd>function</kbd> `get_migration_status`

```python
get_migration_status(config_file: str = 'booktest.ini') → Dict[str, str]
```

Get current migration status information. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
