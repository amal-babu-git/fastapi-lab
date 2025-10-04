"""List apps command - shows all existing modular apps."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


def listapps_command(directory: str = "app"):
    """
    List all existing modular FastAPI apps.

    Scans the app directory and displays all modules that follow
    the modular structure pattern.
    """
    console.print(
        f"\n[bold blue]📋 FastMan CLI - Listing apps...[/bold blue]\n")

    base_dir = Path.cwd() / directory

    if not base_dir.exists():
        console.print(
            f"[bold red]❌ Error:[/bold red] Directory '{directory}' not found")
        raise typer.Exit(1)

    # Find all module directories
    modules = []
    for item in base_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_') and item.name != 'core' and item.name != 'apis':
            # Check if it has key files
            has_models = (item / "models.py").exists()
            has_routes = (item / "routes.py").exists()
            has_schemas = (item / "schemas.py").exists()

            if has_models and has_routes and has_schemas:
                # Count files
                files = list(item.glob("*.py"))
                modules.append({
                    "name": item.name,
                    "path": str(item.relative_to(Path.cwd())),
                    "files": len(files),
                    "complete": all([has_models, has_routes, has_schemas])
                })

    if not modules:
        console.print(
            f"[yellow]No modular apps found in '{directory}/'[/yellow]")
        console.print(
            f"\n[dim]Create one with: python manage.py startapp MyApp[/dim]\n")
        return

    # Create table
    table = Table(title=f"📦 Modular Apps in '{directory}/'", show_lines=True)
    table.add_column("Module", style="cyan", no_wrap=True)
    table.add_column("Path", style="dim")
    table.add_column("Files", justify="center", style="green")
    table.add_column("Status", justify="center")

    for module in sorted(modules, key=lambda x: x["name"]):
        status = "✓ Complete" if module["complete"] else "⚠ Partial"
        status_style = "green" if module["complete"] else "yellow"

        table.add_row(
            module["name"],
            module["path"],
            str(module["files"]),
            f"[{status_style}]{status}[/{status_style}]"
        )

    console.print(table)
    console.print(f"\n[bold]Total:[/bold] {len(modules)} module(s) found\n")
