#!/usr/bin/env python
"""
FastMan CLI - Management Script

Django-like management script for FastAPI projects.

Usage:
    python manage.py startapp <AppName>
    python manage.py startapp <AppName> --dir app
    python manage.py startapp <AppName> --force
    python manage.py version
    python manage.py --help

Examples:
    # Create a new Order module
    python manage.py startapp Order
    
    # Create a Customer module in a specific directory
    python manage.py startapp Customer --dir app
    
    # Force overwrite existing files
    python manage.py startapp Product --force
    
    # Show version
    python manage.py version
"""

from fastman_cli.cli import app
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    app()
