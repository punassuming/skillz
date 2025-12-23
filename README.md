# Skillz

<img src="skillz.png" alt="Skillz" width="300">

[![Tests](https://github.com/jkitchin/skillz/actions/workflows/test.yml/badge.svg)](https://github.com/jkitchin/skillz/actions/workflows/test.yml)
[![Lint](https://github.com/jkitchin/skillz/actions/workflows/lint.yml/badge.svg)](https://github.com/jkitchin/skillz/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/jkitchin/skillz/graph/badge.svg)](https://codecov.io/gh/jkitchin/skillz)


A comprehensive CLI tool for managing AI assistant skills and slash commands for OpenCode, Claude Code, Codex, Gemini, GitHub Copilot, MCP, and other LLM platforms.

> **Note:** Currently only tested on Claude Code and OpenCode. Please report issues for Codex and Gemini. With opencode you may have better performance with https://www.npmjs.com/package/opencode-skills (this is what I use).

- https://github.com/numman-ali/openskills (I have not tried this yet)
- Requested feature in opencode https://github.com/sst/opencode/issues/3235

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Comprehensive guide for using skills with Gemini CLI, Copilot CLI, and Codex CLI
- **[Examples Summary](EXAMPLES_SUMMARY.md)** - Overview of all example skills included

## Features

- **Install/Uninstall**: Easily manage skills and commands
- **Search**: Find skills by keywords and descriptions
- **Create**: Interactive wizard for creating new skills and commands
- **Validate**: Ensure skills and commands meet format requirements
- **Multi-platform**: Support for OpenCode, Claude Code, Codex, Gemini, GitHub Copilot, and MCP
- **Agent Export**: Export canonical agent configurations to platform-specific instruction files

## Installation

### Using uv (recommended)

```bash
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Quick Start

### Configure Repository Path

First, set up the path to your skills repository:

```bash
skillz config set repository /path/to/skillz
```

### List Available Skills

```bash
# List all skills and commands
skillz list

# List only skills
skillz list --type skill

# List only from repository
skillz list --source repository
```

### Install a Skill

```bash
# Install to OpenCode (default)
skillz install skill-name

# Install to Claude Code
skillz install skill-name --platform claude

# Install to project directory (.opencode/skills/)
skillz install skill-name --target project

# Preview before installing
skillz install skill-name --dry-run
```

### Search for Skills

```bash
skillz search python
skillz search "lab notebook"
```

### Create a New Skill

```bash
# Interactive mode
skillz create --type skill

# With name specified
skillz create --type skill --name my-awesome-skill
```

### Uninstall a Skill

```bash
skillz uninstall skill-name
```

### Export Agent Configuration

Export agent configurations from the canonical specification (`.ai/agents/agents.yaml`) to platform-specific instruction files:

```bash
# Export default agent to Codex CLI (creates AGENTS.md)
skillz export --platform codex

# Export default agent to Gemini CLI (creates GEMINI.md)
skillz export --platform gemini

# Export default agent to Copilot CLI (creates .github/copilot-instructions.md)
skillz export --platform copilot

# Export review agent instead of default
skillz export --platform codex --agent review

# Specify custom output location
skillz export --platform codex --output /path/to/output.md
```

**Default Output Locations:**
- **Codex CLI**: `./AGENTS.md`
- **Gemini CLI**: `./GEMINI.md`
- **Copilot CLI**: `./.github/copilot-instructions.md`

## Configuration

Configuration is stored in `~/.config/skillz/config.yaml`.

Default configuration:

```yaml
default_platform: opencode

personal_skills_dir: ~/.config/opencode/skills
personal_commands_dir: ~/.config/opencode/command
project_skills_dir: .opencode/skills
project_commands_dir: .opencode/command
default_target: personal

platforms:
  opencode:
    skills_dir: ~/.config/opencode/skills
    commands_dir: ~/.config/opencode/command
  claude:
    skills_dir: ~/.claude/skills
    commands_dir: ~/.claude/commands
  codex:
    skills_dir: ~/.codex/skills
    commands_dir: ~/.codex/commands
  gemini:
    skills_dir: ~/.config/gemini/skills
    commands_dir: ~/.config/gemini/commands
  copilot:
    skills_dir: .github/skills
    commands_dir: .github/commands
  mcp:
    skills_dir: ~/.config/mcp/skills
    commands_dir: ~/.config/mcp/commands
```

## Canonical Agent Specification

Skillz uses a centralized agent specification system that allows you to define AI agents once and export them to multiple platform-specific formats.

### Agent Configuration File

The canonical agent specification is stored in `.ai/agents/agents.yaml`. This file defines:

- **Version**: Specification version
- **Capabilities**: Available agent capabilities with descriptions
- **Roles**: Reusable role definitions with capabilities and policies
- **Agents**: Individual agent configurations

### Example agents.yaml

```yaml
version: "1.0"

capabilities:
  skill-management:
    description: "Manage AI assistant skills and slash commands"
  validation:
    description: "Validate skill and command formats"

roles:
  skill-manager:
    default-capabilities:
      - skill-management
      - validation
    policies: |
      # Skill Manager Role Policies
      - Always validate skills before installation
      - Follow platform-specific conventions

agents:
  - id: default
    name: "Default Skillz Agent"
    role: skill-manager
    policies: |
      # Default Agent Policies
      - Use personal installation target by default
      - Provide helpful prompts for missing configuration
  
  - id: review
    name: "Skillz Review Agent"
    role: reviewer
    policies: |
      # Review Agent Policies
      - Focus on validation and quality checks
      - Provide comprehensive validation reports
```

### Global Policies

Repository-wide policies can be defined in `.ai/policies/global.md`. These policies are included in all exported agent configurations.

### Exporting Agent Configurations

The `export` command reads the canonical specification and generates platform-specific instruction files:

```bash
# Export to Codex CLI
skillz export --platform codex

# Export to Gemini CLI
skillz export --platform gemini

# Export to GitHub Copilot
skillz export --platform copilot

# Use a specific agent
skillz export --platform codex --agent review
```

### Capability Downgrade

Since not all platforms support capability enforcement, capabilities are automatically rendered as plain-text policies in the exported files. This ensures compatibility across all platforms while maintaining clear documentation of agent capabilities.

## Skills Format

Skills are directories containing a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: A clear description of what this skill does and when to use it
allowed-tools: ["*"]  # Optional: restrict available tools
---

# Skill Content

Detailed instructions for Claude on how to use this skill...
```

### Requirements

- `name`: lowercase, hyphens only, max 64 characters
- `description`: clear explanation, max 1024 characters
- Directory must contain `SKILL.md`

## Commands Format

Commands are markdown files with optional YAML frontmatter:

```markdown
---
description: Brief description for /help
model: sonnet  # Optional: sonnet, opus, or haiku
allowed-tools: ["*"]  # Optional
argument-hint: <your-arg>  # Optional: autocomplete help
---

# Command Content

Command prompt content here...

Use $ARGUMENTS or $1, $2, etc. for parameters.
```

## Project Structure

```
skillz/
├── cli/                    # Python CLI tool
│   ├── commands/          # CLI command implementations
│   ├── config.py          # Configuration management
│   ├── validator.py       # Skill/command validation
│   └── utils.py           # Helper functions
├── skills/                # Skill repository
│   ├── academic/
│   ├── programming/
│   └── research/
├── commands/              # Command repository
├── templates/             # Templates for new skills
└── tests/                 # Test suite
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to automatically run linting and formatting checks before each commit. The hooks will:

- Run `ruff check --fix` to fix linting issues
- Run `ruff format` to format code

If any changes are made by the hooks, the commit will fail. Simply stage the changes and commit again.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=cli --cov-report=html
```

### Linting and Formatting

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting:

```bash
# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Check formatting
ruff format --check .

# Format code
ruff format .
```

## Available Skills

See the `skills/` directory for available skills organized by category:

- **Academic**: PhD qualifier review, proposal assistance
- **Programming**: Python (ASE, pymatgen), Emacs Lisp
- **Research**: Electronic lab notebook management

## Contributing

Contributions are welcome! Please:

1. Follow the skill/command format requirements
2. Add tests for new functionality
3. Update documentation
4. Run linters before submitting

## License

MIT License - see LICENSE file for details

## Support

- Report issues: https://github.com/jkitchin/skillz/issues
- Documentation: https://github.com/jkitchin/skillz#readme

## Related Projects

### Supported Platforms

Skillz manages skills and commands for these AI coding assistants:

- **[OpenCode](https://github.com/sst/opencode)** - The AI coding agent built for the terminal. Open-source, provider-agnostic, with 30k+ GitHub stars.
- **[Claude Code](https://github.com/anthropics/claude-code)** - Anthropic's agentic coding tool that lives in your terminal. Understands your codebase and helps you code faster.
- **[Codex CLI](https://github.com/openai/codex)** - OpenAI's lightweight coding agent that runs in your terminal. See [OpenAI adopts "skills"](https://simonwillison.net/2025/Dec/12/openai-skills/) for details on their skills implementation.
- **[GitHub Copilot](https://github.com/features/copilot)** - AI pair programmer that helps you write code faster and with less effort. Uses project-level skills in `.github/skills/` directories.
- **[MCP (Model Context Protocol)](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)** - Protocol for connecting AI assistants to external tools and data sources. Supported by Docker Desktop, Claude Desktop, and other MCP-compatible clients.
- **Gemini** - Google's AI assistant for code generation and assistance.

### Related Skills Projects

- **[Superpowers](https://github.com/obra/superpowers)** - A complete software development workflow framework for Claude Code with composable skills for design, TDD, code review, and integration. This project was an early motivation to develop this project.

## Credits

Created by John Kitchin for managing AI assistant skills across different LLM platforms.
