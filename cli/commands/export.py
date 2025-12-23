"""Export command for generating agent configuration files."""

import sys
from pathlib import Path
from typing import Dict, List, Optional

import click
import yaml
from rich.console import Console

from cli.config import Config
from cli.utils import find_command_files, find_skill_directories

console = Console()


@click.command()
@click.option(
    "--platform",
    "-p",
    type=click.Choice(["codex", "gemini", "copilot"]),
    required=True,
    help="Target platform (codex, gemini, or copilot)",
)
@click.option(
    "--agent",
    "-a",
    default="default",
    help="Agent ID from agents.yaml (default: 'default')",
)
@click.option(
    "--profile",
    help="Profile name for multiple configurations (optional)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: platform-specific location)",
)
@click.pass_context
def export(ctx, platform, agent, profile, output):
    """
    Export agent configuration to platform-specific instruction files.

    Generates instruction files for Codex CLI, Gemini CLI, or Copilot CLI
    from the canonical agent specification in .ai/agents/agents.yaml.
    """
    verbose = ctx.obj.get("verbose", False)
    config = Config()

    # Get repository path
    repo_path = config.get_repository_path()
    if not repo_path:
        # Try to detect if we're in a repo
        repo_path = Path.cwd()
    
    # Load agents configuration
    agents_yaml_path = repo_path / ".ai" / "agents" / "agents.yaml"
    if not agents_yaml_path.exists():
        console.print(f"[red]Error: Agent configuration not found at {agents_yaml_path}[/red]")
        console.print("Please create .ai/agents/agents.yaml first.")
        raise click.Abort()

    try:
        with open(agents_yaml_path) as f:
            agents_config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]Error loading agents.yaml: {e}[/red]")
        raise click.Abort()

    # Find the specified agent
    agent_config = _find_agent(agents_config, agent)
    if not agent_config:
        console.print(f"[red]Error: Agent '{agent}' not found in agents.yaml[/red]")
        available = [a["id"] for a in agents_config.get("agents", [])]
        console.print(f"Available agents: {', '.join(available)}")
        raise click.Abort()

    # Load global policies
    global_policies_path = repo_path / ".ai" / "policies" / "global.md"
    global_policies = ""
    if global_policies_path.exists():
        with open(global_policies_path) as f:
            global_policies = f.read()

    # Get role policies
    role_id = agent_config.get("role")
    role_policies = ""
    if role_id and "roles" in agents_config:
        role_config = agents_config["roles"].get(role_id, {})
        role_policies = role_config.get("policies", "")

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = _get_default_output_path(platform, repo_path)

    if verbose:
        console.print(f"Agent: {agent}")
        console.print(f"Platform: {platform}")
        console.print(f"Output: {output_path}")

    # Discover skills and commands
    skills = _discover_skills(repo_path)
    commands = _discover_commands(repo_path)

    # Render template
    content = _render_template(
        platform=platform,
        agent_config=agent_config,
        agents_config=agents_config,
        global_policies=global_policies,
        role_policies=role_policies,
        skills=skills,
        commands=commands,
        repo_path=repo_path,
    )

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)

    console.print(f"[green]Successfully exported agent configuration to {output_path}[/green]")


def _find_agent(agents_config: Dict, agent_id: str) -> Optional[Dict]:
    """Find agent configuration by ID."""
    for agent in agents_config.get("agents", []):
        if agent.get("id") == agent_id:
            return agent
    return None


def _get_default_output_path(platform: str, repo_path: Path) -> Path:
    """Get default output path for platform."""
    if platform == "codex":
        return repo_path / "AGENTS.md"
    elif platform == "gemini":
        return repo_path / "GEMINI.md"
    elif platform == "copilot":
        return repo_path / ".github" / "copilot-instructions.md"
    else:
        raise ValueError(f"Unknown platform: {platform}")


def _discover_skills(repo_path: Path) -> List[Dict]:
    """Discover all skills in repository."""
    skills_dir = repo_path / "skills"
    if not skills_dir.exists():
        return []

    skills = []
    for skill_path in find_skill_directories(skills_dir):
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            try:
                with open(skill_md) as f:
                    content = f.read()
                frontmatter = _parse_frontmatter(content)
                if frontmatter:
                    skills.append({
                        "name": frontmatter.get("name", skill_path.name),
                        "description": frontmatter.get("description", ""),
                        "path": skill_path.relative_to(repo_path),
                    })
            except Exception:
                pass

    return sorted(skills, key=lambda x: x["name"])


def _discover_commands(repo_path: Path) -> List[Dict]:
    """Discover all commands in repository."""
    commands_dir = repo_path / "commands"
    if not commands_dir.exists():
        return []

    commands = []
    for cmd_path in find_command_files(commands_dir):
        try:
            with open(cmd_path) as f:
                content = f.read()
            frontmatter = _parse_frontmatter(content)
            description = ""
            if frontmatter and "description" in frontmatter:
                description = frontmatter["description"]
            
            commands.append({
                "name": cmd_path.stem,
                "description": description,
                "path": cmd_path.relative_to(repo_path),
            })
        except Exception:
            pass

    return sorted(commands, key=lambda x: x["name"])


def _parse_frontmatter(content: str) -> Optional[Dict]:
    """Parse YAML frontmatter from markdown content."""
    import re
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    frontmatter_str = match.group(1)
    try:
        return yaml.safe_load(frontmatter_str)
    except yaml.YAMLError:
        return None


def _render_template(
    platform: str,
    agent_config: Dict,
    agents_config: Dict,
    global_policies: str,
    role_policies: str,
    skills: List[Dict],
    commands: List[Dict],
    repo_path: Path,
) -> str:
    """Render platform-specific template."""
    
    # Get agent details
    agent_name = agent_config.get("name", "Skillz Agent")
    agent_id = agent_config.get("id", "default")
    agent_policies = agent_config.get("policies", "")
    role_id = agent_config.get("role", "")
    
    # Get capabilities
    role_config = agents_config.get("roles", {}).get(role_id, {})
    capability_ids = role_config.get("default-capabilities", [])
    capabilities = agents_config.get("capabilities", {})
    
    # Build capabilities as policies (downgrade)
    capabilities_text = ""
    if capability_ids:
        capabilities_text = "## Capabilities\n\n"
        capabilities_text += "The following capabilities are available to this agent:\n\n"
        for cap_id in capability_ids:
            if cap_id in capabilities:
                cap = capabilities[cap_id]
                capabilities_text += f"- **{cap_id}**: {cap.get('description', '')}\n"
        capabilities_text += "\n"

    # Build header
    header = _get_header(platform)
    
    # Build agent identity
    identity = f"# {agent_name}\n\n"
    identity += f"**Agent ID**: {agent_id}\n"
    identity += f"**Role**: {role_id}\n\n"
    
    # Build policies section
    policies_section = "# Policies\n\n"
    
    if global_policies:
        policies_section += "## Global Policies\n\n"
        policies_section += global_policies + "\n\n"
    
    if role_policies:
        policies_section += f"## Role Policies ({role_id})\n\n"
        policies_section += role_policies + "\n\n"
    
    if agent_policies:
        policies_section += "## Agent-Specific Policies\n\n"
        policies_section += agent_policies + "\n\n"
    
    # Build skills index
    skills_section = "# Available Skills\n\n"
    if skills:
        for skill in skills:
            skills_section += f"## {skill['name']}\n\n"
            skills_section += f"{skill['description']}\n\n"
            skills_section += f"Location: `{skill['path']}`\n\n"
    else:
        skills_section += "No skills available.\n\n"
    
    # Build commands index
    commands_section = "# Available Commands\n\n"
    if commands:
        for cmd in commands:
            commands_section += f"## {cmd['name']}\n\n"
            if cmd['description']:
                commands_section += f"{cmd['description']}\n\n"
            commands_section += f"Location: `{cmd['path']}`\n\n"
    else:
        commands_section += "No commands available.\n\n"
    
    # Assemble full content
    content = header
    content += identity
    content += capabilities_text
    content += policies_section
    content += skills_section
    content += commands_section
    
    return content


def _get_header(platform: str) -> str:
    """Get platform-specific header."""
    base_header = """<!--
THIS FILE IS AUTO-GENERATED FROM .ai/agents/agents.yaml
DO NOT EDIT THIS FILE DIRECTLY
Changes should be made to the canonical agent specification in .ai/agents/agents.yaml
and then exported using: skillz export --platform {platform}
-->

"""
    return base_header.format(platform=platform)
