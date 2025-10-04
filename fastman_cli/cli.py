"""
FastMan CLI - Main CLI Application

This is the main Typer application that orchestrates all CLI commands.
New commands can be easily added by creating new command files in the commands/ directory.
"""

import typer
from rich.console import Console
from typing import Optional

from .commands.startapp import startapp_command
from .commands.listapps import listapps_command

# Initialize Typer app
app = typer.Typer(
    name="fastman",
    help="FastMan CLI - FastAPI Module Manager",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()


# Register commands
@app.command("startapp")
def startapp(
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

    This command generates:
    • SQLAlchemy model with common fields
    • Pydantic schemas (Create, Update, Response)
    • CRUD operations extending base CRUD
    • Service layer with business logic
    • FastAPI routes with full CRUD endpoints
    • Custom exceptions
    • Module documentation

    Examples:

      $ python manage.py startapp Order

      $ python manage.py startapp customer --dir app

      $ python manage.py startapp product --force
    """
    startapp_command(app_name, directory, force)


@app.command("listapps")
def listapps(
    directory: str = typer.Option(
        "app",
        "--dir",
        "-d",
        help="Directory to scan for apps"
    ),
):
    """
    List all existing modular FastAPI apps.

    Scans the app directory and displays all modules that follow
    the modular structure pattern.

    Examples:

      $ python manage.py listapps

      $ python manage.py listapps --dir app
    """
    listapps_command(directory)


@app.command("version")
def version():
    """Show FastMan CLI version."""
    from . import __version__
    console.print(
        f"[bold cyan]FastMan CLI[/bold cyan] version [green]{__version__}[/green]")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        is_flag=True,
    ),
):
    """
    FastMan CLI - FastAPI Module Manager

    A Django-like management command for FastAPI projects.
    Generate complete modular apps with CRUD operations in seconds.
    """
    if version:
        from . import __version__
        console.print(
            f"[bold cyan]FastMan CLI[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()

    # Show help if no command is provided
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


# Entry point for running the CLI
if __name__ == "__main__":
    app()
