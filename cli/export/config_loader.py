"""Load and parse .ai/config.yaml."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class AIConfig:
    """Loads and provides access to .ai/config.yaml."""

    def __init__(self, config_path: Path):
        """
        Initialize with path to .ai/config.yaml.

        Args:
            config_path: Path to the .ai/config.yaml file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_path.exists():
            # Return minimal default config
            return {
                "policies": [],
                "skills": {"include_all": True, "exclude": []},
                "commands": {"include_all": True, "exclude": []},
                "profiles": {},
                "platforms": {},
            }

        with open(self.config_path) as f:
            return yaml.safe_load(f) or {}

    def get_policies(self, profile: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get policies to include in export.

        Args:
            profile: Optional profile name to use

        Returns:
            List of policy dictionaries with name, description, and content
        """
        if profile and profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][profile]
            policy_names = profile_config.get("policies", [])
            all_policies = self.config.get("policies", [])
            return [p for p in all_policies if p.get("name") in policy_names]

        return self.config.get("policies", [])

    def get_skills_filter(self, profile: Optional[str] = None) -> Dict[str, Any]:
        """
        Get skills filter configuration.

        Args:
            profile: Optional profile name to use

        Returns:
            Dictionary with include_all, include, and exclude lists
        """
        if profile and profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][profile]
            return profile_config.get("skills", {"include_all": True, "exclude": []})

        return self.config.get("skills", {"include_all": True, "exclude": []})

    def get_commands_filter(self, profile: Optional[str] = None) -> Dict[str, Any]:
        """
        Get commands filter configuration.

        Args:
            profile: Optional profile name to use

        Returns:
            Dictionary with include_all, include, and exclude lists
        """
        if profile and profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][profile]
            return profile_config.get("commands", {"include_all": True, "exclude": []})

        return self.config.get("commands", {"include_all": True, "exclude": []})

    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """
        Get platform-specific configuration.

        Args:
            platform: Platform name (codex, gemini, copilot)

        Returns:
            Dictionary with platform configuration (output, enabled, etc.)
        """
        return self.config.get("platforms", {}).get(platform, {})

    def get_default_output(self, platform: str) -> str:
        """
        Get default output filename for platform.

        Args:
            platform: Platform name

        Returns:
            Default output filename
        """
        platform_config = self.get_platform_config(platform)
        if "output" in platform_config:
            return platform_config["output"]

        # Fallback defaults
        defaults = {
            "codex": "AGENTS.md",
            "gemini": "GEMINI.md",
            "copilot": ".github/copilot-instructions.md",
        }
        return defaults.get(platform, f"{platform.upper()}.md")
