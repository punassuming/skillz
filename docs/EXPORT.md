# Export Feature Documentation

The `skillz export` command provides a standardized way to generate platform-specific instruction files for various AI coding assistants (Codex CLI, Gemini CLI, GitHub Copilot CLI) from a single canonical source.

## Overview

Instead of maintaining separate hand-written instruction files (e.g., `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`) that can drift out of sync, the export feature allows you to:

1. Maintain a single source of truth in `.ai/config.yaml`
2. Define global policies and coding standards once
3. Select which skills and commands to include
4. Generate platform-specific files automatically
5. Keep all platform files in sync

## Quick Start

```bash
# Configure repository path (one-time setup)
skillz config set repository /path/to/skillz

# Export for all platforms
skillz export --platform codex
skillz export --platform gemini
skillz export --platform copilot

# Preview what would be exported
skillz export --platform codex --dry-run
```

## Canonical Configuration (`.ai/config.yaml`)

The `.ai/config.yaml` file is the platform-neutral source of truth for your project's AI assistant configuration.

### Example Configuration

```yaml
# Global project instructions and policies
policies:
  - name: code-quality
    description: Maintain high code quality standards
    content: |
      - Write clean, readable, and maintainable code
      - Follow language-specific conventions and best practices
      - Include proper error handling and input validation
      - Write comprehensive documentation and comments where needed

  - name: testing
    description: Testing requirements
    content: |
      - Write tests for new features and bug fixes
      - Maintain test coverage above 80%
      - Run tests before committing changes
      - Include both unit and integration tests where appropriate

# Skills to include in exports
skills:
  include_all: true  # Include all skills by default
  exclude: []        # Optionally exclude specific skills

# Commands to include in exports
commands:
  include_all: true  # Include all commands by default
  exclude: []        # Optionally exclude specific commands

# Profiles for different use cases
profiles:
  minimal:
    description: Minimal set of essential skills
    policies: [code-quality]
    skills:
      include_all: false
      include: []
    commands:
      include_all: false
      include: []
  
  full:
    description: All available skills and commands
    policies: [code-quality, testing]
    skills:
      include_all: true
    commands:
      include_all: true

# Platform-specific configurations
platforms:
  codex:
    output: AGENTS.md
    enabled: true
  
  gemini:
    output: GEMINI.md
    enabled: true
  
  copilot:
    output: .github/copilot-instructions.md
    enabled: true
```

### Configuration Options

#### Policies

Policies define project-wide instructions and coding standards:

```yaml
policies:
  - name: policy-name
    description: Brief description
    content: |
      Multi-line content with
      instructions and guidelines
```

#### Skills Filter

Control which skills from `skills/` are included:

```yaml
skills:
  include_all: true           # Include all skills
  exclude: [skill1, skill2]   # Exclude specific skills

# OR

skills:
  include_all: false          # Include only specific skills
  include: [skill3, skill4]   # List skills to include
```

Skills are referenced by their relative path from the `skills/` directory (e.g., `python/pycse`, `scientific/design-of-experiments`).

#### Commands Filter

Control which commands from `commands/` are included:

```yaml
commands:
  include_all: true                    # Include all commands
  exclude: [examples/old-command]      # Exclude specific commands

# OR

commands:
  include_all: false                   # Include only specific commands
  include: [examples/review-pr]        # List commands to include
```

Commands are referenced by their relative path from the `commands/` directory without the `.md` extension.

#### Profiles

Profiles allow different configurations for different scenarios:

```yaml
profiles:
  minimal:
    description: Minimal set for quick iteration
    policies: [code-quality]
    skills:
      include_all: false
      include: [python/basics]
    commands:
      include_all: false
      include: [examples/review-pr]
  
  full:
    description: Complete set with all features
    policies: [code-quality, testing, security]
    skills:
      include_all: true
    commands:
      include_all: true
  
  data-science:
    description: Data science focused configuration
    policies: [code-quality, documentation]
    skills:
      include_all: false
      include: [python/pycse, scientific/design-of-experiments]
    commands:
      include_all: false
      include: [examples/explain-code]
```

## Command Usage

### Basic Export

```bash
# Export for Codex CLI
skillz export --platform codex

# Export for Gemini CLI
skillz export --platform gemini

# Export for GitHub Copilot CLI
skillz export --platform copilot
```

### Using Profiles

```bash
# Export with minimal profile
skillz export --platform codex --profile minimal

# Export with full profile
skillz export --platform gemini --profile full

# Export with custom profile
skillz export --platform copilot --profile data-science
```

### Custom Output Path

```bash
# Specify custom output location
skillz export --platform codex --output custom/AGENTS.md

# Export to different directory
skillz export --platform gemini --output docs/ai/GEMINI.md
```

### Dry Run

Preview what would be exported without writing files:

```bash
skillz export --platform codex --dry-run
```

This shows:
- Number of policies included
- List of skills (first 5 with description)
- List of commands (first 5)
- Where the file would be written

### Verbose Output

```bash
skillz -v export --platform codex
```

Shows additional information:
- Platform being exported to
- Profile being used
- Source location
- Repository path

## Generated File Format

All generated files include:

### 1. Generated File Header

```markdown
<!-- 
  ⚠️  GENERATED FILE - DO NOT EDIT BY HAND ⚠️
  
  This file was automatically generated by: skillz export --platform codex
  Generated on: 2025-12-23 21:33:10
  Source: .ai/config.yaml
  
  To regenerate this file, run:
    skillz export --platform codex
  
  To modify the content, edit:
    - Policies: .ai/config.yaml
    - Skills: skills/**/SKILL.md
    - Commands: commands/**/*.md
-->
```

### 2. Project Policies

All configured policies with their content.

### 3. Skills Index

A table of contents listing all included skills with:
- Skill name
- Description
- Source file location

### 4. Skills Reference

Full content of each skill, including:
- Skill name and source path
- Complete skill content (from SKILL.md)

### 5. Commands Reference

All included commands with:
- Command name
- Description (if provided)
- Usage hint (if provided)
- Source file location
- Full command content

## Platform-Specific Conventions

### Codex CLI

- **Default Output**: `AGENTS.md` in repository root
- **Format**: Markdown with H1/H2 headers
- **Convention**: Codex CLI reads `AGENTS.md` for project-level instructions

### Gemini CLI

- **Default Output**: `GEMINI.md` in repository root
- **Format**: Markdown with sections
- **Convention**: Gemini CLI can read custom instruction files

### GitHub Copilot CLI

- **Default Output**: `.github/copilot-instructions.md`
- **Format**: Markdown with structured sections
- **Note**: GitHub Copilot CLI support for custom instruction files may vary by version
- **Convention**: This follows the pattern of storing GitHub-specific configs in `.github/`

**Important**: While GitHub Copilot supports workspace/repository context, the specific file name and location conventions may vary. The default `.github/copilot-instructions.md` is a reasonable convention that keeps Copilot instructions alongside other GitHub configuration.

## Deterministic Output

The export command produces deterministic output to ensure stable diffs:

- Skills are sorted alphabetically by name
- Commands are sorted alphabetically by name
- Policies maintain the order defined in `.ai/config.yaml`
- All content is rendered consistently

This means:
- Multiple exports produce identical output (excluding timestamps)
- Git diffs show only actual content changes
- Easy to review changes in version control

## Version Control Recommendations

### What to Commit

**DO commit:**
- `.ai/config.yaml` - Your canonical configuration
- Skills in `skills/` directory
- Commands in `commands/` directory

**CONSIDER committing (for user reference):**
- Generated files (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`)
  - Pros: Users can see current state without running export
  - Cons: Duplicates information, can get out of sync
  - Recommendation: Commit generated files but regenerate frequently

**DO NOT manually edit:**
- Generated instruction files
  - They include a warning header
  - Changes will be overwritten on next export
  - Edit `.ai/config.yaml` or source skills/commands instead

### Suggested Workflow

1. **Make changes**:
   ```bash
   # Edit policies
   vim .ai/config.yaml
   
   # Update skills
   vim skills/python/my-skill/SKILL.md
   
   # Modify commands
   vim commands/examples/my-command.md
   ```

2. **Regenerate exports**:
   ```bash
   skillz export --platform codex
   skillz export --platform gemini
   skillz export --platform copilot
   ```

3. **Review and commit**:
   ```bash
   git diff
   git add .ai/config.yaml skills/ commands/ *.md .github/
   git commit -m "Update AI assistant configuration"
   ```

### CI/CD Integration

Add a check to ensure generated files are up to date:

```yaml
# .github/workflows/check-exports.yml
name: Check Exports

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install skillz
        run: pip install -e ".[templates]"
      
      - name: Configure repository
        run: skillz config set repository .
      
      - name: Generate exports
        run: |
          skillz export --platform codex
          skillz export --platform gemini
          skillz export --platform copilot
      
      - name: Check for changes
        run: |
          if ! git diff --quiet; then
            echo "Generated files are out of date. Run 'skillz export' locally."
            git diff
            exit 1
          fi
```

## Troubleshooting

### "Repository path not configured"

```bash
skillz config set repository /path/to/skillz/repo
```

### ".ai/config.yaml not found"

The export command will work with defaults, but for best results:

```bash
# Create .ai directory
mkdir .ai

# Copy example config
cp example-config.yaml .ai/config.yaml

# Edit as needed
vim .ai/config.yaml
```

### "No skills found"

Ensure:
- Skills are in `skills/` directory relative to repository path
- Each skill has a `SKILL.md` file
- Skills have valid YAML frontmatter

### Template not found

Ensure you installed with the templates extra:

```bash
pip install -e ".[templates]"
```

### Generated file is too large

Use profiles to reduce content:

```yaml
profiles:
  lite:
    skills:
      include_all: false
      include: [essential-skill-1, essential-skill-2]
```

Then export with profile:

```bash
skillz export --platform codex --profile lite
```

## Examples

### Example 1: Minimal Configuration for Quick Projects

```yaml
# .ai/config.yaml
policies:
  - name: basics
    description: Basic coding standards
    content: |
      - Write clear, readable code
      - Comment complex logic

skills:
  include_all: false
  include: [python/basics]

commands:
  include_all: false
  include: [examples/review-pr]

profiles:
  minimal:
    policies: [basics]
    skills:
      include_all: false
      include: [python/basics]
    commands:
      include_all: false
      include: []
```

### Example 2: Data Science Project

```yaml
# .ai/config.yaml
policies:
  - name: data-science-standards
    description: Data science best practices
    content: |
      - Document data sources and transformations
      - Include reproducible examples
      - Use version control for notebooks
      - Validate data quality

skills:
  include_all: false
  include:
    - python/pycse
    - scientific/design-of-experiments
    - laboratory/eln

commands:
  include_all: false
  include:
    - examples/explain-code
    - examples/review-pr

platforms:
  codex:
    output: docs/ai/CODEX.md
  gemini:
    output: docs/ai/GEMINI.md
```

### Example 3: Enterprise Project with Multiple Profiles

```yaml
# .ai/config.yaml
policies:
  - name: security
    description: Security requirements
    content: |
      - No secrets in code
      - Validate all inputs
      - Use parameterized queries
  
  - name: code-review
    description: Code review standards
    content: |
      - All code must be reviewed
      - Automated tests required
      - Documentation must be updated

skills:
  include_all: true
  exclude:
    - experimental/alpha-feature
    - deprecated/old-api

commands:
  include_all: true

profiles:
  dev:
    description: Development environment
    policies: [code-review]
    skills:
      include_all: true
      exclude: [production/monitoring]
    commands:
      include_all: true
  
  prod:
    description: Production environment
    policies: [security, code-review]
    skills:
      include_all: false
      include: [production/monitoring, production/deployment]
    commands:
      include_all: false
      include: [production/deploy, production/rollback]

platforms:
  codex:
    output: AGENTS.md
  gemini:
    output: GEMINI.md
  copilot:
    output: .github/copilot-instructions.md
```

## Advanced Topics

### Custom Templates

You can customize the export templates by modifying files in `templates/export/`:

- `templates/export/codex/agents.md.j2` - Codex CLI template
- `templates/export/gemini/gemini.md.j2` - Gemini CLI template
- `templates/export/copilot/copilot.md.j2` - Copilot CLI template

Templates use Jinja2 syntax and have access to:
- `platform` - Target platform name
- `generation_date` - Timestamp
- `source_config` - Path to config file
- `profile` - Profile name (if used)
- `policies` - List of policy dictionaries
- `skills` - List of skill dictionaries
- `commands` - List of command dictionaries

### Extending Support to New Platforms

To add support for a new platform:

1. Create template: `templates/export/newplatform/template.md.j2`
2. Add platform to `ExportManager.SUPPORTED_PLATFORMS` in `cli/export/exporter.py`
3. Add template mapping in `_render_template()` method
4. Update documentation

## FAQ

**Q: Can I use export without `.ai/config.yaml`?**  
A: Yes, defaults will be used (all skills and commands included, no policies).

**Q: Can I export only specific skills?**  
A: Yes, use the `include` list in skills configuration or create a profile.

**Q: Are generated files platform-specific?**  
A: Templates are tailored to each platform's conventions, but content is the same.

**Q: Can I customize the output format?**  
A: Yes, modify the Jinja2 templates in `templates/export/`.

**Q: Should I commit generated files?**  
A: It's recommended for reference, but regenerate frequently to keep in sync.

**Q: Can I use this with CI/CD?**  
A: Yes, see the CI/CD Integration section above.

**Q: What if my platform isn't supported?**  
A: Create a custom template and submit a PR, or use a similar platform's format.
