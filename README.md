# Fake Computational Biology Project

A tutorial project for learning agentic coding workflows. Demonstrates building phylogenetic trees using UPGMA with flexible distance metrics.

## Using This Template

This is a GitHub template repository. To use it:

1. Click **"Use this template"** at the top of the page
2. Create your own copy with a new repository name
3. Clone and start coding

## Getting Started

### Option 1: Devcontainer (Recommended)

This project includes a pre-configured development environment using [VS Code devcontainers](https://code.visualstudio.com/docs/devcontainers/containers).

1. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open this project in VS Code
3. Click "Reopen in Container" when prompted

All tools are pre-installed. See [.devcontainer/README.md](.devcontainer/README.md) for details.

### Option 2: Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Usage

```bash
# Run tests
pytest tests/ -v

# View documentation
mkdocs serve  # Navigate to http://127.0.0.1:8000
```

## Project Structure

**Current (V1)**: Monolithic implementation with hardcoded Hamming distance
**Goal (V2)**: Refactored code with pluggable distance functions

See [docs/design/phylo-upgma/overview.md](docs/design/phylo-upgma/overview.md) for the complete design.

## Tutorial Flow

1. Start with V1 (monolithic, working, tested)
2. Refactor to separate distance calculation from tree building
3. Verify all tests still pass
4. Add Levenshtein distance support (now trivial with clean abstraction)

This demonstrates clean separation of concerns and the power of abstraction.
