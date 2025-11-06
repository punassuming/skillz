"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_dir(temp_dir):
    """Create a mock config directory."""
    config_dir = temp_dir / ".config" / "claude-skills"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def mock_skills_dir(temp_dir):
    """Create a mock skills directory with a sample skill."""
    skills_dir = temp_dir / "skills"
    skills_dir.mkdir()

    # Create a valid skill
    skill_dir = skills_dir / "test-skill"
    skill_dir.mkdir()

    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: A test skill for unit testing
allowed-tools: "*"
---

# Test Skill

This is a test skill.
""")

    return skills_dir


@pytest.fixture
def mock_commands_dir(temp_dir):
    """Create a mock commands directory with a sample command."""
    commands_dir = temp_dir / "commands"
    commands_dir.mkdir()

    # Create a valid command
    cmd_file = commands_dir / "test-command.md"
    cmd_file.write_text("""---
description: A test command
---

# Test Command

This is a test command with $ARGUMENTS.
""")

    return commands_dir


@pytest.fixture
def mock_repository(temp_dir):
    """Create a mock repository with skills and commands."""
    repo_dir = temp_dir / "repository"
    repo_dir.mkdir()

    # Create skills directory
    skills_dir = repo_dir / "skills"
    skills_dir.mkdir()

    skill_dir = skills_dir / "sample-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: sample-skill
description: A sample skill for testing
allowed-tools: ["Read", "Write"]
---

# Sample Skill
""")

    # Create commands directory
    commands_dir = repo_dir / "commands"
    commands_dir.mkdir()

    cmd_file = commands_dir / "sample-command.md"
    cmd_file.write_text("""---
description: A sample command for testing
---

# Sample Command
""")

    return repo_dir
