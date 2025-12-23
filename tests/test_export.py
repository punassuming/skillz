"""Tests for export command."""

from pathlib import Path

import pytest
import yaml

from cli.commands.export import (
    _discover_commands,
    _discover_skills,
    _find_agent,
    _get_default_output_path,
    _render_template,
)


class TestExportCommand:
    """Tests for export command."""

    def test_get_default_output_path_codex(self, temp_dir):
        """Test default output path for Codex."""
        path = _get_default_output_path("codex", temp_dir)
        assert path == temp_dir / "AGENTS.md"

    def test_get_default_output_path_gemini(self, temp_dir):
        """Test default output path for Gemini."""
        path = _get_default_output_path("gemini", temp_dir)
        assert path == temp_dir / "GEMINI.md"

    def test_get_default_output_path_copilot(self, temp_dir):
        """Test default output path for Copilot."""
        path = _get_default_output_path("copilot", temp_dir)
        assert path == temp_dir / ".github" / "copilot-instructions.md"

    def test_find_agent_default(self):
        """Test finding default agent."""
        agents_config = {
            "agents": [
                {"id": "default", "name": "Default Agent"},
                {"id": "review", "name": "Review Agent"},
            ]
        }
        agent = _find_agent(agents_config, "default")
        assert agent is not None
        assert agent["id"] == "default"
        assert agent["name"] == "Default Agent"

    def test_find_agent_review(self):
        """Test finding review agent."""
        agents_config = {
            "agents": [
                {"id": "default", "name": "Default Agent"},
                {"id": "review", "name": "Review Agent"},
            ]
        }
        agent = _find_agent(agents_config, "review")
        assert agent is not None
        assert agent["id"] == "review"
        assert agent["name"] == "Review Agent"

    def test_find_agent_not_found(self):
        """Test finding non-existent agent."""
        agents_config = {"agents": [{"id": "default", "name": "Default Agent"}]}
        agent = _find_agent(agents_config, "nonexistent")
        assert agent is None

    def test_discover_skills(self, temp_dir):
        """Test skill discovery."""
        # Create a skills directory with some skills
        skills_dir = temp_dir / "skills"
        skills_dir.mkdir()

        # Create skill 1
        skill1 = skills_dir / "skill-one"
        skill1.mkdir()
        (skill1 / "SKILL.md").write_text(
            """---
name: skill-one
description: First test skill
---
# Skill One
"""
        )

        # Create skill 2
        skill2 = skills_dir / "skill-two"
        skill2.mkdir()
        (skill2 / "SKILL.md").write_text(
            """---
name: skill-two
description: Second test skill
---
# Skill Two
"""
        )

        skills = _discover_skills(temp_dir)
        assert len(skills) == 2
        assert skills[0]["name"] == "skill-one"
        assert skills[1]["name"] == "skill-two"
        assert skills[0]["description"] == "First test skill"
        assert skills[1]["description"] == "Second test skill"

    def test_discover_commands(self, temp_dir):
        """Test command discovery."""
        # Create a commands directory with some commands
        commands_dir = temp_dir / "commands"
        commands_dir.mkdir()

        # Create command 1
        (commands_dir / "cmd-one.md").write_text(
            """---
description: First test command
---
# Command One
"""
        )

        # Create command 2 (without frontmatter)
        (commands_dir / "cmd-two.md").write_text(
            """# Command Two

No frontmatter here.
"""
        )

        commands = _discover_commands(temp_dir)
        assert len(commands) == 2
        assert commands[0]["name"] == "cmd-one"
        assert commands[1]["name"] == "cmd-two"
        assert commands[0]["description"] == "First test command"
        assert commands[1]["description"] == ""

    def test_discover_skills_deterministic_ordering(self, temp_dir):
        """Test that skills are discovered in deterministic order."""
        skills_dir = temp_dir / "skills"
        skills_dir.mkdir()

        # Create skills in random order
        for name in ["zebra-skill", "alpha-skill", "middle-skill"]:
            skill_dir = skills_dir / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                f"""---
name: {name}
description: Test skill {name}
---
# {name}
"""
            )

        skills = _discover_skills(temp_dir)
        assert len(skills) == 3
        # Should be sorted alphabetically
        assert skills[0]["name"] == "alpha-skill"
        assert skills[1]["name"] == "middle-skill"
        assert skills[2]["name"] == "zebra-skill"

    def test_discover_commands_deterministic_ordering(self, temp_dir):
        """Test that commands are discovered in deterministic order."""
        commands_dir = temp_dir / "commands"
        commands_dir.mkdir()

        # Create commands in random order
        for name in ["zebra-cmd", "alpha-cmd", "middle-cmd"]:
            (commands_dir / f"{name}.md").write_text(f"# {name}")

        commands = _discover_commands(temp_dir)
        assert len(commands) == 3
        # Should be sorted alphabetically
        assert commands[0]["name"] == "alpha-cmd"
        assert commands[1]["name"] == "middle-cmd"
        assert commands[2]["name"] == "zebra-cmd"

    def test_render_template_includes_capabilities_as_policies(self):
        """Test that capabilities are rendered as policies (downgrade behavior)."""
        agent_config = {
            "id": "test-agent",
            "name": "Test Agent",
            "role": "test-role",
            "policies": "Agent policies here",
        }
        agents_config = {
            "capabilities": {
                "cap1": {"description": "First capability"},
                "cap2": {"description": "Second capability"},
            },
            "roles": {
                "test-role": {
                    "default-capabilities": ["cap1", "cap2"],
                    "policies": "Role policies here",
                }
            },
        }

        content = _render_template(
            platform="codex",
            agent_config=agent_config,
            agents_config=agents_config,
            global_policies="Global policies here",
            role_policies="Role policies here",
            skills=[],
            commands=[],
            repo_path=Path("/tmp"),
        )

        # Check that capabilities are rendered as text policies
        assert "## Capabilities" in content
        assert "cap1" in content
        assert "First capability" in content
        assert "cap2" in content
        assert "Second capability" in content

    def test_render_template_includes_header(self):
        """Test that rendered template includes auto-generated header."""
        agent_config = {
            "id": "test",
            "name": "Test",
            "role": "test-role",
            "policies": "",
        }
        agents_config = {"roles": {"test-role": {"default-capabilities": []}}}

        content = _render_template(
            platform="codex",
            agent_config=agent_config,
            agents_config=agents_config,
            global_policies="",
            role_policies="",
            skills=[],
            commands=[],
            repo_path=Path("/tmp"),
        )

        assert "AUTO-GENERATED" in content
        assert ".ai/agents/agents.yaml" in content
        assert "DO NOT EDIT" in content

    def test_render_template_different_agent_identities(self):
        """Test that different agents have different identities in output."""
        agents_config = {"roles": {"role1": {"default-capabilities": []}}}

        # Agent 1
        agent1_config = {
            "id": "agent1",
            "name": "Agent One",
            "role": "role1",
            "policies": "Policies for agent 1",
        }
        content1 = _render_template(
            platform="codex",
            agent_config=agent1_config,
            agents_config=agents_config,
            global_policies="",
            role_policies="",
            skills=[],
            commands=[],
            repo_path=Path("/tmp"),
        )

        # Agent 2
        agent2_config = {
            "id": "agent2",
            "name": "Agent Two",
            "role": "role1",
            "policies": "Policies for agent 2",
        }
        content2 = _render_template(
            platform="codex",
            agent_config=agent2_config,
            agents_config=agents_config,
            global_policies="",
            role_policies="",
            skills=[],
            commands=[],
            repo_path=Path("/tmp"),
        )

        # Different agent names
        assert "Agent One" in content1
        assert "Agent Two" in content2
        assert "Agent One" not in content2
        assert "Agent Two" not in content1

        # Different agent IDs
        assert "**Agent ID**: agent1" in content1
        assert "**Agent ID**: agent2" in content2

        # Different policies
        assert "Policies for agent 1" in content1
        assert "Policies for agent 2" in content2

    def test_render_template_includes_skills_and_commands(self):
        """Test that rendered template includes skills and commands."""
        agent_config = {"id": "test", "name": "Test", "role": "test-role", "policies": ""}
        agents_config = {"roles": {"test-role": {"default-capabilities": []}}}

        skills = [
            {"name": "skill1", "description": "Skill 1 desc", "path": Path("skills/skill1")},
            {"name": "skill2", "description": "Skill 2 desc", "path": Path("skills/skill2")},
        ]

        commands = [
            {
                "name": "cmd1",
                "description": "Command 1 desc",
                "path": Path("commands/cmd1.md"),
            },
            {"name": "cmd2", "description": "", "path": Path("commands/cmd2.md")},
        ]

        content = _render_template(
            platform="codex",
            agent_config=agent_config,
            agents_config=agents_config,
            global_policies="",
            role_policies="",
            skills=skills,
            commands=commands,
            repo_path=Path("/tmp"),
        )

        # Check skills
        assert "# Available Skills" in content
        assert "skill1" in content
        assert "Skill 1 desc" in content
        assert "skill2" in content
        assert "Skill 2 desc" in content

        # Check commands
        assert "# Available Commands" in content
        assert "cmd1" in content
        assert "Command 1 desc" in content
        assert "cmd2" in content


@pytest.fixture
def mock_agents_yaml(temp_dir):
    """Create a mock agents.yaml file."""
    ai_dir = temp_dir / ".ai" / "agents"
    ai_dir.mkdir(parents=True)

    agents_yaml = ai_dir / "agents.yaml"
    agents_data = {
        "version": "1.0",
        "capabilities": {
            "test-cap": {"description": "Test capability"},
        },
        "roles": {
            "test-role": {
                "default-capabilities": ["test-cap"],
                "policies": "Test role policies",
            }
        },
        "agents": [
            {
                "id": "default",
                "name": "Default Agent",
                "role": "test-role",
                "policies": "Default agent policies",
            },
            {
                "id": "review",
                "name": "Review Agent",
                "role": "test-role",
                "policies": "Review agent policies",
            },
        ],
    }

    with open(agents_yaml, "w") as f:
        yaml.safe_dump(agents_data, f)

    return temp_dir
