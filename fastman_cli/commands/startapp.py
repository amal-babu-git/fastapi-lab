"""Start app command - generates a new modular app."""

import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from ..utils.helpers import (
    to_snake_case,
    to_pascal_case,
    ensure_directory,
    write_file,
)
from ..templates import (
    generate_model,
    generate_schemas,
    generate_crud,
    generate_service,
    generate_routes,
    generate_exceptions,
    generate_init,
    generate_readme,
)

console = Console()


def startapp_command(
    app_name: str = typer.Argument(..., help="Name of the app to create"),
    directory: str = typer.Option(
        "app",
        "--dir",
        "-d",
        help="Directory where the app will be created"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files"
    ),
):
    """
    Create a new modular FastAPI app with complete CRUD structure.

    Example:
        python manage.py startapp Order
        python manage.py startapp customer --dir app
    """
    console.print(
        f"\n[bold blue]🚀 FastMan CLI - Creating new app...[/bold blue]\n")

    # Convert app name to different cases
    module_name = to_snake_case(app_name)
    class_name = to_pascal_case(app_name)

    # Define paths
    base_dir = Path.cwd()
    app_dir = base_dir / directory / module_name

    # Check if directory exists
    if app_dir.exists() and not force:
        console.print(
            f"[bold red]❌ Error:[/bold red] App '{module_name}' already exists at {app_dir}",
            style="red"
        )
        console.print(
            f"[yellow]💡 Tip:[/yellow] Use --force flag to overwrite existing files"
        )
        raise typer.Exit(1)

    # Create directory structure
    console.print(f"[cyan]📁 Creating directory structure...[/cyan]")
    ensure_directory(app_dir)

    # Files to generate
    files_to_create = {
        "models.py": generate_model(module_name, class_name),
        "schemas.py": generate_schemas(module_name, class_name),
        "crud.py": generate_crud(module_name, class_name),
        "services.py": generate_service(module_name, class_name),
        "routes.py": generate_routes(module_name, class_name),
        "exceptions.py": generate_exceptions(module_name, class_name),
        "__init__.py": generate_init(module_name, class_name),
        "README.md": generate_readme(module_name, class_name),
    }

    # Track created files
    created_files = []
    skipped_files = []

    # Create files
    console.print(f"[cyan]📝 Generating files...[/cyan]\n")

    for filename, content in files_to_create.items():
        file_path = app_dir / filename

        if write_file(file_path, content, overwrite=force):
            created_files.append(filename)
            console.print(f"  [green]✓[/green] Created: {filename}")
        else:
            skipped_files.append(filename)
            console.print(
                f"  [yellow]⊘[/yellow] Skipped: {filename} (already exists)")

    # Summary
    console.print()
    summary_table = Table(title="📊 Summary", show_header=False, box=None)
    summary_table.add_row("[bold]App Name:[/bold]",
                          f"[cyan]{class_name}[/cyan]")
    summary_table.add_row("[bold]Module Name:[/bold]",
                          f"[cyan]{module_name}[/cyan]")
    summary_table.add_row("[bold]Location:[/bold]", f"[cyan]{app_dir}[/cyan]")
    summary_table.add_row("[bold]Files Created:[/bold]",
                          f"[green]{len(created_files)}[/green]")

    if skipped_files:
        summary_table.add_row("[bold]Files Skipped:[/bold]",
                              f"[yellow]{len(skipped_files)}[/yellow]")

    console.print(summary_table)
    console.print()

    # Next steps panel
    next_steps = f"""
[bold cyan]1. Register the router[/bold cyan]
   Add to [yellow]app/apis/v1.py[/yellow]:
   
   [dim]from app.{module_name}.routes import router as {module_name}_router
   router.include_router({module_name}_router)[/dim]

[bold cyan]2. Generate database migration[/bold cyan]
   
   [dim]alembic revision --autogenerate -m "Add {module_name} table"
   alembic upgrade head[/dim]

[bold cyan]3. Test your API[/bold cyan]
   
   [dim]uvicorn app.core.main:app --reload[/dim]
   
   Visit: [link]http://localhost:8000/docs[/link]

[bold cyan]4. Customize[/bold cyan]
   
   • Edit [yellow]{module_name}/models.py[/yellow] to add custom fields
   • Update [yellow]{module_name}/services.py[/yellow] for business logic
   • Modify [yellow]{module_name}/routes.py[/yellow] for custom endpoints
"""

    console.print(
        Panel(
            next_steps,
            title="[bold green]✨ Next Steps[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )

    console.print(
        f"\n[bold green]✅ App '{class_name}' created successfully![/bold green]\n"
    )
