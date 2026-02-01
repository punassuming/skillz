# Hooks

This directory contains Claude Code hooks - shell commands that execute at various points in Claude Code's lifecycle.

## Directory Structure

Each hook is a directory containing:
- `HOOK.md` - Required file with YAML frontmatter (name, description, event, matcher, type, timeout)
- `hook.py` or `hook.sh` - The executable hook script

## Hook Events

- **PreToolUse** - Before tool calls (can block)
- **PostToolUse** - After tool completes
- **PermissionRequest** - When permission dialogs appear (can block)
- **UserPromptSubmit** - When user submits prompt (can block)
- **Notification** - When Claude sends notifications
- **Stop** - When Claude finishes responding (can block)
- **SubagentStop** - When subagent completes (can block)
- **PreCompact** - Before context compaction
- **SessionStart** - When session starts
- **SessionEnd** - When session ends

## Creating a Hook

Use the template or run:
```bash
skillz hooks create my-hook --event PostToolUse
```

See `templates/HOOK_TEMPLATE.md` for full documentation.
