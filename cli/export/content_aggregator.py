"""Aggregate skills and commands for export."""

import re
from pathlib import Path
from typing import Any, Dict, List

import yaml

from cli.utils import find_command_files, find_skill_directories


class ContentAggregator:
    """Aggregates skills and commands for export."""

    def __init__(self, repository_path: Path):
        """
        Initialize with repository path.

        Args:
            repository_path: Path to the skills repository
        """
        self.repository_path = repository_path

    def aggregate_skills(self, filter_config: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Aggregate skills based on filter configuration.

        Args:
            filter_config: Dictionary with include_all, include, and exclude

        Returns:
            List of skill dictionaries with name, description, content, and source_path
        """
        skills_dir = self.repository_path / "skills"
        if not skills_dir.exists():
            return []

        all_skill_dirs = find_skill_directories(skills_dir)
        skills = []

        for skill_dir in sorted(all_skill_dirs):
            # Get relative path from skills directory
            rel_path = skill_dir.relative_to(skills_dir)
            skill_key = str(rel_path).replace("\\", "/")

            # Check if should be included
            if not self._should_include(skill_key, filter_config):
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue

            # Parse skill
            skill_data = self._parse_skill_file(skill_file)
            if skill_data:
                skill_data["source_path"] = str(skill_file.relative_to(self.repository_path))
                skills.append(skill_data)

        # Sort by name for deterministic ordering
        return sorted(skills, key=lambda x: x["name"])

    def aggregate_commands(self, filter_config: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Aggregate commands based on filter configuration.

        Args:
            filter_config: Dictionary with include_all, include, and exclude

        Returns:
            List of command dictionaries with name, description, content, and source_path
        """
        commands_dir = self.repository_path / "commands"
        if not commands_dir.exists():
            return []

        all_command_files = find_command_files(commands_dir)
        commands = []

        for command_file in sorted(all_command_files):
            # Get relative path from commands directory
            rel_path = command_file.relative_to(commands_dir)
            # Remove .md extension for key
            command_key = str(rel_path.with_suffix("")).replace("\\", "/")

            # Check if should be included
            if not self._should_include(command_key, filter_config):
                continue

            # Parse command
            command_data = self._parse_command_file(command_file)
            if command_data:
                command_data["source_path"] = str(
                    command_file.relative_to(self.repository_path)
                )
                commands.append(command_data)

        # Sort by name for deterministic ordering
        return sorted(commands, key=lambda x: x["name"])

    def _should_include(self, item_key: str, filter_config: Dict[str, Any]) -> bool:
        """
        Check if item should be included based on filter config.

        Args:
            item_key: Relative path key for the item
            filter_config: Filter configuration

        Returns:
            True if item should be included
        """
        exclude_list = filter_config.get("exclude", [])
        if item_key in exclude_list:
            return False

        include_all = filter_config.get("include_all", True)
        if include_all:
            return True

        include_list = filter_config.get("include", [])
        return item_key in include_list

    def _parse_skill_file(self, skill_file: Path) -> Dict[str, str]:
        """
        Parse a SKILL.md file.

        Args:
            skill_file: Path to SKILL.md

        Returns:
            Dictionary with name, description, and content
        """
        try:
            with open(skill_file) as f:
                content = f.read()

            frontmatter = self._parse_frontmatter(content)
            if not frontmatter:
                return {}

            # Remove frontmatter from content
            content_without_frontmatter = self._remove_frontmatter(content)

            return {
                "name": frontmatter.get("name", ""),
                "description": frontmatter.get("description", ""),
                "content": content_without_frontmatter.strip(),
            }
        except Exception:
            return {}

    def _parse_command_file(self, command_file: Path) -> Dict[str, str]:
        """
        Parse a command markdown file.

        Args:
            command_file: Path to command file

        Returns:
            Dictionary with name, description, content, and optional argument_hint
        """
        try:
            with open(command_file) as f:
                content = f.read()

            frontmatter = self._parse_frontmatter(content)
            content_without_frontmatter = self._remove_frontmatter(content)

            # Use filename without extension as name
            name = command_file.stem

            result = {
                "name": name,
                "description": "",
                "content": content_without_frontmatter.strip(),
            }

            if frontmatter:
                result["description"] = frontmatter.get("description", "")
                if "argument-hint" in frontmatter:
                    result["argument_hint"] = frontmatter["argument-hint"]

            return result
        except Exception:
            return {}

    @staticmethod
    def _parse_frontmatter(content: str) -> Dict[str, Any]:
        """Parse YAML frontmatter from markdown content."""
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return {}

        frontmatter_str = match.group(1)
        try:
            return yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError:
            return {}

    @staticmethod
    def _remove_frontmatter(content: str) -> str:
        """Remove frontmatter from content."""
        pattern = r"^---\s*\n.*?\n---\s*\n"
        return re.sub(pattern, "", content, count=1, flags=re.DOTALL)
