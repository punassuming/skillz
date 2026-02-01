# Agents

This directory contains Claude Code agents (subagents) - specialized AI assistants that handle specific tasks independently.

## File Format

Each agent is a single `.md` file with YAML frontmatter:

```yaml
---
name: agent-name
description: Brief description of what this agent does
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

## Agent Properties

- **name** - Lowercase with hyphens, max 64 chars (required)
- **description** - What the agent does, when to use it (required)
- **tools** - Comma-separated list of allowed tools (optional, default: all)
- **model** - Model to use: `sonnet`, `opus`, `haiku` (optional)
- **disallowedTools** - Tools to explicitly disallow (optional)

## Available Models

| Model | Best For |
|-------|----------|
| `haiku` | Fast, simple tasks, cost-sensitive |
| `sonnet` | Balanced performance (default) |
| `opus` | Complex reasoning, high-stakes decisions |

## Creating an Agent

Use the template or run:
```bash
skillz agents create my-agent --model sonnet
```

See `templates/AGENT_TEMPLATE.md` for full documentation.
