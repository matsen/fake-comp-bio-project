# Fake Computational Biology Project

## Purpose

This is a **tutorial project for learning agentic coding workflows**. It demonstrates building phylogenetic trees using UPGMA with flexible distance metrics.

The project is designed for a refactoring exercise:
- **V1 (current)**: Monolithic implementation with hardcoded Hamming distance
- **V2 (goal)**: Refactored code with pluggable distance functions (Hamming, Levenshtein, etc.)

## Design

See [docs/design/phylo-upgma/overview.md](docs/design/phylo-upgma/overview.md) for the complete design including the target V2 API.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Run Tests

```bash
pytest tests/ -v
```

## View Documentation

```bash
source .venv/bin/activate
pip install mkdocs-material
mkdocs serve
```

Navigate to http://127.0.0.1:8000

The documentation includes the complete design with the target V2 API and test examples.

## Tutorial Flow

1. Start with V1 (monolithic, working, tested)
2. Refactor to separate distance calculation from tree building
3. Verify all tests still pass (safety net)
4. Add Levenshtein distance support (now trivial)

The refactoring demonstrates clean separation of concerns and the power of abstraction.
