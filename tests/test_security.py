"""Tests for security-related utility functions."""


import pytest

from cli.config import VALID_PLATFORMS, InvalidPlatformError, validate_platform
from cli.utils import PathTraversalError, safe_path_join


class TestSafePathJoin:
    """Tests for safe_path_join function."""

    def test_normal_path(self, tmp_path):
        """Test normal path joining works."""
        base = tmp_path / "base"
        base.mkdir()

        result = safe_path_join(base, "subdir")
        assert result == base.resolve() / "subdir"

    def test_path_traversal_blocked(self, tmp_path):
        """Test that path traversal attempts are blocked."""
        base = tmp_path / "base"
        base.mkdir()

        with pytest.raises(PathTraversalError):
            safe_path_join(base, "../etc/passwd")

    def test_double_traversal_blocked(self, tmp_path):
        """Test multiple traversal attempts are blocked."""
        base = tmp_path / "base"
        base.mkdir()

        with pytest.raises(PathTraversalError):
            safe_path_join(base, "../../secrets")

    def test_valid_nested_path(self, tmp_path):
        """Test valid nested paths work."""
        base = tmp_path / "base"
        base.mkdir()

        result = safe_path_join(base, "level1/level2/level3")
        assert str(result).startswith(str(base.resolve()))

    def test_simple_name(self, tmp_path):
        """Test simple names work."""
        base = tmp_path / "skills"
        base.mkdir()

        result = safe_path_join(base, "my-skill")
        assert result == base.resolve() / "my-skill"

    def test_symlink_to_outside_blocked(self, tmp_path):
        """Test symlinks pointing outside base are blocked."""
        base = tmp_path / "base"
        base.mkdir()

        # Create a symlink pointing outside base
        outside = tmp_path / "outside"
        outside.mkdir()
        link = base / "escape-link"
        link.symlink_to(outside)

        # The symlink target resolves outside base, so it should be blocked
        with pytest.raises(PathTraversalError):
            safe_path_join(base, "escape-link")

    def test_path_with_dots_in_name(self, tmp_path):
        """Test that paths with dots in the name (not traversal) work."""
        base = tmp_path / "base"
        base.mkdir()

        # A name with a dot that's not traversal
        result = safe_path_join(base, "my.skill.v2")
        assert result == base.resolve() / "my.skill.v2"


class TestValidatePlatform:
    """Tests for validate_platform function."""

    def test_valid_platforms(self):
        """Test all valid platforms are accepted."""
        for platform in VALID_PLATFORMS:
            result = validate_platform(platform)
            assert result == platform.lower()

    def test_case_insensitive(self):
        """Test platform validation is case-insensitive."""
        assert validate_platform("CLAUDE") == "claude"
        assert validate_platform("Claude") == "claude"
        assert validate_platform("OPENCODE") == "opencode"

    def test_invalid_platform_raises(self):
        """Test invalid platforms raise error."""
        with pytest.raises(InvalidPlatformError):
            validate_platform("gpt")

        with pytest.raises(InvalidPlatformError):
            validate_platform("unknown")

        with pytest.raises(InvalidPlatformError):
            validate_platform("")

    def test_error_message_includes_valid_options(self):
        """Test error message includes valid platform options."""
        try:
            validate_platform("invalid")
            assert False, "Should have raised"
        except InvalidPlatformError as e:
            error_msg = str(e)
            assert "claude" in error_msg
            assert "opencode" in error_msg
            assert "codex" in error_msg
            assert "gemini" in error_msg


class TestConfigMethods:
    """Tests for new Config methods."""

    def test_get_hooks_dir_personal(self):
        """Test getting personal hooks directory."""
        from cli.config import Config

        config = Config()
        hooks_dir = config.get_hooks_dir(target="personal", platform="claude")
        assert "hooks" in str(hooks_dir)

    def test_get_hooks_dir_project(self):
        """Test getting project hooks directory."""
        from cli.config import Config

        config = Config()
        hooks_dir = config.get_hooks_dir(target="project", platform="claude")
        assert "hooks" in str(hooks_dir)

    def test_get_agents_dir_personal(self):
        """Test getting personal agents directory."""
        from cli.config import Config

        config = Config()
        agents_dir = config.get_agents_dir(target="personal", platform="claude")
        assert "agents" in str(agents_dir)

    def test_get_agents_dir_project(self):
        """Test getting project agents directory."""
        from cli.config import Config

        config = Config()
        agents_dir = config.get_agents_dir(target="project", platform="claude")
        assert "agents" in str(agents_dir)

    def test_get_settings_file(self):
        """Test getting settings file path."""
        from cli.config import Config

        config = Config()
        settings = config.get_settings_file(target="personal", platform="claude")
        assert "settings.json" in str(settings)

    def test_platform_specific_dirs(self):
        """Test different platforms have different directories."""
        from cli.config import Config

        config = Config()

        claude_hooks = config.get_hooks_dir(target="personal", platform="claude")
        opencode_hooks = config.get_hooks_dir(target="personal", platform="opencode")

        # They should be different
        assert claude_hooks != opencode_hooks


class TestFindFunctions:
    """Tests for find_hook_directories and find_agent_files."""

    def test_find_hook_directories(self, tmp_path):
        """Test finding hook directories."""
        from cli.utils import find_hook_directories

        # Create hook directories
        hook1 = tmp_path / "hook1"
        hook1.mkdir()
        (hook1 / "HOOK.md").write_text("# Hook 1")

        hook2 = tmp_path / "nested" / "hook2"
        hook2.mkdir(parents=True)
        (hook2 / "HOOK.md").write_text("# Hook 2")

        hooks = find_hook_directories(tmp_path)
        assert len(hooks) == 2
        assert hook1 in hooks
        assert hook2 in hooks

    def test_find_hook_directories_empty(self, tmp_path):
        """Test finding hooks in empty directory."""
        from cli.utils import find_hook_directories

        hooks = find_hook_directories(tmp_path)
        assert len(hooks) == 0

    def test_find_hook_directories_nonexistent(self, tmp_path):
        """Test finding hooks in nonexistent directory."""
        from cli.utils import find_hook_directories

        hooks = find_hook_directories(tmp_path / "nonexistent")
        assert len(hooks) == 0

    def test_find_agent_files(self, tmp_path):
        """Test finding agent files."""
        from cli.utils import find_agent_files

        # Create agent files
        (tmp_path / "agent1.md").write_text("# Agent 1")
        (tmp_path / "nested").mkdir()
        (tmp_path / "nested" / "agent2.md").write_text("# Agent 2")

        agents = find_agent_files(tmp_path)
        assert len(agents) == 2

    def test_find_agent_files_ignores_readme(self, tmp_path):
        """Test that README.md is ignored."""
        from cli.utils import find_agent_files

        (tmp_path / "agent1.md").write_text("# Agent 1")
        (tmp_path / "README.md").write_text("# README")
        (tmp_path / "readme.md").write_text("# readme")

        agents = find_agent_files(tmp_path)
        assert len(agents) == 1
        assert "agent1.md" in str(agents[0])
