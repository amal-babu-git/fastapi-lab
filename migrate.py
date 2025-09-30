"""
Database migration helper script.

This script provides convenient functions for common Alembic operations.
Can be used directly or imported in other scripts.
"""

import subprocess
import sys
from typing import Optional


def run_command(cmd: list[str]) -> tuple[int, str]:
    """Run a shell command and return exit code and output."""
    try:
        # Use sys.executable to ensure we use the same Python interpreter
        if cmd[0] == "python":
            cmd[0] = sys.executable

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
        return result.returncode, output
    except Exception as e:
        return 1, str(e)


def current() -> None:
    """Show current migration version."""
    print("🔍 Checking current migration version...\n")
    code, output = run_command(["python", "-m", "alembic", "current"])
    print(output)
    if code == 0:
        print("✅ Current version checked successfully")
    else:
        print("❌ Failed to check current version")
        sys.exit(1)


def history() -> None:
    """Show migration history."""
    print("📜 Migration history:\n")
    code, output = run_command(
        ["python", "-m", "alembic", "history", "--verbose"])
    print(output)
    if code == 0:
        print("✅ History retrieved successfully")
    else:
        print("❌ Failed to retrieve history")
        sys.exit(1)


def create_migration(message: str, autogenerate: bool = True) -> None:
    """Create a new migration."""
    print(f"📝 Creating migration: {message}\n")

    cmd = ["python", "-m", "alembic", "revision"]
    if autogenerate:
        cmd.append("--autogenerate")
    cmd.extend(["-m", message])

    code, output = run_command(cmd)
    print(output)

    if code == 0:
        print(f"✅ Migration '{message}' created successfully")
        print("⚠️  Please review the generated migration file before applying!")
    else:
        print(f"❌ Failed to create migration")
        sys.exit(1)


def upgrade(revision: str = "head") -> None:
    """Apply migrations up to specified revision."""
    print(f"⬆️  Upgrading database to: {revision}\n")
    code, output = run_command(
        ["python", "-m", "alembic", "upgrade", revision])
    print(output)

    if code == 0:
        print(f"✅ Database upgraded to {revision} successfully")
    else:
        print("❌ Failed to upgrade database")
        sys.exit(1)


def downgrade(revision: str = "-1") -> None:
    """Rollback migrations to specified revision."""
    print(f"⬇️  Downgrading database to: {revision}\n")

    # Confirm for safety
    confirm = input(
        f"⚠️  Are you sure you want to downgrade to '{revision}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Downgrade cancelled")
        return

    code, output = run_command(
        ["python", "-m", "alembic", "downgrade", revision])
    print(output)

    if code == 0:
        print(f"✅ Database downgraded to {revision} successfully")
    else:
        print("❌ Failed to downgrade database")
        sys.exit(1)


def stamp(revision: str) -> None:
    """Mark the database as being at a specific revision without running migrations."""
    print(f"🔖 Stamping database at revision: {revision}\n")

    confirm = input(
        f"⚠️  Are you sure you want to stamp the database at '{revision}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Stamp cancelled")
        return

    code, output = run_command(["python", "-m", "alembic", "stamp", revision])
    print(output)

    if code == 0:
        print(f"✅ Database stamped at {revision} successfully")
    else:
        print("❌ Failed to stamp database")
        sys.exit(1)


def show_help() -> None:
    """Show help message."""
    help_text = """
🗄️  Database Migration Helper

Usage: python migrate.py [command] [options]

Commands:
  current                       Show current migration version
  history                       Show migration history
  create <message>             Create new migration with autogenerate
  create-empty <message>       Create empty migration (manual)
  upgrade [revision]           Apply migrations (default: head)
  downgrade [revision]         Rollback migrations (default: -1)
  stamp <revision>             Mark database at specific revision
  help                         Show this help message

Examples:
  python migrate.py current
  python migrate.py create "add user table"
  python migrate.py upgrade head
  python migrate.py downgrade -1
  python migrate.py history

Quick Commands:
  - Show current version:    python migrate.py current
  - Create new migration:    python migrate.py create "your message here"
  - Apply all migrations:    python migrate.py upgrade
  - Rollback one migration:  python migrate.py downgrade
  - View history:            python migrate.py history
"""
    print(help_text)


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    try:
        if command == "current":
            current()
        elif command == "history":
            history()
        elif command == "create":
            if len(sys.argv) < 3:
                print("❌ Error: Migration message required")
                print("Usage: python migrate.py create \"your message\"")
                sys.exit(1)
            message = sys.argv[2]
            create_migration(message, autogenerate=True)
        elif command == "create-empty":
            if len(sys.argv) < 3:
                print("❌ Error: Migration message required")
                print("Usage: python migrate.py create-empty \"your message\"")
                sys.exit(1)
            message = sys.argv[2]
            create_migration(message, autogenerate=False)
        elif command == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            upgrade(revision)
        elif command == "downgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
            downgrade(revision)
        elif command == "stamp":
            if len(sys.argv) < 3:
                print("❌ Error: Revision required")
                print("Usage: python migrate.py stamp <revision>")
                sys.exit(1)
            revision = sys.argv[2]
            stamp(revision)
        elif command in ["help", "-h", "--help"]:
            show_help()
        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'python migrate.py help' for usage information")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
