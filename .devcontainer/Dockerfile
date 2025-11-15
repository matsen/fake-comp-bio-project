# Devcontainer for fake-comp-bio-project
# Tutorial project demonstrating agentic coding workflows
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-extras \
    build-essential \
    curl \
    wget \
    vim \
    less \
    zsh \
    fzf \
    autojump \
    sudo \
    procps \
    tree \
    keychain \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for Claude Code)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user with zsh as default shell
RUN useradd -m -s /bin/zsh vscode && \
    usermod -aG sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install Python development tools globally (including venv)
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mypy \
    pytest \
    pytest-cov \
    ruff \
    ipython \
    mkdocs-material

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Set working directory
WORKDIR /workspace

# Copy post-create script and make it executable
COPY post-create.sh /usr/local/bin/post-create.sh
RUN chmod +x /usr/local/bin/post-create.sh

# Create directories with proper ownership before switching user
RUN mkdir -p /home/vscode/.claude /home/vscode/.antigen && \
    chown -R vscode:vscode /home/vscode/.claude /home/vscode/.antigen

# Switch to vscode user
USER vscode

# Configure git to trust mounted repository
RUN git config --global --add safe.directory /workspace

# Create a nice .zshrc with helpful aliases
RUN echo '# Simple prompt with git info\n\
autoload -Uz vcs_info\n\
precmd() { vcs_info }\n\
zstyle ":vcs_info:git:*" formats " (%b)"\n\
setopt PROMPT_SUBST\n\
PROMPT="%F{green}%n@%m%f:%F{blue}%~%f\${vcs_info_msg_0_} %# "\n\
\n\
# Enable command history\n\
HISTFILE=~/.zsh_history\n\
HISTSIZE=10000\n\
SAVEHIST=10000\n\
setopt SHARE_HISTORY\n\
\n\
# Enable command completion\n\
autoload -Uz compinit && compinit\n\
\n\
# Helpful aliases\n\
alias ll="ls -lah"\n\
alias la="ls -A"\n\
alias l="ls -CF"\n\
\n\
# OSC 52 clipboard copy function (works in VS Code terminal)\n\
copy() {\n\
    if [ -t 0 ]; then\n\
        # No stdin, copy file or argument\n\
        [ -f "$1" ] && cat "$1" | copy || echo -n "$*" | copy\n\
    else\n\
        # Read from stdin\n\
        buf=$(cat)\n\
        printf "\\033]52;c;$(echo -n "$buf" | base64 | tr -d \"\\n\")\\007"\n\
    fi\n\
}\n\
alias pbcopy="copy"\n\
alias xclip="copy"\n\
\n\
# Copy absolute path to clipboard\n\
cpth() {\n\
    readlink -f "$1" | copy\n\
    echo "Copied to clipboard: $(readlink -f "$1")"\n\
}\n\
\n\
# Claude convenience aliases\n\
alias yolo="claude --dangerously-skip-permissions"\n\
\n\
# Initialize keychain for SSH key management\n\
if command -v keychain &> /dev/null; then\n\
    # Start keychain and add SSH keys (will prompt for passphrase once per session)\n\
    eval $(keychain --eval --quiet id_rsa id_ed25519 2>/dev/null)\n\
fi\n\
\n\
# Auto-activate virtual environment if it exists\n\
if [ -d "/workspace/.venv" ]; then\n\
    source /workspace/.venv/bin/activate\n\
fi\n\
\n\
# Helpful startup message\n\
echo ""\n\
echo "Welcome to fake-comp-bio-project devcontainer!"\n\
echo ""\n\
echo "Quick start:"\n\
echo "  pip install -e \".[dev]\"  # Install project in dev mode"\n\
echo "  pytest tests/ -v         # Run tests"\n\
echo "  mkdocs serve             # View documentation"\n\
echo ""\n\
' > /home/vscode/.zshrc
