# Global Policies for Skillz

## Repository Structure

- Skills are organized in `skills/` directory with subdirectories by category
- Commands are organized in `commands/` directory
- Each skill must have a `SKILL.md` file with YAML frontmatter
- Commands are individual markdown files with optional frontmatter

## Naming Conventions

- Skill and command names must be lowercase
- Use hyphens to separate words (e.g., `python-ase`, `lab-notebook`)
- Maximum length: 64 characters for names
- No special characters except hyphens and numbers

## Validation Requirements

- Skills must have `name` and `description` in frontmatter
- Description maximum length: 1024 characters for skills, 256 for commands
- `allowed-tools` field is optional and can be `["*"]` for all tools
- Valid tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch, TodoWrite, AskUserQuestion, Skill, SlashCommand, NotebookEdit, BashOutput, KillShell

## Platform Support

- OpenCode: Default platform, uses `~/.config/opencode/` directory
- Claude Code: Uses `~/.claude/` directory
- Codex CLI: Uses `~/.codex/` directory with `AGENTS.md` config
- Gemini CLI: Uses `~/.config/gemini/` directory with `GEMINI.md` config
- GitHub Copilot: Uses `.github/` directory with `copilot-instructions.md` config
- MCP: Uses `~/.config/mcp/` directory

## Installation Targets

- **Personal**: Install to user-level platform directory
- **Project**: Install to project-level directory (e.g., `.opencode/`)

## Best Practices

- Always validate before installation
- Use `--dry-run` to preview changes
- Provide clear error messages with actionable suggestions
- Maintain backward compatibility
- Document platform-specific requirements
