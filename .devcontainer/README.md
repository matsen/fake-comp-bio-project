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
- **Claude Code**: Pre-installed with persistent auth and settings
- **Keychain**: SSH key management with passphrase caching
- **Zsh**: Enhanced shell with helpful aliases and git integration
- **VS Code Integration**: Pre-configured Python extensions and settings

## Quick Start

### First-Time Setup

1. **Configure GitHub CLI authentication**:
   - Open VS Code User Settings (Cmd+,)
   - Search for "terminal.integrated.env"
   - Click "Edit in settings.json"
   - Add to your **User settings.json** (NOT workspace):
     ```json
     {
       "terminal.integrated.env.linux": {
         "GH_TOKEN": "ghp_your_github_token_here"
       }
     }
     ```
   - Get your token from: https://github.com/settings/tokens/new (needs `repo` scope)
   - **Note**: This goes in user settings so it stays private and works across all projects

2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open this folder in VS Code
4. Click "Reopen in Container" when prompted
5. On first launch, press **ESC twice** to skip Claude Code's theme/terminal setup prompts

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

# Run Claude Code
claude

# GitHub CLI (pre-authenticated via GH_TOKEN)
gh issue list
gh pr create
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

## SSH Agent Forwarding

The devcontainer forwards your host's SSH agent via Docker Desktop's socket at `/run/host-services/ssh-auth.sock`. Your keys stay on the host—only the agent connection is forwarded.

### Verify It's Working
```bash
# In container
echo $SSH_AUTH_SOCK   # Should show /run/host-services/ssh-auth.sock
ssh-add -l            # Should show your key
ssh -T git@github.com # Test GitHub access
```

### Troubleshooting

**"The agent has no identities"**
1. Check host has keys loaded: `ssh-add -l` on host
2. On macOS, load keys with: `ssh-add --apple-use-keychain`

**Wrong socket path (shows `/tmp/ssh-...`)**
- The SSHD devcontainer feature overrides `SSH_AUTH_SOCK`—remove it from `devcontainer.json`
- `keychain` in shell config also overrides it—don't initialize keychain with agent forwarding

**Test Docker Desktop forwarding directly:**
```bash
docker run --rm -it -v /run/host-services/ssh-auth.sock:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent alpine sh -c "apk add openssh-client && ssh-add -l"
```
If this shows your key, Docker Desktop forwarding works and the issue is in devcontainer config.

## Claude Code Integration

Claude Code is fully integrated with persistent authentication and settings:

### What Persists Across Rebuilds
- ✅ Claude Code authentication (`.credentials.json`)
- ✅ Claude Code settings (`settings.json`)
- ✅ Custom slash commands
- ✅ Session state and analytics

### Custom Agents and Hooks
To add custom agents or hooks, mount them in `devcontainer.json`:

```json
"mounts": [
  "source=/path/to/custom-agents,target=/home/vscode/.claude/agents,type=bind",
  "source=/path/to/hooks,target=/home/vscode/.claude/hooks,type=bind"
]
```

## GitHub CLI (gh)

GitHub CLI is pre-configured to work via the `GH_TOKEN` environment variable set in your VS Code user settings. This means:
- ✅ No need to authenticate inside the container
- ✅ Works immediately on container start
- ✅ Secure (token stays in user settings, not committed to repos)

## Persistent Data

The following persist across container rebuilds:
- Claude Code authentication and settings
- SSH key passphrases (via keychain, per session)
- GitHub CLI authentication (via GH_TOKEN env var)
- Your project code and git history (mounted from host)
