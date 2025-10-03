# Testing DVC Storage Locally

This guide shows how to test booktest's DVC storage backend locally.

## Prerequisites

1. **Install DVC**
   ```bash
   pip install dvc
   # or
   poetry add dvc --group dev
   ```

2. **Verify DVC installation**
   ```bash
   dvc --version
   ```

## Setup Steps

### 1. Initialize DVC in your project

```bash
cd /home/arau/lumoa/src/booktest
dvc init
```

This creates a `.dvc` directory and `dvc.yaml` file.

### 2. Configure a local DVC remote

Create a local directory to act as your DVC remote storage:

```bash
# Create a local storage directory (outside your project)
mkdir -p /tmp/booktest-dvc-storage

# Configure DVC to use this local directory
dvc remote add -d booktest-remote /tmp/booktest-dvc-storage
```

This configures DVC to use `/tmp/booktest-dvc-storage` as the default remote.

### 3. Enable DVC storage in booktest

Create or update `.booktest` configuration file:

```ini
[storage]
mode = dvc
dvc.remote = booktest-remote
dvc.manifest_path = booktest.manifest.yaml
```

Or use environment variables:

```bash
export BOOKTEST_STORAGE_MODE=dvc
export BOOKTEST_STORAGE_DVC_REMOTE=booktest-remote
export BOOKTEST_STORAGE_DVC_MANIFEST_PATH=booktest.manifest.yaml
```

### 4. Run tests with snapshots

```bash
# Run tests that use snapshots with -s flag to capture/refresh
./do test test/examples/snapshots -s

# Or run specific tests
./do test test/examples/snapshots/requests -s
```

## What happens with DVC storage?

When using DVC storage:

1. **Snapshot capture**: Snapshots are stored in `.booktest_cache/staging/` with content-addressable naming
   - Format: `.booktest_cache/staging/{snapshot_type}/sha256/{first2chars}/{fullhash}`
   - Example: `.booktest_cache/staging/http/sha256/ab/abc123...`

2. **Manifest tracking**: A `booktest.manifest.yaml` file is created/updated mapping test IDs to snapshot hashes
   ```yaml
   storage_mode: dvc
   test/examples/snapshots/requests:
     http: sha256:abc123...
   test/examples/snapshots/httpx:
     httpx: sha256:def456...
   ```

3. **Snapshot freezing**: When you accept/freeze snapshots, they are:
   - Moved from staging to cache (`.booktest_cache/`)
   - Pushed to the DVC remote (`/tmp/booktest-dvc-storage/`)

4. **Snapshot retrieval**: When running tests:
   - First checks local cache (`.booktest_cache/`)
   - If not found, pulls from DVC remote
   - Uses hash from manifest to locate content

## Verifying DVC storage works

### Check manifest file
```bash
cat booktest.manifest.yaml
```

Should show your tests and their snapshot hashes.

### Check staging area
```bash
ls -la .booktest_cache/staging/
```

Should show snapshot files organized by type and hash.

### Check DVC remote
```bash
ls -la /tmp/booktest-dvc-storage/
```

Should show content-addressable files after freezing snapshots.

## Comparing Git vs DVC storage

| Feature | Git Storage | DVC Storage |
|---------|-------------|-------------|
| Snapshot location | `books/.../_snapshots/*.json` | `.booktest_cache/` + remote |
| Git tracking | Full snapshot content | Only manifest file |
| Deduplication | No (duplicates stored) | Yes (same content = same hash) |
| Large files | Git bloat | Efficient remote storage |
| Manifest | Implicit (file paths) | Explicit (YAML file) |

## Testing both storage backends

### Test with Git storage (default)
```bash
# Remove or rename .dvc directory temporarily
mv .dvc .dvc.bak
./do test test/examples/snapshots -s
# Snapshots stored in books/.out/test/examples/snapshots/.../_snapshots/
```

### Test with DVC storage
```bash
# Restore .dvc directory
mv .dvc.bak .dvc
./do test test/examples/snapshots -s
# Snapshots stored in .booktest_cache/ and manifest
```

## Switching between storage modes

### Auto-detect (default)
Booktest automatically detects DVC if:
- DVC is installed
- `.dvc` directory or `dvc.yaml` exists
- OR `booktest.manifest.yaml` exists

### Force Git storage
```bash
# In .booktest file
[storage]
mode = git
```

### Force DVC storage
```bash
# In .booktest file
[storage]
mode = dvc
```

## Cleanup

To remove all DVC-related files:

```bash
# Remove DVC configuration
rm -rf .dvc dvc.yaml dvc.lock

# Remove booktest cache and manifest
rm -rf .booktest_cache booktest.manifest.yaml

# Remove local remote storage
rm -rf /tmp/booktest-dvc-storage
```

## Troubleshooting

### "DVC is not available"
- Ensure DVC is installed: `pip install dvc`
- Check it's in PATH: `which dvc`

### "Failed to push to DVC"
- Check remote configuration: `dvc remote list`
- Verify remote path exists: `ls /tmp/booktest-dvc-storage`
- Check DVC remote permissions

### "Missing snapshot for request"
- Run with `-s` flag to capture snapshots first
- Check manifest file has the test entry
- Try pulling from remote: `dvc pull` (from cache directory)

### Manifest not updating
- Verify storage mode is set to `dvc`
- Check file permissions on `booktest.manifest.yaml`
- Look for warnings in test output

## Advanced: Remote storage options

Instead of local storage, you can configure DVC to use:

### AWS S3
```bash
dvc remote add booktest-remote s3://mybucket/booktest-snapshots
dvc remote modify booktest-remote region us-west-2
```

### Google Cloud Storage
```bash
dvc remote add booktest-remote gs://mybucket/booktest-snapshots
```

### SSH/SFTP
```bash
dvc remote add booktest-remote ssh://user@host/path/to/storage
```

See [DVC remote storage documentation](https://dvc.org/doc/command-reference/remote) for more options.
