"""Export command for generating agent configuration files."""

from pathlib import Path
from typing import Dict, List, Optional

import click
import yaml
from rich.console import Console

from cli.config import Config
from cli.utils import find_command_files, find_skill_directories

console = Console()
GEMINI_YAML_WIDTH = 120


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
                    skills.append(
                        {
                            "name": frontmatter.get("name", skill_path.name),
                            "description": frontmatter.get("description", ""),
                            "path": skill_path.relative_to(repo_path),
                        }
                    )
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

            commands.append(
                {
                    "name": cmd_path.stem,
                    "description": description,
                    "path": cmd_path.relative_to(repo_path),
                }
            )
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
    """Render platform-specific template using a shared instruction block."""

    agent_name = agent_config.get("name", "Skillz Agent")
    agent_id = agent_config.get("id", "default")
    agent_policies = agent_config.get("policies", "")
    role_id = agent_config.get("role", "")

    role_config = agents_config.get("roles", {}).get(role_id, {})
    capability_ids = role_config.get("default-capabilities", [])
    capabilities = agents_config.get("capabilities", {})
    capabilities_payload = []
    for cap_id in capability_ids:
        cap = capabilities.get(cap_id, {})
        capabilities_payload.append({"id": cap_id, "description": cap.get("description", "")})

    normalized_skills = _normalize_items(skills)
    normalized_commands = _normalize_items(commands)

    instruction_block = _build_instruction_block(
        agent_name=agent_name,
        agent_id=agent_id,
        role_id=role_id,
        capabilities=capabilities_payload,
        global_policies=global_policies,
        role_policies=role_policies,
        agent_policies=agent_policies,
        skills=normalized_skills,
        commands=normalized_commands,
    )

    payload = {
        "agent": {"id": agent_id, "name": agent_name, "role": role_id},
        "capabilities": capabilities_payload,
        "skills": normalized_skills,
        "commands": normalized_commands,
        "instruction_block": instruction_block,
    }

    if platform == "codex":
        return _render_codex(payload)
    if platform == "gemini":
        return _render_gemini(payload)
    if platform == "copilot":
        return _render_copilot(payload)

    raise ValueError(f"Unknown platform: {platform}")


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


def _build_instruction_block(
    agent_name: str,
    agent_id: str,
    role_id: str,
    capabilities: List[Dict],
    global_policies: str,
    role_policies: str,
    agent_policies: str,
    skills: List[Dict],
    commands: List[Dict],
) -> str:
    """Construct a platform-neutral instruction block shared by all exporters."""

    identity = f"# {agent_name}\n\n"
    identity += f"**Agent ID**: {agent_id}\n"
    identity += f"**Role**: {role_id}\n\n"

    capabilities_text = ""
    if capabilities:
        capabilities_text = "## Capabilities\n\n"
        capabilities_text += "The following capabilities are available to this agent:\n\n"
        for cap in capabilities:
            capabilities_text += f"- **{cap['id']}**: {cap.get('description', '')}\n"
        capabilities_text += "\n"

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

    skills_section = "# Available Skills\n\n"
    if skills:
        for skill in skills:
            skills_section += f"## {skill['name']}\n\n"
            if skill.get("description"):
                skills_section += f"{skill['description']}\n\n"
            skills_section += f"Location: `{skill['path']}`\n\n"
    else:
        skills_section += "No skills available.\n\n"

    commands_section = "# Available Commands\n\n"
    if commands:
        for cmd in commands:
            commands_section += f"## {cmd['name']}\n\n"
            if cmd.get("description"):
                commands_section += f"{cmd['description']}\n\n"
            commands_section += f"Location: `{cmd['path']}`\n\n"
    else:
        commands_section += "No commands available.\n\n"

    return identity + capabilities_text + policies_section + skills_section + commands_section


def _render_codex(payload: Dict) -> str:
    """Render Codex CLI configuration (TOML-style) using the shared instruction block."""
    header = _get_header("codex")
    agent = payload["agent"]
    skills = payload.get("skills", [])
    commands = payload.get("commands", [])

    lines = []
    lines.append(header)
    lines.append("# Codex CLI Agent Profile")
    lines.append("")
    lines.append("[[agents]]")
    lines.append(f'id = "{_escape_toml(agent["id"])}"')
    lines.append(f'name = "{_escape_toml(agent["name"])}"')
    if agent.get("role"):
        lines.append(f'role = "{_escape_toml(agent["role"])}"')
    lines.append('instructions = """')
    lines.append(payload["instruction_block"].rstrip())
    lines.append('"""')

    if skills:
        lines.append("")
        lines.append("# Skills available to this agent")
        for skill in skills:
            lines.append("[[agents.skills]]")
            lines.append(f'name = "{_escape_toml(skill["name"])}"')
            lines.append(f'description = "{_escape_toml(skill.get("description", ""))}"')
            lines.append(f'path = "{_escape_toml(skill.get("path", ""))}"')

    if commands:
        lines.append("")
        lines.append("# Commands available to this agent")
        for cmd in commands:
            lines.append("[[agents.commands]]")
            lines.append(f'name = "{_escape_toml(cmd["name"])}"')
            lines.append(f'description = "{_escape_toml(cmd.get("description", ""))}"')
            lines.append(f'path = "{_escape_toml(cmd.get("path", ""))}"')

    return "\n".join(lines)


def _render_gemini(payload: Dict) -> str:
    """Render Gemini CLI configuration in YAML with embedded instructions."""
    header = _get_header("gemini")
    agent = payload["agent"]
    gemini_payload = {
        "agents": [
            {
                "id": agent["id"],
                "name": agent["name"],
                "role": agent.get("role", ""),
                "instructions": payload["instruction_block"],
                "skills": payload.get("skills", []),
                "commands": payload.get("commands", []),
            }
        ]
    }
    yaml_content = yaml.safe_dump(
        gemini_payload,
        sort_keys=False,
        default_flow_style=False,
        width=GEMINI_YAML_WIDTH,
    )
    return header + yaml_content


def _render_copilot(payload: Dict) -> str:
    """Render GitHub Copilot instructions markdown using the shared block."""
    header = _get_header("copilot")
    agent = payload["agent"]
    content = header
    content += f"# Copilot Agent: {agent['name']}\n\n"
    content += f"**Agent ID**: {agent['id']}\n\n"
    if agent.get("role"):
        content += f"**Role**: {agent['role']}\n\n"
    content += payload["instruction_block"]
    return content


def _normalize_items(items: List[Dict]) -> List[Dict]:
    """Normalize skill/command entries to plain dictionaries with string paths."""
    normalized = []
    for item in items:
        normalized.append(
            {
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "path": str(item.get("path", "")),
            }
        )
    return normalized


def _escape_toml(value: str) -> str:
    """Minimally escape TOML string content without pulling in extra dependencies."""
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\b", "\\b")
        .replace("\f", "\\f")
    )
