"""Export command for generating platform-specific instruction files."""

from pathlib import Path

import click
from rich.console import Console

from cli.config import Config
from cli.export import ExportManager

console = Console()


@click.command()
@click.option(
    "--platform",
    "-p",
    type=click.Choice(["codex", "gemini", "copilot"], case_sensitive=False),
    required=True,
    help="Target platform for export",
)
@click.option(
    "--profile",
    type=str,
    default=None,
    help="Profile to use from .ai/config.yaml (e.g., 'minimal', 'full')",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default=None,
    help="Output file path (defaults to platform-specific location from config)",
)
@click.option(
    "--source",
    type=click.Choice(["repository", "installed"], case_sensitive=False),
    default="repository",
    help="Source of skills and commands",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be exported without writing files",
)
@click.pass_context
def export(ctx, platform, profile, output, source, dry_run):
    """
    Export skills and commands to platform-specific instruction files.

    Reads from the canonical .ai/ configuration and generates instruction files
    for Codex CLI, Gemini CLI, or GitHub Copilot CLI.

    Examples:

        # Export for Codex CLI
        skillz export --platform codex

        # Export for Gemini CLI with minimal profile
        skillz export --platform gemini --profile minimal

        # Export for Copilot with custom output path
        skillz export --platform copilot --output .github/copilot.md

        # Preview what would be exported
        skillz export --platform codex --dry-run
    """
    config = Config()
    verbose = ctx.obj.get("verbose", False)

    # Get repository path
    repo_path = config.get_repository_path()
    if not repo_path:
        console.print("[red]Error: Repository path not configured[/red]")
        console.print("Set it with: skillz config set repository /path/to/repo")
        raise click.Abort()

    if not repo_path.exists():
        console.print(f"[red]Error: Repository path does not exist: {repo_path}[/red]")
        raise click.Abort()

    # Check for .ai/config.yaml
    ai_config_path = repo_path / ".ai" / "config.yaml"
    if not ai_config_path.exists():
        console.print(
            f"[yellow]Warning: .ai/config.yaml not found at {ai_config_path}[/yellow]"
        )
        console.print("Using default configuration...")

    try:
        # Initialize export manager
        export_manager = ExportManager(repo_path)

        if verbose:
            console.print(f"[blue]Platform:[/blue] {platform}")
            console.print(f"[blue]Profile:[/blue] {profile or 'default'}")
            console.print(f"[blue]Source:[/blue] {source}")
            console.print(f"[blue]Repository:[/blue] {repo_path}")

        if dry_run:
            console.print("\n[yellow]DRY RUN - No files will be written[/yellow]\n")

            # Build context to show what would be exported
            context = export_manager._build_context(platform, profile)

            console.print(f"[bold]Policies:[/bold] {len(context['policies'])} policy(ies)")
            for policy in context["policies"]:
                console.print(f"  • {policy['name']}: {policy['description']}")

            console.print(f"\n[bold]Skills:[/bold] {len(context['skills'])} skill(s)")
            for skill in context["skills"][:5]:  # Show first 5
                console.print(f"  • {skill['name']}: {skill['description'][:60]}...")
            if len(context["skills"]) > 5:
                console.print(f"  ... and {len(context['skills']) - 5} more")

            console.print(f"\n[bold]Commands:[/bold] {len(context['commands'])} command(s)")
            for command in context["commands"][:5]:  # Show first 5
                console.print(f"  • {command['name']}")
            if len(context["commands"]) > 5:
                console.print(f"  ... and {len(context['commands']) - 5} more")

            # Show where it would be written
            output_path = output or export_manager.ai_config.get_default_output(platform)
            console.print(f"\n[bold]Would write to:[/bold] {output_path}")

        else:
            # Perform export
            console.print(f"[blue]Exporting for {platform}...[/blue]")
            output_path = export_manager.export(platform, output, profile)
            console.print(f"[green]✓[/green] Successfully exported to: {output_path}")

            # Show summary
            context = export_manager._build_context(platform, profile)
            console.print(f"\nIncluded:")
            console.print(f"  • {len(context['policies'])} policy(ies)")
            console.print(f"  • {len(context['skills'])} skill(s)")
            console.print(f"  • {len(context['commands'])} command(s)")

    except Exception as e:
        console.print(f"[red]Error during export:[/red] {e}")
        if verbose:
            import traceback

            console.print(traceback.format_exc())
        raise click.Abort()
