# Devcontainer Setup for fake-comp-bio-project

This devcontainer provides a complete development environment for the fake-comp-bio-project tutorial, demonstrating best practices for agentic coding workflows.

## Features

- **Python 3.11**: Modern Python environment
- **Development Tools**:
  - `pytest` for testing
  - `mypy` for type checking
  - `ruff` for linting and formatting
  - `mkdocs-material` for documentation
- **Git Tools**: `git`, `git-extras`, and GitHub CLI (`gh`)
- **Claude Code**: Pre-installed for agentic coding demonstrations
- **Zsh**: Enhanced shell with helpful aliases and git integration
- **VS Code Integration**: Pre-configured Python extensions and settings

## Quick Start

### Using VS Code

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open this folder in VS Code
3. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")
4. Wait for the container to build and start
5. The virtual environment will be auto-created and activated

### Manual Container Build

```bash
# Build the container
docker build -t fake-comp-bio-project .devcontainer

# Run the container
docker run -it -v $(pwd):/workspace fake-comp-bio-project
```

## What Gets Installed

The container automatically:
1. Installs the project in development mode: `pip install -e '.[dev]'`
2. Creates a `.venv` virtual environment
3. Installs all dependencies from `pyproject.toml`

## Helpful Commands

Once inside the container:

```bash
# Run tests
pytest tests/ -v

# View documentation locally
mkdocs serve  # Then visit http://127.0.0.1:8000

# Type checking
mypy fakephylo

# Format code
ruff format .

# Run Claude Code (if you have API credentials)
claude
```

## Shell Aliases

The container includes helpful aliases:

- `yolo` - Run Claude Code without permission prompts
- `pbcopy` / `xclip` - Copy to clipboard (works in VS Code terminal via OSC 52)
- `cpth <file>` - Copy absolute file path to clipboard
- `ll`, `la`, `l` - Various `ls` shortcuts

## For Demo Purposes

This devcontainer is designed for demonstrating the agentic coding workflow described in:
- [Agentic Coding from First Principles](https://matsen.fredhutch.org/general/2025/10/30/agentic-coding-principles.html)
- [Agentic Git Flow](https://matsen.fredhutch.org/general/2025/11/01/agentic-git-flow.html)

Key demonstration features:
- Clean, reproducible environment
- All development tools pre-installed
- Ready for test-driven development
- Configured for agentic workflows with Claude Code

## Customization

To use Claude Code inside the container, you'll need to mount your credentials:

```json
"mounts": [
  "source=${HOME}/.claude/.credentials.json,target=/home/vscode/.claude/.credentials.json,type=bind"
]
```

Add this to `devcontainer.json` if you want to persist Claude Code credentials.
