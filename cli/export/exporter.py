"""Main exporter for generating platform-specific files."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template

from cli.export.config_loader import AIConfig
from cli.export.content_aggregator import ContentAggregator


class ExportManager:
    """Manages export of skills and commands to platform-specific formats."""

    SUPPORTED_PLATFORMS = ["codex", "gemini", "copilot"]

    def __init__(
        self, repository_path: Path, ai_config_path: Optional[Path] = None, templates_dir: Optional[Path] = None
    ):
        """
        Initialize export manager.

        Args:
            repository_path: Path to skills repository
            ai_config_path: Path to .ai/config.yaml (defaults to repository_path/.ai/config.yaml)
            templates_dir: Path to templates directory
        """
        self.repository_path = repository_path

        if ai_config_path is None:
            ai_config_path = repository_path / ".ai" / "config.yaml"
        self.ai_config = AIConfig(ai_config_path)

        if templates_dir is None:
            # Assume templates are in the same structure as the CLI
            templates_dir = Path(__file__).parent.parent.parent / "templates"
        self.templates_dir = templates_dir

        self.aggregator = ContentAggregator(repository_path)

    def export(
        self,
        platform: str,
        output: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> str:
        """
        Export to platform-specific format.

        Args:
            platform: Target platform (codex, gemini, copilot)
            output: Output file path (optional, uses default from config if not provided)
            profile: Profile name to use (optional)

        Returns:
            Path to generated file

        Raises:
            ValueError: If platform is not supported
        """
        if platform not in self.SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Platform '{platform}' not supported. "
                f"Supported platforms: {', '.join(self.SUPPORTED_PLATFORMS)}"
            )

        # Determine output path
        if output is None:
            output = self.ai_config.get_default_output(platform)
        output_path = self.repository_path / output

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Gather content
        context = self._build_context(platform, profile)

        # Render template
        rendered = self._render_template(platform, context)

        # Write output
        with open(output_path, "w") as f:
            f.write(rendered)

        return str(output_path)

    def _build_context(self, platform: str, profile: Optional[str] = None) -> Dict[str, Any]:
        """
        Build context for template rendering.

        Args:
            platform: Target platform
            profile: Optional profile name

        Returns:
            Dictionary with all context data for templates
        """
        # Get filters
        skills_filter = self.ai_config.get_skills_filter(profile)
        commands_filter = self.ai_config.get_commands_filter(profile)

        # Aggregate content
        policies = self.ai_config.get_policies(profile)
        skills = self.aggregator.aggregate_skills(skills_filter)
        commands = self.aggregator.aggregate_commands(commands_filter)

        # Build context
        return {
            "platform": platform,
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_config": str(self.ai_config.config_path.relative_to(self.repository_path)),
            "profile": profile,
            "policies": policies,
            "skills": skills,
            "commands": commands,
        }

    def _render_template(self, platform: str, context: Dict[str, Any]) -> str:
        """
        Render template for platform.

        Args:
            platform: Target platform
            context: Template context

        Returns:
            Rendered content
        """
        # Map platforms to template files
        template_map = {
            "codex": "export/codex/agents.md.j2",
            "gemini": "export/gemini/gemini.md.j2",
            "copilot": "export/copilot/copilot.md.j2",
        }

        template_name = template_map.get(platform)
        if not template_name:
            raise ValueError(f"No template found for platform: {platform}")

        # Load and render template
        env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        template = env.get_template(template_name)
        return template.render(**context)
