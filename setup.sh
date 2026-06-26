#!/bin/bash

# MINT macOS/Linux Installer Bootstrapper
# Checks for Python 3, clones the repository if run via curl, and launches the setup.

echo "=================================================="
echo "      M I N T   S E T U P   B O O T S T R A P"
echo "=================================================="

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# 2. Check if installer.py is in the current directory
if [ -f "installer.py" ]; then
    python3 installer.py
else
    # If run via curl | bash, clone the repo to a temporary folder and run setup
    echo "  ❯ Cloning MINT repository..."
    TEMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TEMP_DIR"' EXIT
    if command -v git &> /dev/null; then
        git clone https://github.com/sayfalse/mint.git "$TEMP_DIR"
    else
        echo "Error: Git is required for the automated curl installer."
        echo "Please install Git or manually download the repository."
        exit 1
    fi
    
    cd "$TEMP_DIR" || exit 1
    python3 installer.py
fi
