# Install --all Option Design

**Date:** 2025-11-08
**Feature:** Add `--all` flag to install command for batch installation

## Overview

Add a `--all` option to the `claude-skills install` command that installs all available skills and commands from the repository in a single operation.

## Requirements

### Functional Requirements
- Install all skills and commands from repository with single command
- Skip items that are already installed (no overwrite)
- Stop immediately on first validation or installation error
- Support existing `--target` and `--platform` options
- Support `--dry-run` to preview what would be installed

### Non-Functional Requirements
- Reuse existing validation and installation logic
- Minimal changes to existing code (~30-40 lines)
- Clear progress feedback during installation
- Predictable installation order (skills first, then commands)

### Constraints
- `--all` and NAME argument are mutually exclusive
- No category filtering support (install everything or nothing)
- `--force` flag ignored (always skip existing items)
- `--type` flag ignored (always install both skills and commands)

## Architecture

### Command Signature Changes

**Before:**
```python
@click.command()
@click.argument("name")
@click.option("--target", ...)
@click.option("--platform", ...)
@click.option("--type", "item_type", ...)
@click.option("--force", ...)
@click.option("--dry-run", ...)
def install(ctx, name, target, platform, item_type, force, dry_run):
```

**After:**
```python
@click.command()
@click.argument("name", required=False)
@click.option("--target", ...)
@click.option("--platform", ...)
@click.option("--type", "item_type", ...)
@click.option("--force", ...)
@click.option("--dry-run", ...)
@click.option("--all", is_flag=True, help="Install all skills and commands")
def install(ctx, name, target, platform, item_type, force, dry_run, all):
```

### Control Flow

```
install()
├─ Validate: require either NAME or --all (not both, not neither)
├─ Get repository path
├─ if --all:
│  └─ install_all_items()
│     ├─ Discover all skills and commands
│     ├─ Print summary count
│     ├─ if --dry-run: show list and exit
│     ├─ For each skill:
│     │  ├─ Check if exists → skip
│     │  ├─ Validate → abort on error
│     │  └─ Install → abort on error
│     └─ For each command:
│        ├─ Check if exists → skip
│        ├─ Validate → abort on error
│        └─ Install → abort on error
└─ else:
   └─ (existing single-item installation logic)
```

### New Functions

**`install_all_items()`**
- Parameters: `repo_path, config, target, platform, dry_run, verbose`
- Discovers all skills and commands from repository
- Handles dry-run preview
- Loops through items with validation and installation
- Prints progress for each item

**`_discover_all_skills()`**
- Parameters: `repo_path`
- Returns: list of Path objects to skill directories
- Uses existing `find_skill_directories()` utility

**`_discover_all_commands()`**
- Parameters: `repo_path`
- Returns: list of Path objects to command files
- Uses existing `find_command_files()` utility

## Implementation Details

### Discovery Mechanism
- Reuse `find_skill_directories()` from `cli.utils`
- Reuse `find_command_files()` from `cli.utils`
- Scan `repo_path/skills/` for all SKILL.md files
- Scan `repo_path/commands/` for all .md files

### Validation
- For skills: use existing `SkillValidator.validate_skill_directory()`
- For commands: use existing `CommandValidator.validate_command_file()`
- Stop immediately on first validation error

### Installation
- For skills: use existing `copy_directory()` utility
- For commands: use existing `copy_file()` utility
- Stop immediately on first copy error

### Handling Existing Items
- Check if destination path exists before validation
- Print yellow warning: "Skipping skill 'name' (already installed)"
- Continue to next item

### Error Handling
- Validation error: print error details and `raise click.Abort()`
- Copy error: bubble up exception (will abort)
- Missing repository: handled by existing code before --all branch

## User Feedback

### Dry Run Output
```
Would install the following items:

Skills (12):
  - pymatgen [new]
  - literature-review [exists]
  - troubleshooting [new]
  ...

Commands (3):
  - analyze [new]
  - summarize [exists]
  ...
```

### Installation Progress
```
Found 12 skills and 3 commands

[green]Installed skill 'pymatgen'[/green]
[yellow]Skipping skill 'literature-review' (already installed)[/yellow]
[green]Installed skill 'troubleshooting'[/green]
...
[green]Installed command 'analyze'[/green]
[yellow]Skipping command 'summarize' (already installed)[/yellow]
...
```

### Error Output
```
Found 12 skills and 3 commands

[green]Installed skill 'pymatgen'[/green]
[green]Installed skill 'troubleshooting'[/green]
[red]Error: Invalid skill 'broken-skill'[/red]
  - Missing required field: name
  - Invalid frontmatter format
Aborted!
```

## Flag Interactions

| Flag | Behavior with --all |
|------|---------------------|
| `--target` | Respected (determines installation location) |
| `--platform` | Respected (determines platform subdirectory) |
| `--force` | Ignored (we always skip existing items) |
| `--dry-run` | Respected (shows preview without installing) |
| `--type` | Ignored (always installs both skills and commands) |
| `--verbose` | Respected (shows additional debug info) |

## Testing Considerations

1. **Basic functionality**: `--all` installs all items
2. **Dry run**: `--all --dry-run` shows preview
3. **Skip existing**: Already installed items are skipped
4. **Validation error**: Invalid item stops installation
5. **Mutual exclusivity**: `--all` with NAME argument fails
6. **Missing argument**: No NAME and no `--all` fails
7. **Target/platform**: `--all --target project` uses correct location
8. **Empty repository**: Handles zero skills/commands gracefully

## Future Enhancements (Out of Scope)

- Continue on errors (collect failures, report at end)
- Category filtering with `--all --category research`
- Progress bar for large installations
- `--update-all` to reinstall existing items
- Parallel installation for performance

## Implementation Estimate

- Lines added: ~40-50
- Lines modified: ~5-10
- Complexity: Low (reuses all existing logic)
- Risk: Low (isolated to new code path)
