"""Tests for export module."""

from pathlib import Path

import pytest

from cli.export import ExportManager
from cli.export.config_loader import AIConfig
from cli.export.content_aggregator import ContentAggregator


class TestAIConfig:
    """Tests for AIConfig."""

    def test_load_default_config_when_missing(self, temp_dir):
        """Test loading default config when file doesn't exist."""
        config_path = temp_dir / "nonexistent.yaml"
        ai_config = AIConfig(config_path)

        assert ai_config.config is not None
        assert "policies" in ai_config.config
        assert "skills" in ai_config.config
        assert "commands" in ai_config.config

    def test_load_existing_config(self, temp_dir):
        """Test loading an existing config file."""
        config_path = temp_dir / "config.yaml"
        config_path.write_text(
            """
policies:
  - name: test-policy
    description: Test policy
    content: Test content

skills:
  include_all: true
  exclude: []

commands:
  include_all: false
  include: [test-command]
"""
        )

        ai_config = AIConfig(config_path)
        policies = ai_config.get_policies()

        assert len(policies) == 1
        assert policies[0]["name"] == "test-policy"

    def test_get_policies_with_profile(self, temp_dir):
        """Test getting policies with a profile."""
        config_path = temp_dir / "config.yaml"
        config_path.write_text(
            """
policies:
  - name: policy1
    description: First policy
    content: Content 1
  - name: policy2
    description: Second policy
    content: Content 2

profiles:
  minimal:
    policies: [policy1]
"""
        )

        ai_config = AIConfig(config_path)
        policies = ai_config.get_policies("minimal")

        assert len(policies) == 1
        assert policies[0]["name"] == "policy1"

    def test_get_default_output(self, temp_dir):
        """Test getting default output paths."""
        config_path = temp_dir / "config.yaml"
        config_path.write_text(
            """
platforms:
  codex:
    output: CUSTOM_AGENTS.md
"""
        )

        ai_config = AIConfig(config_path)

        # Custom output from config
        assert ai_config.get_default_output("codex") == "CUSTOM_AGENTS.md"

        # Fallback defaults
        assert ai_config.get_default_output("gemini") == "GEMINI.md"
        assert ai_config.get_default_output("copilot") == ".github/copilot-instructions.md"


class TestContentAggregator:
    """Tests for ContentAggregator."""

    def test_aggregate_skills(self, mock_skills_dir):
        """Test aggregating skills."""
        aggregator = ContentAggregator(mock_skills_dir.parent)
        filter_config = {"include_all": True, "exclude": []}

        skills = aggregator.aggregate_skills(filter_config)

        assert len(skills) > 0
        assert all("name" in skill for skill in skills)
        assert all("description" in skill for skill in skills)
        assert all("content" in skill for skill in skills)
        assert all("source_path" in skill for skill in skills)

    def test_aggregate_skills_with_exclude(self, mock_skills_dir):
        """Test aggregating skills with exclusion."""
        aggregator = ContentAggregator(mock_skills_dir.parent)

        # First, get all skills to know what to exclude
        all_skills_filter = {"include_all": True, "exclude": []}
        all_skills = aggregator.aggregate_skills(all_skills_filter)

        if len(all_skills) > 0:
            # Exclude first skill
            first_skill_name = all_skills[0]["name"]
            skill_dir_name = mock_skills_dir / first_skill_name

            filter_config = {"include_all": True, "exclude": [first_skill_name]}
            filtered_skills = aggregator.aggregate_skills(filter_config)

            assert len(filtered_skills) == len(all_skills) - 1

    def test_aggregate_skills_deterministic_order(self, mock_skills_dir):
        """Test that skills are returned in deterministic order."""
        aggregator = ContentAggregator(mock_skills_dir.parent)
        filter_config = {"include_all": True, "exclude": []}

        skills1 = aggregator.aggregate_skills(filter_config)
        skills2 = aggregator.aggregate_skills(filter_config)

        # Compare names to ensure same order
        names1 = [s["name"] for s in skills1]
        names2 = [s["name"] for s in skills2]

        assert names1 == names2

    def test_aggregate_commands(self, temp_dir):
        """Test aggregating commands."""
        commands_dir = temp_dir / "commands"
        commands_dir.mkdir()

        # Create test command
        cmd_file = commands_dir / "test-command.md"
        cmd_file.write_text(
            """---
description: Test command
argument-hint: <input>
---

# Test Command

This is a test command.
"""
        )

        aggregator = ContentAggregator(temp_dir)
        filter_config = {"include_all": True, "exclude": []}

        commands = aggregator.aggregate_commands(filter_config)

        assert len(commands) == 1
        assert commands[0]["name"] == "test-command"
        assert commands[0]["description"] == "Test command"
        assert "argument_hint" in commands[0]


class TestExportManager:
    """Tests for ExportManager."""

    def test_export_codex(self, mock_skills_dir, temp_dir):
        """Test exporting for Codex platform."""
        # Create .ai/config.yaml
        ai_dir = mock_skills_dir.parent / ".ai"
        ai_dir.mkdir(exist_ok=True)
        config_path = ai_dir / "config.yaml"
        config_path.write_text(
            """
policies:
  - name: test-policy
    description: Test policy
    content: Policy content

skills:
  include_all: true

commands:
  include_all: true

platforms:
  codex:
    output: test-output/AGENTS.md
"""
        )

        manager = ExportManager(mock_skills_dir.parent, config_path)
        output_path = manager.export("codex")

        assert Path(output_path).exists()
        content = Path(output_path).read_text()

        # Verify generated file contains expected sections
        assert "GENERATED FILE" in content
        assert "DO NOT EDIT BY HAND" in content
        assert "Project Policies" in content
        assert "Skills Index" in content
        assert "test-skill" in content  # From mock_skills_dir fixture

    def test_export_gemini(self, mock_skills_dir, temp_dir):
        """Test exporting for Gemini platform."""
        ai_dir = mock_skills_dir.parent / ".ai"
        ai_dir.mkdir(exist_ok=True)
        config_path = ai_dir / "config.yaml"
        config_path.write_text(
            """
policies: []
skills:
  include_all: true
commands:
  include_all: true
platforms:
  gemini:
    output: test-output/GEMINI.md
"""
        )

        manager = ExportManager(mock_skills_dir.parent, config_path)
        output_path = manager.export("gemini")

        assert Path(output_path).exists()
        content = Path(output_path).read_text()

        assert "GENERATED FILE" in content
        assert "Gemini" in content

    def test_export_copilot(self, mock_skills_dir, temp_dir):
        """Test exporting for Copilot platform."""
        ai_dir = mock_skills_dir.parent / ".ai"
        ai_dir.mkdir(exist_ok=True)
        config_path = ai_dir / "config.yaml"
        config_path.write_text(
            """
policies: []
skills:
  include_all: true
commands:
  include_all: true
platforms:
  copilot:
    output: test-output/copilot.md
"""
        )

        manager = ExportManager(mock_skills_dir.parent, config_path)
        output_path = manager.export("copilot")

        assert Path(output_path).exists()
        content = Path(output_path).read_text()

        assert "GENERATED FILE" in content
        assert "Copilot" in content

    def test_export_unsupported_platform(self, mock_skills_dir):
        """Test exporting with unsupported platform."""
        manager = ExportManager(mock_skills_dir.parent)

        with pytest.raises(ValueError, match="not supported"):
            manager.export("unsupported-platform")

    def test_export_deterministic_output(self, mock_skills_dir, temp_dir):
        """Test that exports produce deterministic output."""
        ai_dir = mock_skills_dir.parent / ".ai"
        ai_dir.mkdir(exist_ok=True)
        config_path = ai_dir / "config.yaml"
        config_path.write_text(
            """
policies: []
skills:
  include_all: true
commands:
  include_all: true
"""
        )

        manager = ExportManager(mock_skills_dir.parent, config_path)

        # Export twice
        output1_path = manager.export("codex", "test1.md")
        output2_path = manager.export("codex", "test2.md")

        content1 = Path(output1_path).read_text()
        content2 = Path(output2_path).read_text()

        # Remove timestamp lines for comparison
        def remove_timestamps(text):
            lines = text.split("\n")
            return "\n".join(
                [line for line in lines if "Generated on:" not in line and "Last" not in line]
            )

        assert remove_timestamps(content1) == remove_timestamps(content2)

    def test_export_with_profile(self, mock_skills_dir, temp_dir):
        """Test exporting with a profile."""
        ai_dir = mock_skills_dir.parent / ".ai"
        ai_dir.mkdir(exist_ok=True)
        config_path = ai_dir / "config.yaml"
        config_path.write_text(
            """
policies:
  - name: policy1
    description: First policy
    content: Content 1
  - name: policy2
    description: Second policy
    content: Content 2

profiles:
  minimal:
    policies: [policy1]
    skills:
      include_all: false
      include: []
    commands:
      include_all: false
      include: []

skills:
  include_all: true

commands:
  include_all: true
"""
        )

        manager = ExportManager(mock_skills_dir.parent, config_path)
        output_path = manager.export("codex", "minimal.md", profile="minimal")

        content = Path(output_path).read_text()

        # Should only have policy1
        assert "policy1" in content.lower()
        assert "policy2" not in content.lower()
