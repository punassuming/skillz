# Quick Reference: Using Skills with AI CLI Tools

## Installation Commands

```bash
# Install skillz
uv pip install -e .
skillz config set repository /path/to/skillz

# Install AI CLI tools
npm install -g @google/gemini-cli      # Gemini
npm install -g @github/copilot         # Copilot
npm install -g @openai/codex           # Codex
```

## Basic Workflow

```bash
# 1. Find a skill
skillz search tdd

# 2. View examples
skillz info tdd

# 3. Install to platform
skillz install tdd --platform gemini

# 4. Use in CLI
gemini-cli "Help me practice TDD"
```

## Platform-Specific Quick Start

### Gemini CLI

```bash
# Install skill
skillz install tdd --platform gemini

# Use skill
gemini-cli "Guide me through test-driven development"

# Agentic workflow
gemini-cli "Use TDD to build a calculator: write tests, implement, refactor"
```

### GitHub Copilot

```bash
# Install to project
cd ~/project
skillz install code-reviewer --platform copilot --target project

# Use skill
gh copilot suggest "Review my code for bugs"

# Agent mode
gh copilot agent "Review code, find bugs, suggest fixes"
```

### Codex CLI

```bash
# Install skill
skillz install scientific-writing --platform codex

# Use skill
codex "Help me write a better abstract"

# Multi-agent
codex agents run --agent writer:scientific-writing --task "Write introduction"
```

## Common Patterns

### Pattern 1: Development Workflow

```bash
# Install skills
skillz install tdd code-reviewer version-control --platform gemini

# Run workflow
gemini-cli "Build new feature using TDD, review code, commit properly"
```

### Pattern 2: Optimization

```bash
# Install skill
skillz install python-optimization --platform copilot

# Execute
gh copilot agent "Profile code, find bottlenecks, optimize, benchmark"
```

### Pattern 3: Research & Writing

```bash
# Install skills
skillz install literature-review scientific-writing --platform codex

# Execute
codex "Research topic, synthesize findings, write introduction section"
```

## Skill Examples Reference

| Skill | Example File | Use Case |
|-------|-------------|----------|
| tdd | `tdd-session-string-calculator.md` | Test-driven development |
| code-reviewer | `sample-code-review.md` | Bug detection & review |
| version-control | `git-workflow-feature-development.md` | Git workflows |
| literature-review | `ml-materials-literature-review.md` | Systematic research |
| scientific-writing | `research-paper-sections.md` | Academic writing |
| image-generation | `prompt-examples.md` | AI image prompts |
| python-optimization | `optimization-workflow.md` | Performance tuning |

## Troubleshooting

```bash
# Check installation
skillz list --source personal

# Verify platform directory
ls ~/.config/gemini/skills/        # Gemini
ls .github/skills/                 # Copilot (project)
ls ~/.config/codex/skills/         # Codex

# Reinstall
skillz uninstall skill-name
skillz install skill-name --platform gemini --force
```

## Tips

- Reference example files in prompts: "Use examples/tdd-session-string-calculator.md"
- Enable agent mode for autonomous workflows
- Install only relevant skills to your work
- Combine multiple skills for complex tasks

## Full Documentation

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for comprehensive documentation.
