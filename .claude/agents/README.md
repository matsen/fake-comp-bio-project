# Claude Code Agents

This directory contains specialized agents for code quality and architecture review.

## Available Agents

### clean-code-reviewer
Reviews code for clean code principles including:
- Single Responsibility Principle
- Meaningful naming
- DRY violations
- Function size and complexity
- Clear intent and readability

**Usage**: `@clean-code-reviewer`

Invoke this agent on new/modified code before creating pull requests.

### antipattern-scanner
Scans code for common architectural antipatterns:
- God objects and classes
- Shotgun surgery
- Feature envy
- Primitive obsession
- And more

**Usage**: `@antipattern-scanner`

## Source

These agents are maintained at: https://github.com/matsengrp/claude-code-agents

They are copied into this project during container setup to make the template self-contained.
