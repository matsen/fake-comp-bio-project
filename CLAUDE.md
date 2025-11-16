# CLAUDE.md

This file provides guidance to Claude Code when working with the fake computational biology tutorial project.

## Project Overview

This is a **tutorial project for learning agentic coding workflows**. It demonstrates building phylogenetic trees using UPGMA with flexible distance metrics through a refactoring exercise.

### Tutorial Structure
- **V1 (current)**: Monolithic implementation with hardcoded Hamming distance
- **V2 (goal)**: Refactored code with pluggable distance functions (Hamming, Levenshtein, etc.)

The project intentionally starts with non-ideal code (V1) that students refactor into clean architecture (V2).

## Code Quality Standards

### Testing Standards and Validation

#### Real Tests, No Fake Implementations
- **No Sophisticated Fake Mocks**: Tests must validate real behavior, not fake implementations. Identity functions, trivial arithmetic, or hardcoded returns are forbidden.
- **Real Implementations**: Use actual BioPython objects and real DNA sequences, not mock objects that return fake data.
- **Zero Tolerance for Partial Tests**: All tests must be fully implemented. Placeholder tests (`pass`), empty test bodies, `pytest.mark.skip` without implementation, or tests that return fake data are prohibited.
- **Implementation-Complete Rule**: Every test function must perform meaningful assertions against real system behavior. Tests exist to validate correctness, not to achieve coverage metrics.

**⚠️ CRITICAL ANTI-FAKE TEST BARRIER ⚠️**

If you find yourself thinking "I'll just create a simple mock that returns..." or "I'll make a fake implementation that..." then **STOP IMMEDIATELY**. This is a red flag indicating you're about to violate the real-testing principle. Instead:
1. **Use real data**: Create actual sequences and distance matrices
2. **Use real libraries**: Use BioPython's actual tree construction, not mocks
3. **Test real behavior**: Verify ultrametric properties, tree topology, branch lengths
4. **Ask for help**: If real testing seems difficult, it means the design may need improvement

**The temptation to fake is a design smell** - address the underlying issue rather than masking it with fake implementations.

#### Fail-Fast, No Fallbacks
- **No Silent Fallbacks**: Code must fail immediately when expected conditions aren't met. Silent fallback behavior masks bugs and creates unpredictable systems.
- **Explicit Error Messages**: When something goes wrong, stop execution with clear error messages explaining what failed and what was expected.
- **Example**: `raise ValueError(f"All sequences must have the same length, got lengths: {lengths}")` instead of silently using only equal-length sequences.

### Clean Code Principles
- **Single Responsibility**: Each function does one thing well
- **Meaningful Names**: Variables and functions reveal intent without comments
- **DRY Violations**: Eliminate code duplication through proper abstraction
- **Small Functions**: Keep functions focused and readable
- **Type Hints**: All functions must have complete type annotations

### Development Workflow
1. **Design First**: Create clear architectural plans before coding (see design docs)
2. **Simplify Relentlessly**: Remove complexity aggressively - the simplest design that works is usually best
3. **Type Hints**: All functions and classes must have complete type annotations
4. **Testing**: Comprehensive unit tests with real implementations
5. **Documentation**: Functions need docstrings explaining purpose, args, and returns

### Pre-PR Quality Checklist

Before any pull request, ensure the following workflow is completed:

#### Code Quality Foundation
1. **Format Code**: Ensure consistent formatting (use black/ruff if available)
2. **Documentation**: Ensure all non-trivial functions have comprehensive docstrings
3. **Type Hints**: Verify all functions have complete type annotations

#### Architecture and Implementation Review
4. **Clean Code Review**: Run `@clean-code-reviewer` agent on all new/modified code for architectural review
5. **Fail-Fast Validation**: Verify no silent fallbacks or error suppression

#### Test Quality Validation
6. **Test Implementation Audit**: Scan all test files for partially implemented tests, placeholder implementations, mock objects that return fake data, or `pytest.mark.skip` decorators. All tests must provide real validation with actual implementations
7. **Integration Tests**: Ensure all tests pass with `pytest tests/ -v`
8. **Test Coverage**: Verify comprehensive test coverage of new functionality
9. **Real Test Validation**: Confirm no fake mocks or trivial test implementations

### Error Handling
- **Fail Fast**: Use assertions and validation to catch errors early
- **Stop Everything**: When something seems wrong, stop immediately - never handle errors silently
- **Loud Failures**: Silent error handling is forbidden - all errors must be visible and halt execution
- **Meaningful Messages**: Error messages should explain what went wrong and what was expected
- **Type Safety**: Use type hints to catch errors at development time
- **Input Validation**: Validate inputs at function boundaries

### Naming Conventions
- **Count Pattern**: Use `num_x` consistently for all countable quantities (`num_sequences`, `num_species`)
- Variables reveal intent: `distance_function` not `df`, `hamming_distance` not `hd`
- Functions match behavior: `compute_distance_matrix()` not `calc_dm()`
- Booleans are questions: `has_equal_lengths` not `equal_lengths`

## Repository Structure

```
fake-comp-bio-project/
├── fakephylo/                   # Main Python package
│   ├── __init__.py              # Package exports
│   └── tree_builder.py          # V1: Monolithic UPGMA implementation
├── docs/                        # Documentation (mkdocs)
│   ├── index.md                 # Documentation homepage
│   ├── design/                  # Design documents
│   │   └── phylo-upgma/
│   │       └── overview.md      # Complete design with V2 API
│   └── javascripts/
│       └── mathjax.js           # LaTeX math support
├── tests/                       # Test suite
│   └── test_tree_builder.py    # V1 tests (all pass)
├── data/                        # Example datasets
├── .venv/                       # Virtual environment (not committed)
├── Makefile                     # Development commands (if needed)
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
├── mkdocs.yml                   # Documentation configuration
└── pyproject.toml               # Project dependencies and config
```

## Documentation

The project uses **mkdocs** with the Material theme:

- **Local development**: `mkdocs serve` → http://127.0.0.1:8000
- **Install**: `pip install mkdocs-material`
- **Structure**: Design documents under `docs/design/phylo-upgma/`
- **Features**: Dark/light mode toggle, search, responsive design

## Development Environment

### Virtual Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest python-Levenshtein
```

### Running Tests
```bash
source .venv/bin/activate
pytest tests/ -v
```

All tests must pass before committing changes.

## Tutorial Learning Objectives

This project teaches:

1. **Recognizing Tight Coupling**: V1 embeds distance calculation inside tree building
2. **Refactoring with Tests**: Use tests as safety net during refactoring
3. **Separation of Concerns**: Extract distance calculation into separate function
4. **Function Composition**: Build flexible APIs through composition
5. **Clean Architecture**: Depend on abstractions (distance functions) not concretions

The refactoring from V1 to V2 demonstrates how proper abstraction enables easy extension.
