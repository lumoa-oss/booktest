#!/bin/bash
# Script to set up DVC for local testing with booktest

set -e

echo "Setting up DVC for local booktest testing..."
echo

# Check if DVC is installed
if ! command -v dvc &> /dev/null; then
    echo "❌ DVC is not installed."
    echo "Install it with: pip install dvc"
    echo "Or with poetry: poetry add dvc --group dev"
    exit 1
fi

echo "✓ DVC is installed ($(dvc --version))"

# Initialize DVC if not already initialized
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
    echo "✓ DVC initialized"
else
    echo "✓ DVC already initialized"
fi

# Create local storage directory
STORAGE_DIR="/tmp/booktest-dvc-storage"
echo
echo "Creating local storage directory: $STORAGE_DIR"
mkdir -p "$STORAGE_DIR"
echo "✓ Storage directory created"

# Configure DVC remote
echo
echo "Configuring DVC remote..."
if dvc remote list | grep -q "booktest-remote"; then
    echo "Updating existing booktest-remote..."
    dvc remote modify booktest-remote url "$STORAGE_DIR"
else
    echo "Adding new booktest-remote..."
    dvc remote add -d booktest-remote "$STORAGE_DIR"
fi
echo "✓ DVC remote configured"

# Create .booktest configuration
echo
echo "Creating .booktest configuration..."
cat > .booktest.dvc << 'EOF'
[storage]
mode = dvc
dvc.remote = booktest-remote
dvc.manifest_path = booktest.manifest.yaml
EOF
echo "✓ Created .booktest.dvc (DVC configuration)"

# Keep original .booktest if exists
if [ -f ".booktest" ]; then
    echo "✓ Original .booktest preserved"
    echo
    echo "To use DVC storage, rename files:"
    echo "  mv .booktest .booktest.git"
    echo "  mv .booktest.dvc .booktest"
else
    mv .booktest.dvc .booktest
    echo "✓ .booktest configured for DVC"
fi

# Add .gitignore entries
echo
echo "Updating .gitignore..."
if [ -f ".gitignore" ]; then
    if ! grep -q ".booktest_cache" .gitignore; then
        echo ".booktest_cache/" >> .gitignore
        echo "booktest.manifest.yaml" >> .gitignore
        echo "✓ Added DVC entries to .gitignore"
    else
        echo "✓ .gitignore already contains DVC entries"
    fi
else
    echo ".booktest_cache/" > .gitignore
    echo "booktest.manifest.yaml" >> .gitignore
    echo "✓ Created .gitignore with DVC entries"
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ DVC setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Next steps:"
echo "  1. Run tests with snapshots:"
echo "     ./do test test/examples/snapshots -s"
echo
echo "  2. Check the manifest file:"
echo "     cat booktest.manifest.yaml"
echo
echo "  3. Check DVC remote storage:"
echo "     ls -la $STORAGE_DIR"
echo
echo "To switch back to Git storage:"
echo "  mv .booktest .booktest.dvc"
echo "  mv .booktest.git .booktest  # if you backed it up"
echo "  # or just remove .dvc directory:"
echo "  rm -rf .dvc"
echo
echo "To clean up DVC completely:"
echo "  rm -rf .dvc .booktest_cache booktest.manifest.yaml"
echo "  rm -rf $STORAGE_DIR"
echo
