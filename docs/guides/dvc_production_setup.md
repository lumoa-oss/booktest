# DVC Production Setup Guide

This guide covers taking DVC-based snapshot storage into production use across your team and CI environment.

## Table of Contents

1. [Storage Location Options](#storage-location-options)
2. [Initial Setup (First Time)](#initial-setup-first-time)
3. [Developer Machine Setup](#developer-machine-setup)
4. [CI Integration](#ci-integration)
5. [Workflows and Best Practices](#workflows-and-best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Storage Location Options

The most critical decision is where to store your snapshot files. Each option has different trade-offs for ergonomics, collaboration, and CI complexity.

### Option 1: S3 or S3-Compatible Storage (Recommended)

**What it is:** Cloud object storage like AWS S3, DigitalOcean Spaces, MinIO, or Backblaze B2.

**Daily Ergonomics:**
- ✅ Snapshots automatically uploaded on first run with `-s`
- ✅ Snapshots automatically downloaded when missing
- ✅ Works from anywhere (office, home, CI)
- ✅ No VPN or network access required
- ⚠️ Requires credential setup once per machine
- ⚠️ May have small latency for downloads

**Pull Requests and Merges:**
- ✅ Manifest file (`booktest.manifest.yaml`) in Git shows what changed
- ✅ Snapshot content automatically available when PR is checked out
- ✅ Merge conflicts only in manifest file (plain YAML, easy to resolve)
- ✅ Reviewers can see snapshot diffs with `./do test -r`

**CI:**
- ✅ Easy to configure with environment variables
- ✅ Read-only credentials safe for public repos
- ✅ Fast parallel downloads
- ⚠️ Requires credential management (GitHub Secrets, etc.)

**Cost:** $5-20/month for typical project (depends on storage size and transfer)

**Setup Complexity:** Medium - requires cloud account and credential setup

**Recommended for:** Most teams, especially with remote developers or CI

---

### Option 2: SSH Remote (Shared Server)

**What it is:** A server accessible via SSH that all developers can reach (e.g., company server, VPS).

**Daily Ergonomics:**
- ✅ Snapshots automatically uploaded/downloaded
- ✅ No per-request costs
- ⚠️ Requires SSH access from all locations
- ⚠️ May require VPN when working remotely
- ⚠️ Performance depends on server location/connection

**Pull Requests and Merges:**
- ✅ Manifest file shows changes
- ✅ Snapshot content automatically available
- ✅ Same merge behavior as S3

**CI:**
- ⚠️ Requires SSH key in CI
- ⚠️ CI runners must have network access to server
- ⚠️ May need firewall rules for CI IPs

**Cost:** Free if server already exists, or $5-10/month for VPS

**Setup Complexity:** Medium - requires server setup and SSH key management

**Recommended for:** Teams with existing infrastructure and all developers on same network

---

### Option 3: Local Filesystem (Network Share)

**What it is:** A shared network drive (NFS, SMB, etc.) mounted on all developer machines.

**Daily Ergonomics:**
- ✅ Very fast (local filesystem speed)
- ✅ No credential management needed
- ⚠️ Requires network drive mounted on all machines
- ⚠️ Only works from locations with network access
- ❌ Doesn't work for remote developers without VPN

**Pull Requests and Merges:**
- ✅ Manifest file shows changes
- ⚠️ Developers must have network access to verify snapshots
- ⚠️ May lead to "works on my machine" issues

**CI:**
- ❌ Very difficult - CI runners need network mount
- ❌ Usually not feasible for cloud CI (GitHub Actions, etc.)
- ⚠️ Might work for self-hosted runners

**Cost:** Free if infrastructure exists

**Setup Complexity:** Low for developers, very high for CI

**Recommended for:** Small co-located teams not using cloud CI

---

### Option 4: Git LFS Alternative (Store in Git)

**What it is:** Don't use DVC - keep snapshots in Git with Git LFS.

**Daily Ergonomics:**
- ✅ No separate tool needed
- ✅ Everything in Git
- ❌ Slower Git operations (clone, pull, push)
- ❌ Large repo size over time
- ⚠️ Git LFS may have costs (GitHub charges for bandwidth)

**Pull Requests and Merges:**
- ✅ Everything in one place
- ❌ Large diffs in PRs
- ❌ Binary files hard to review

**CI:**
- ✅ Works automatically
- ⚠️ May have bandwidth costs

**Cost:** GitHub LFS: $5/month for 50GB storage + 50GB bandwidth

**Setup Complexity:** Low

**Recommended for:** Small projects with small snapshots (< 100MB total)

---

### Comparison Matrix

| Factor | S3-Compatible | SSH Remote | Network Share | Git LFS |
|--------|--------------|------------|---------------|---------|
| **Remote work** | ✅ Excellent | ⚠️ VPN needed | ❌ VPN required | ✅ Excellent |
| **CI integration** | ✅ Easy | ⚠️ Moderate | ❌ Difficult | ✅ Easy |
| **Setup complexity** | Medium | Medium | Low | Low |
| **Monthly cost** | $5-20 | $0-10 | $0 | $5+ |
| **Performance** | Good | Good-Excellent | Excellent | Poor (large repos) |
| **Scalability** | ✅ Unlimited | ⚠️ Server size | ⚠️ Share size | ❌ Git limits |

**Our recommendation:** Start with **S3-compatible storage** (DigitalOcean Spaces or AWS S3) unless you have specific constraints.

---

## Initial Setup (First Time)

This section covers setting up DVC for the first time in your repository.

### Prerequisites

```bash
# Install DVC with S3 support
pip install 'dvc[s3]'

# OR for SSH support
pip install 'dvc[ssh]'

# OR for all backends
pip install 'dvc[all]'
```

### Step 1: Initialize DVC in Repository

```bash
cd /path/to/your/booktest/project

# Initialize DVC (creates .dvc/ directory)
dvc init

# Commit DVC configuration
git add .dvc .dvcignore
git commit -m "Initialize DVC for snapshot storage"
```

### Step 2: Configure Remote Storage

Choose one based on your storage decision:

#### Option A: S3-Compatible Storage (Recommended)

**For AWS S3:**
```bash
# Configure remote
dvc remote add -d booktest-remote s3://your-bucket-name/booktest-snapshots

# Configure region
dvc remote modify booktest-remote region us-east-1

# Commit configuration
git add .dvc/config
git commit -m "Configure DVC remote storage"
```

**For DigitalOcean Spaces:**
```bash
# Configure remote
dvc remote add -d booktest-remote s3://your-space-name/booktest-snapshots

# Configure endpoint
dvc remote modify booktest-remote endpointurl https://nyc3.digitaloceanspaces.com

# Commit configuration
git add .dvc/config
git commit -m "Configure DVC remote storage"
```

**For MinIO (self-hosted S3):**
```bash
# Configure remote
dvc remote add -d booktest-remote s3://your-bucket/booktest-snapshots

# Configure endpoint
dvc remote modify booktest-remote endpointurl http://minio.yourcompany.com:9000

# Commit configuration
git add .dvc/config
git commit -m "Configure DVC remote storage"
```

#### Option B: SSH Remote

```bash
# Configure remote (replace with your server details)
dvc remote add -d booktest-remote ssh://user@server.yourcompany.com/path/to/dvc-storage

# Commit configuration
git add .dvc/config
git commit -m "Configure DVC SSH remote"
```

#### Option C: Local/Network Share

```bash
# Configure remote (path must be accessible from all machines)
dvc remote add -d booktest-remote /mnt/shared-drive/booktest-snapshots

# Or on Windows
dvc remote add -d booktest-remote Z:\\booktest-snapshots

# Commit configuration
git add .dvc/config
git commit -m "Configure DVC local remote"
```

### Step 3: Configure Booktest to Use DVC

Edit `.booktest` configuration:

```ini
# Storage configuration
storage.mode=dvc
storage.dvc.remote=booktest-remote
storage.dvc.manifest_path=booktest.manifest.yaml
```

Commit the configuration:

```bash
git add .booktest
git commit -m "Enable DVC storage in booktest"
```

### Step 4: Update .gitignore

Ensure `.gitignore` excludes local cache but includes manifest:

```gitignore
# DVC local cache (large binary files - don't commit)
.booktest_cache/

# Temporary files
.booktest.dvc

# Note: booktest.manifest.yaml SHOULD be tracked in Git
# Note: .dvc/ directory SHOULD be tracked in Git
```

```bash
git add .gitignore
git commit -m "Update gitignore for DVC storage"
```

### Step 5: Generate Initial Snapshots

```bash
# Run tests and create initial snapshots
./do test -s

# Verify manifest was created
cat booktest.manifest.yaml

# Push snapshots to remote storage
dvc push

# Commit manifest
git add booktest.manifest.yaml
git commit -m "Add initial test snapshots"
git push
```

### Step 6: Verify Setup

```bash
# Clear local cache to test remote access
rm -rf .booktest_cache

# Run tests - should fetch from remote
./do test

# Should show INTACT (not UPDATED) - verifies snapshots were fetched
```

✅ **Setup complete!** Other developers can now clone and use the snapshots.

---

## Developer Machine Setup

Instructions for developers joining the project after DVC is set up.

### Prerequisites

```bash
# Install DVC with appropriate backend support
pip install 'dvc[s3]'  # or [ssh], [all]

# OR install globally (recommended)
brew install dvc  # macOS
# or
apt install dvc   # Ubuntu
```

### Step 1: Clone Repository

```bash
git clone https://github.com/yourcompany/yourproject.git
cd yourproject

# DVC is already initialized (from .dvc/ in repo)
```

### Step 2: Configure Credentials

Choose based on your storage type:

#### For S3/Spaces/MinIO:

**Option A: AWS credentials file (recommended for AWS S3):**
```bash
# Create/edit ~/.aws/credentials
mkdir -p ~/.aws
cat >> ~/.aws/credentials << EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
EOF

chmod 600 ~/.aws/credentials
```

**Option B: DVC config (recommended for non-AWS):**
```bash
# Store credentials in local DVC config (not committed)
dvc remote modify --local booktest-remote access_key_id YOUR_ACCESS_KEY
dvc remote modify --local booktest-remote secret_access_key YOUR_SECRET_KEY
```

**Option C: Environment variables:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
```

#### For SSH Remote:

```bash
# Ensure SSH key is set up
ssh-add ~/.ssh/id_rsa

# Test connection
ssh user@server.yourcompany.com

# DVC will use your SSH key automatically
```

#### For Network Share:

```bash
# Ensure network drive is mounted
ls /mnt/shared-drive/booktest-snapshots

# No additional configuration needed
```

### Step 3: Fetch Snapshots

```bash
# DVC will automatically fetch snapshots when running tests
./do test

# Or manually pull all snapshots
dvc pull
```

### Step 4: Verify Setup

```bash
# Run tests - should show INTACT status
./do test

# You should see output like:
# test/examples/snapshots/httpx OK 46 ms. (snapshots intact)
```

✅ **Setup complete!** You're ready to develop.

### Daily Workflow

**When pulling changes:**
```bash
git pull
# DVC automatically fetches missing snapshots on next test run
./do test
```

**When creating new snapshots:**
```bash
# Make code changes
./do test -s  # Create new snapshots

# DVC automatically stores snapshots locally
# Push to remote for others to access
dvc push

# Commit manifest
git add booktest.manifest.yaml
git commit -m "Update snapshots for new feature"
git push
```

**When updating existing snapshots:**
```bash
./do test -r  # Review changes
./do test -s  # Accept changes

dvc push  # Upload new snapshot versions
git add booktest.manifest.yaml
git commit -m "Update snapshots after bug fix"
git push
```

---

## CI Integration

Setting up DVC in Continuous Integration environments.

### GitHub Actions

#### For S3/Spaces Storage:

**Step 1: Add credentials to GitHub Secrets**

Go to repository Settings → Secrets and variables → Actions → New repository secret:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

**Step 2: Configure workflow**

`.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
          pip install 'dvc[s3]'

      - name: Configure DVC credentials
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Credentials passed via environment variables
          echo "DVC configured with AWS credentials"

      - name: Run tests
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          poetry run booktest test
          # Or: ./do test

      - name: Check for snapshot changes
        if: github.event_name == 'pull_request'
        run: |
          # Fail if snapshots were updated without -s flag
          git diff --exit-code booktest.manifest.yaml || \
            (echo "❌ Snapshots changed but not committed!" && exit 1)
```

**For pull requests that update snapshots:**

```yaml
      - name: Verify snapshot updates
        if: github.event_name == 'pull_request'
        run: |
          # Check if manifest changed
          if git diff --quiet origin/${{ github.base_ref }} -- booktest.manifest.yaml; then
            echo "✅ No snapshot changes"
          else
            echo "⚠️ Snapshots were updated - review carefully"
            # Show what changed
            git diff origin/${{ github.base_ref }} -- booktest.manifest.yaml
          fi
```

#### For SSH Remote:

**Step 1: Add SSH key to GitHub Secrets**

Generate deploy key:
```bash
ssh-keygen -t ed25519 -f dvc_deploy_key -N ""
# Add dvc_deploy_key.pub to server's ~/.ssh/authorized_keys
# Add dvc_deploy_key (private) to GitHub Secrets as DVC_SSH_KEY
```

**Step 2: Configure workflow**

```yaml
      - name: Configure SSH for DVC
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DVC_SSH_KEY }}" > ~/.ssh/dvc_key
          chmod 600 ~/.ssh/dvc_key
          echo "Host dvc-server" >> ~/.ssh/config
          echo "  HostName server.yourcompany.com" >> ~/.ssh/config
          echo "  User dvcuser" >> ~/.ssh/config
          echo "  IdentityFile ~/.ssh/dvc_key" >> ~/.ssh/config
          echo "  StrictHostKeyChecking no" >> ~/.ssh/config

      - name: Install DVC with SSH support
        run: pip install 'dvc[ssh]'

      - name: Run tests
        run: poetry run booktest test
```

### GitLab CI

`.gitlab-ci.yml`:

```yaml
test:
  image: python:3.11

  before_script:
    - pip install poetry 'dvc[s3]'
    - poetry install

  script:
    - poetry run booktest test

  variables:
    AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY

  cache:
    paths:
      - .booktest_cache/
```

Configure secrets in GitLab Settings → CI/CD → Variables.

### Jenkins

**Jenkinsfile:**

```groovy
pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('dvc-aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('dvc-aws-secret-key')
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install poetry dvc[s3]'
                sh 'poetry install'
            }
        }

        stage('Test') {
            steps {
                sh 'poetry run booktest test'
            }
        }

        stage('Check Snapshots') {
            when {
                changeRequest()
            }
            steps {
                script {
                    def manifestChanged = sh(
                        script: 'git diff --exit-code booktest.manifest.yaml',
                        returnStatus: true
                    )
                    if (manifestChanged != 0) {
                        echo '⚠️ Snapshots were updated'
                    }
                }
            }
        }
    }
}
```

### CI Best Practices

1. **Use read-only credentials when possible**
   ```bash
   # Create a separate IAM user/role with only read permissions
   # CI doesn't need to push snapshots (developers do that)
   ```

2. **Cache DVC storage between runs**
   ```yaml
   # GitHub Actions
   - uses: actions/cache@v3
     with:
       path: .booktest_cache
       key: dvc-cache-${{ hashFiles('booktest.manifest.yaml') }}
   ```

3. **Fail if snapshots change unexpectedly**
   ```bash
   # Ensure developers used -s flag when updating snapshots
   git diff --exit-code booktest.manifest.yaml
   ```

4. **Show snapshot diff summary in PR comments**
   ```yaml
   - name: Comment on PR
     if: github.event_name == 'pull_request'
     run: |
       CHANGES=$(git diff origin/${{ github.base_ref }} --stat booktest.manifest.yaml)
       gh pr comment ${{ github.event.pull_request.number }} \
         --body "### Snapshot Changes\n\`\`\`\n$CHANGES\n\`\`\`"
   ```

---

## Workflows and Best Practices

### Workflow 1: Creating New Tests with Snapshots

```bash
# 1. Create new test
vim test/new_feature_test.py

# 2. Run with -s to generate snapshots
./do test test.new_feature -s

# 3. Review generated snapshots
cat books/test/new_feature.md

# 4. Push snapshots to remote
dvc push

# 5. Commit everything
git add test/new_feature_test.py booktest.manifest.yaml books/test/new_feature.md
git commit -m "Add new feature test with snapshots"
git push
```

### Workflow 2: Updating Existing Snapshots

```bash
# 1. Make code changes
vim src/feature.py

# 2. See what changed
./do test -r

# Review output:
# --- Expected
# +++ Actual
# Shows differences in snapshot content

# 3. If changes are intentional, update snapshots
./do test -s

# 4. Push new snapshots
dvc push

# 5. Commit manifest
git add booktest.manifest.yaml
git commit -m "Update snapshots after feature improvement"
git push
```

### Workflow 3: Reviewing Pull Requests with Snapshot Changes

```bash
# 1. Check out PR branch
gh pr checkout 123

# 2. See what snapshots changed
git diff main -- booktest.manifest.yaml

# 3. Run tests to fetch new snapshots
./do test

# 4. Review the actual changes in books/ folder
git diff main -- books/

# 5. Compare against baseline with review mode
git checkout main
./do test  # Establish baseline

git checkout pr-branch
./do test -r  # Show differences

# 6. If acceptable, approve and merge
```

### Workflow 4: Resolving Merge Conflicts in Manifest

When two branches both update snapshots:

```bash
# 1. Merge attempt fails with conflict in booktest.manifest.yaml
git merge feature-branch
# CONFLICT in booktest.manifest.yaml

# 2. Edit manifest - it's plain YAML with structure:
# test/path/to/test:
#   httpx: abc123...
#   metadata: def456...

# 3. Keep both changes (union merge for different tests)
vim booktest.manifest.yaml

# 4. Verify tests pass
./do test

# 5. Commit merge
git add booktest.manifest.yaml
git commit -m "Merge snapshot updates from feature-branch"

# 6. Push merged snapshots
dvc push
git push
```

### Workflow 5: Cleaning Up Old Snapshots

Over time, snapshots accumulate. Clean up unreferenced ones:

```bash
# See what would be removed
dvc gc --workspace --dry

# Remove snapshots not referenced in current manifest
dvc gc --workspace

# Push cleanup to remote (remove unreferenced files there too)
dvc gc --workspace --cloud

# Commit updated manifest if changed
git add booktest.manifest.yaml
git commit -m "Clean up unused snapshots"
git push
```

### Best Practices

**1. Always push before committing manifest:**
```bash
# ✅ Correct order
./do test -s
dvc push          # Push snapshots first
git commit        # Then commit manifest

# ❌ Wrong order
./do test -s
git commit        # Others can't fetch snapshots yet!
dvc push
```

**2. Use meaningful commit messages for snapshot changes:**
```bash
# ❌ Bad
git commit -m "Update snapshots"

# ✅ Good
git commit -m "Update snapshots: API now returns user age field"
```

**3. Review snapshot changes before committing:**
```bash
./do test -r  # Always review with -r flag first
./do test -s  # Only then accept with -s
```

**4. Keep snapshots and code changes together:**
```bash
# ✅ One commit with both
git add src/feature.py booktest.manifest.yaml
git commit -m "Add age field to user API response"

# Not: separate commits for code and snapshots
```

**5. Document significant snapshot changes in PR description:**
```markdown
## Changes
- Added age field to user API
- **Snapshots updated:** User API tests now include age field in expected output

## Testing
- Ran `./do test -s` to update snapshots
- Verified all tests pass with new snapshot baseline
```

---

## Troubleshooting

### Problem: "Failed to fetch snapshot from DVC"

**Symptoms:** Tests fail with warnings about missing snapshots.

**Solutions:**

1. **Check DVC remote is accessible:**
   ```bash
   dvc remote list
   dvc status -r booktest-remote
   ```

2. **Verify credentials are configured:**
   ```bash
   # For S3
   aws s3 ls s3://your-bucket-name/

   # For SSH
   ssh user@server.yourcompany.com
   ```

3. **Manually pull snapshots:**
   ```bash
   dvc pull -v
   ```

4. **Check if snapshots exist remotely:**
   ```bash
   # For S3
   aws s3 ls s3://your-bucket-name/booktest-snapshots/ --recursive

   # The hash from manifest should exist in remote
   grep "abc123" booktest.manifest.yaml
   aws s3 ls s3://your-bucket-name/booktest-snapshots/ --recursive | grep abc123
   ```

### Problem: "Tests show UPDATED when they should be INTACT"

**Symptoms:** After pulling changes, tests show snapshots as updated.

**Cause:** Local cache doesn't have the snapshot version referenced in manifest.

**Solutions:**

1. **Pull snapshots explicitly:**
   ```bash
   dvc pull
   ./do test
   ```

2. **Clear local cache and re-fetch:**
   ```bash
   rm -rf .booktest_cache
   ./do test
   ```

3. **Check if pusher actually uploaded:**
   ```bash
   # The developer who updated manifests should verify:
   dvc status -r booktest-remote
   # Should show "up to date"

   # If not:
   dvc push
   ```

### Problem: Merge conflicts in booktest.manifest.yaml

**Symptoms:** Git reports conflict in manifest file.

**Solution:**

The manifest is a simple YAML file mapping test IDs to snapshot hashes:

```yaml
storage_mode: dvc
test/examples/feature_a:
  httpx: abc123...
  metadata: def456...
test/examples/feature_b:
  httpx: xyz789...
  metadata: uvw012...
```

To resolve:

1. **Different tests changed:** Keep both (union merge)
   ```yaml
   <<<<<<< HEAD
   test/examples/feature_a:
     httpx: abc123...
   =======
   test/examples/feature_b:
     httpx: xyz789...
   >>>>>>> feature-branch

   # Resolution: Keep both
   test/examples/feature_a:
     httpx: abc123...
   test/examples/feature_b:
     httpx: xyz789...
   ```

2. **Same test changed differently:** Choose one or regenerate
   ```bash
   # Option A: Choose one version
   git checkout --theirs booktest.manifest.yaml

   # Option B: Regenerate from current code
   ./do test -s
   ```

3. **Verify and commit:**
   ```bash
   ./do test  # Ensure tests pass
   git add booktest.manifest.yaml
   git commit
   ```

### Problem: CI can't access DVC remote

**Symptoms:** CI tests fail with DVC access errors.

**Solutions:**

1. **Verify credentials are in CI secrets:**
   ```bash
   # Check they're set (don't print values!)
   echo "AWS_ACCESS_KEY_ID is set: ${AWS_ACCESS_KEY_ID:+yes}"
   ```

2. **Test credentials manually in CI:**
   ```yaml
   - name: Test DVC access
     run: |
       dvc remote list
       dvc status -r booktest-remote -v
   ```

3. **For SSH: verify key format:**
   ```bash
   # SSH key should be base64 encoded in secrets
   echo "${{ secrets.DVC_SSH_KEY }}" | base64 -d > ~/.ssh/dvc_key
   ```

4. **Check network access:**
   ```bash
   # Can CI reach the remote?
   curl -I https://your-bucket.s3.amazonaws.com/
   # Or for SSH:
   ssh -v user@server.yourcompany.com
   ```

### Problem: "Permission denied" errors

**Symptoms:** DVC operations fail with permission errors.

**Solutions:**

1. **S3: Verify IAM permissions include:**
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "s3:GetObject",
       "s3:PutObject",
       "s3:ListBucket"
     ],
     "Resource": [
       "arn:aws:s3:::your-bucket-name/*",
       "arn:aws:s3:::your-bucket-name"
     ]
   }
   ```

2. **SSH: Verify user has write access:**
   ```bash
   ssh user@server.yourcompany.com
   ls -la /path/to/dvc-storage
   touch /path/to/dvc-storage/test-file
   ```

3. **Network share: Check mount permissions:**
   ```bash
   ls -la /mnt/shared-drive/booktest-snapshots/
   # Should be writable by your user
   ```

### Problem: Slow snapshot operations

**Symptoms:** Tests take a long time to fetch/push snapshots.

**Solutions:**

1. **Enable DVC cache:**
   ```bash
   # DVC caches by default in .booktest_cache/
   # Ensure it's not being deleted
   ```

2. **Use parallel fetch/push:**
   ```bash
   # For S3
   dvc remote modify booktest-remote jobs 8
   ```

3. **Check network bandwidth:**
   ```bash
   # Test download speed
   time dvc pull -v
   ```

4. **For large snapshots, consider:**
   - Using a closer storage region
   - Compressing snapshot data
   - Splitting into smaller test cases

### Problem: Snapshot hash mismatches

**Symptoms:** Same content produces different hashes.

**Cause:** Usually line ending differences (CRLF vs LF).

**Solutions:**

1. **Ensure consistent line endings:**
   ```bash
   git config --global core.autocrlf input  # Unix-style LF
   ```

2. **Regenerate all snapshots on same platform:**
   ```bash
   rm -rf .booktest_cache
   ./do test -s
   dvc push --force
   ```

3. **Check snapshot content:**
   ```bash
   # Find snapshot file by hash
   HASH=abc123...
   find .booktest_cache -name "${HASH}*"

   # Examine content
   cat .booktest_cache/httpx/ab/c123...
   ```

---

## Migration from Git Storage

If you're currently using Git-based storage and want to migrate to DVC:

### Step 1: Backup current snapshots

```bash
# Ensure everything is committed
git status

# Create backup branch
git checkout -b backup-before-dvc
git push -u origin backup-before-dvc
git checkout main
```

### Step 2: Initialize DVC (as described above)

```bash
dvc init
dvc remote add -d booktest-remote s3://your-bucket/booktest-snapshots
# ... configure credentials ...
```

### Step 3: Update booktest configuration

```ini
# Change from:
# storage.mode=git

# To:
storage.mode=dvc
storage.dvc.remote=booktest-remote
storage.dvc.manifest_path=booktest.manifest.yaml
```

### Step 4: Regenerate snapshots in DVC format

```bash
# This will create new snapshots in DVC format
./do test -s

# Push to DVC remote
dvc push

# Commit manifest
git add booktest.manifest.yaml .dvc/config .booktest
git commit -m "Migrate to DVC storage"
```

### Step 5: Clean up old Git-stored snapshots

```bash
# Remove old snapshot files from git
git rm -r books/test/**/_snapshots/

# Commit removal
git commit -m "Remove old Git-stored snapshots (now in DVC)"
```

### Step 6: Verify migration

```bash
# Clear cache
rm -rf .booktest_cache

# Run tests - should fetch from DVC
./do test

# Should show INTACT status
```

### Step 7: Update team and CI

- Send migration guide to team
- Update CI configuration with DVC credentials
- Update documentation

---

## Summary

**For most teams, we recommend:**

- **Storage:** S3-compatible (DigitalOcean Spaces or AWS S3)
- **Credentials:** AWS credentials file for developers, GitHub Secrets for CI
- **Workflow:** Always `dvc push` before `git push` when updating snapshots
- **CI:** Use read-only credentials, cache `.booktest_cache/` between runs

This setup provides:
- ✅ Works from anywhere (no VPN needed)
- ✅ Easy CI integration
- ✅ Reasonable costs ($5-20/month)
- ✅ Scales with team size
- ✅ Clear separation between code (Git) and data (DVC)

For questions or issues, check the [troubleshooting section](#troubleshooting) or open an issue on GitHub.
