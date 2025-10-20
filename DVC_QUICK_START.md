# DVC Quick Start for Booktest

## One-command setup

```bash
./setup_dvc_local.sh
```

This script will:
- Check DVC installation
- Initialize DVC
- Create local storage at `/tmp/booktest-dvc-storage`
- Configure booktest to use DVC
- Update `.gitignore`

## Manual setup (if you prefer)

```bash
# 1. Install DVC
pip install dvc

# 2. Initialize DVC
dvc init

# 3. Configure local remote
mkdir -p /tmp/booktest-dvc-storage
dvc remote add -d booktest-remote /tmp/booktest-dvc-storage

# 4. Configure booktest (add to .booktest file)
cat >> .booktest << 'EOF'

[storage]
mode = dvc
EOF
```

## Run tests with DVC

```bash
# Run all snapshot tests
./do test test/examples/snapshots -s

# Run specific test
./do test test/datascience/gpt -s

# Check what storage is being used
grep -A3 "\[storage\]" .booktest
```

## Verify it's working

```bash
# Check manifest (Git-tracked, small file)
cat booktest.manifest.yaml

# Check cache (large snapshot files, local only)
ls -lah .booktest_cache/

# Check remote storage (persisted snapshots)
ls -lah /tmp/booktest-dvc-storage/
```

## Switch between Git and DVC

### Use DVC storage
```bash
# Option 1: Via config file
echo -e "\n[storage]\nmode = dvc" >> .booktest

# Option 2: Via environment
export BOOKTEST_STORAGE_MODE=dvc
```

### Use Git storage
```bash
# Option 1: Via config file
echo -e "\n[storage]\nmode = git" >> .booktest

# Option 2: Via environment
export BOOKTEST_STORAGE_MODE=git

# Option 3: Remove .dvc directory
rm -rf .dvc
```

## File locations

| What | Git Storage | DVC Storage |
|------|-------------|-------------|
| Snapshots | `books/.out/.../\_snapshots/*.json` | `.booktest_cache/{type}/sha256/...` |
| Tracked in Git | Full snapshot files | Only `booktest.manifest.yaml` |
| Remote storage | N/A | `/tmp/booktest-dvc-storage/` |

## Common workflows

### First time capturing snapshots
```bash
./do test test/examples/snapshots -s
# Snapshots captured to staging area
# Manifest updated with hashes
```

### Accepting/freezing snapshots
```bash
./do test test/examples/snapshots -s -a
# Or interactively accept during review
# Snapshots promoted to cache and pushed to remote
```

### Running tests with existing snapshots
```bash
./do test test/examples/snapshots
# Reads from manifest
# Fetches from cache or remote as needed
# No `-s` flag = use existing snapshots
```

### Re-capturing snapshots (refresh)
```bash
./do test test/examples/snapshots -s
# Generates new snapshots
# Updates manifest if content changed
# Shows "(snapshots updated)" if hashes differ
```

## Troubleshooting

### Check current storage mode
```bash
# Method 1: Check config
grep -A3 "\[storage\]" .booktest

# Method 2: Check for DVC files
ls -la .dvc/  # If exists = DVC available

# Method 3: Check manifest
cat booktest.manifest.yaml  # If exists = DVC likely in use
```

### DVC not working?
```bash
# Check DVC is installed
dvc --version

# Check DVC remote
dvc remote list

# Check remote path exists
ls -la /tmp/booktest-dvc-storage/

# Force Git mode to compare
echo -e "\n[storage]\nmode = git" > .booktest
```

### Compare Git vs DVC results
```bash
# Run with Git
echo -e "\n[storage]\nmode = git" > .booktest
./do test test/examples/snapshots/requests -s
cp books/.out/test/examples/snapshots/requests.md /tmp/git-result.md

# Run with DVC
echo -e "\n[storage]\nmode = dvc" > .booktest
./do test test/examples/snapshots/requests -s
cp books/.out/test/examples/snapshots/requests.md /tmp/dvc-result.md

# Compare results
diff /tmp/git-result.md /tmp/dvc-result.md
# Should be identical (both storage backends produce same results)
```

## Clean up

```bash
# Remove all DVC files
rm -rf .dvc .booktest_cache booktest.manifest.yaml dvc.yaml dvc.lock
rm -rf /tmp/booktest-dvc-storage

# Remove DVC config from .booktest
sed -i '/\[storage\]/,/^$/d' .booktest
```

## What gets committed to Git?

### With Git storage:
- `books/.out/.../_snapshots/*.json` (full snapshot files)
- Large binary content tracked in Git

### With DVC storage:
- `booktest.manifest.yaml` (small text file with hashes)
- `.dvc/` directory (DVC configuration)
- `.gitignore` updated to exclude `.booktest_cache/`
- No large snapshot files in Git

**Result:** Much smaller Git repository, faster clones, cleaner diffs!
