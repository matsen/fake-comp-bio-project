#!/bin/bash
set -e

echo "Setting up fake-comp-bio-project environment..."
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"

cd /workspace
echo "Changed to: $(pwd)"

# Check if we're in the right place
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found in /workspace"
    ls -la /workspace
    exit 1
fi

echo "Found pyproject.toml, proceeding..."

# Remove any existing .venv from host (might have wrong symlinks)
if [ -d ".venv" ]; then
    echo "Removing existing .venv directory..."
    rm -rf .venv
fi

# Create virtual environment
echo "Creating virtual environment..."
echo "Python version: $(python3 --version)"
echo "Running: python3 -m venv --copies .venv"

python3 -m venv --copies .venv 2>&1 || {
    echo "ERROR: venv creation failed with exit code $?"
    echo "Checking if .venv directory was created:"
    ls -la .venv/ 2>&1 || echo ".venv directory does not exist"
    echo "Checking .venv/bin contents:"
    ls -la .venv/bin/ 2>&1 || echo ".venv/bin does not exist"
    echo "Checking python3 venv module:"
    python3 -m venv --help 2>&1 || echo "venv module not available"
    exit 1
}

echo "Venv creation command completed, checking result..."
ls -la .venv/

# Verify venv was created
if [ ! -f ".venv/bin/python" ]; then
    echo "Error: Virtual environment creation failed - .venv/bin/python not found"
    echo "Contents of .venv:"
    ls -la .venv/
    echo "Contents of .venv/bin (if exists):"
    ls -la .venv/bin/ 2>&1 || echo ".venv/bin does not exist"
    exit 1
fi

echo "Virtual environment created successfully!"

# Upgrade pip
echo "Upgrading pip..."
.venv/bin/pip install --upgrade pip

# Install project in dev mode
echo "Installing project in dev mode..."
.venv/bin/pip install -e ".[dev]"

echo ""
echo "Environment ready! Run pytest to verify setup."
echo ""
