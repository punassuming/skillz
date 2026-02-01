"""Tests for HookValidator and AgentValidator."""



from cli.validator import AgentValidator, HookValidator


class TestHookValidator:
    """Tests for HookValidator."""

    def test_valid_hook_directory(self, tmp_path):
        """Test validation of a valid hook directory."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        # Create HOOK.md
        hook_md = hook_dir / "HOOK.md"
        hook_md.write_text("""---
name: my-hook
description: A test hook
event: PreToolUse
---

# My Hook

This hook does something useful.
""")

        # Create hook script
        hook_script = hook_dir / "hook.py"
        hook_script.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n")

        is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
        assert is_valid, f"Expected valid but got errors: {errors}"
        assert len(errors) == 0

    def test_missing_hook_md(self, tmp_path):
        """Test validation fails when HOOK.md is missing."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
        assert not is_valid
        assert any("Missing HOOK.md" in err for err in errors)

    def test_missing_script(self, tmp_path):
        """Test validation fails when no script is present."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        # Create HOOK.md but no script
        hook_md = hook_dir / "HOOK.md"
        hook_md.write_text("""---
name: my-hook
description: A test hook
event: PreToolUse
---

# My Hook
""")

        is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
        assert not is_valid
        assert any("No hook script" in err for err in errors)

    def test_invalid_event(self, tmp_path):
        """Test validation fails for invalid event."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        hook_md = hook_dir / "HOOK.md"
        hook_md.write_text("""---
name: my-hook
description: A test hook
event: InvalidEvent
---

# My Hook
""")

        hook_script = hook_dir / "hook.py"
        hook_script.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n")

        is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
        assert not is_valid
        assert any("Invalid event" in err for err in errors)

    def test_valid_events(self, tmp_path):
        """Test all valid events are accepted."""
        valid_events = [
            "PreToolUse",
            "PostToolUse",
            "PermissionRequest",
            "UserPromptSubmit",
            "Notification",
            "Stop",
            "SubagentStop",
            "PreCompact",
            "SessionStart",
            "SessionEnd",
        ]

        for event in valid_events:
            hook_dir = tmp_path / f"hook-{event.lower()}"
            hook_dir.mkdir()

            hook_md = hook_dir / "HOOK.md"
            hook_md.write_text(f"""---
name: hook-{event.lower()}
description: Test hook for {event}
event: {event}
---

# Hook
""")

            hook_script = hook_dir / "hook.py"
            hook_script.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n")

            is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
            assert is_valid, f"Event {event} should be valid, got errors: {errors}"

    def test_description_too_long(self, tmp_path):
        """Test validation fails for description over 256 chars."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        long_desc = "x" * 257

        hook_md = hook_dir / "HOOK.md"
        hook_md.write_text(f"""---
name: my-hook
description: {long_desc}
event: PreToolUse
---

# My Hook
""")

        hook_script = hook_dir / "hook.py"
        hook_script.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n")

        is_valid, errors = HookValidator.validate_hook_directory(hook_dir)
        assert not is_valid
        assert any("Description too long" in err for err in errors)

    def test_get_hook_metadata(self, tmp_path):
        """Test extracting metadata from hook."""
        hook_dir = tmp_path / "my-hook"
        hook_dir.mkdir()

        hook_md = hook_dir / "HOOK.md"
        hook_md.write_text("""---
name: my-hook
description: A test hook
event: PreToolUse
matcher: Bash
timeout: 30
---

# My Hook
""")

        metadata = HookValidator.get_hook_metadata(hook_dir)
        assert metadata is not None
        assert metadata["name"] == "my-hook"
        assert metadata["event"] == "PreToolUse"
        assert metadata["matcher"] == "Bash"
        assert metadata["timeout"] == 30


class TestAgentValidator:
    """Tests for AgentValidator."""

    def test_valid_agent(self, tmp_path):
        """Test validation of a valid agent file."""
        agent_file = tmp_path / "code-reviewer.md"
        agent_file.write_text("""---
name: code-reviewer
description: Reviews code for quality and security issues
tools: Read, Grep, Glob
model: sonnet
---

# Code Reviewer

You are a code review specialist.
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert is_valid, f"Expected valid but got errors: {errors}"

    def test_missing_name(self, tmp_path):
        """Test validation fails when name is missing."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
description: An agent
---

# Agent
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert not is_valid
        assert any("Missing required field: name" in err for err in errors)

    def test_missing_description(self, tmp_path):
        """Test validation fails when description is missing."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
---

# Agent
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert not is_valid
        assert any("Missing required field: description" in err for err in errors)

    def test_invalid_model(self, tmp_path):
        """Test validation fails for invalid model."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
description: An agent
model: gpt-4
---

# Agent
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert not is_valid
        assert any("Invalid model" in err for err in errors)

    def test_valid_models(self, tmp_path):
        """Test all valid models are accepted."""
        valid_models = ["sonnet", "opus", "haiku"]

        for model in valid_models:
            agent_file = tmp_path / f"agent-{model}.md"
            agent_file.write_text(f"""---
name: agent-{model}
description: Agent using {model}
model: {model}
---

# Agent
""")

            is_valid, errors = AgentValidator.validate_agent_file(agent_file)
            assert is_valid, f"Model {model} should be valid, got errors: {errors}"

    def test_invalid_tool(self, tmp_path):
        """Test validation fails for unknown tool."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
description: An agent
tools: Read, UnknownTool, Grep
---

# Agent
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert not is_valid
        assert any("Unknown tool" in err for err in errors)

    def test_empty_content(self, tmp_path):
        """Test validation fails for empty agent content."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
description: An agent
---
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert not is_valid
        assert any("empty" in err.lower() for err in errors)

    def test_get_agent_metadata(self, tmp_path):
        """Test extracting metadata from agent."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
description: Test agent
tools: Read, Grep
model: haiku
---

# Agent
""")

        metadata = AgentValidator.get_agent_metadata(agent_file)
        assert metadata is not None
        assert metadata["name"] == "my-agent"
        assert metadata["model"] == "haiku"
        assert metadata["tools"] == "Read, Grep"

    def test_tools_as_list(self, tmp_path):
        """Test tools can be specified as a list."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
name: my-agent
description: An agent
tools:
  - Read
  - Grep
  - Glob
---

# Agent
""")

        is_valid, errors = AgentValidator.validate_agent_file(agent_file)
        assert is_valid, f"Expected valid but got errors: {errors}"
