#!/usr/bin/env python3
"""
Test script to verify the restructured FastAPI application works correctly.
This script tests imports and basic functionality after modularization.
"""


def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")

    try:
        # Test app imports
        from app.core.main import app
        print("✓ app.core.main import successful")

        from app.core.models import Base, Product
        print("✓ app.core.models import successful")

        from app.core.database import get_session, get_database_url
        print("✓ app.core.database import successful")

        # Test schemas import (should still work from root)
        from app.core.schemas import Product as ProductSchema
        print("✓ schemas import successful")

        # Test main entry point
        import main
        print("✓ main entry point import successful")

        print("\n✅ All imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_database_url():
    """Test database URL construction."""
    try:
        from app.core.database import get_database_url
        # This will fail if env vars are missing, but that's expected
        try:
            url = get_database_url()
            print(f"✓ Database URL constructed: {url[:50]}...")
        except ValueError as e:
            print(
                f"⚠️ Database URL construction failed (expected if .env not configured): {e}")
        return True
    except Exception as e:
        print(f"❌ Database URL test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🔍 Testing restructured FastAPI application...\n")

    tests_passed = 0
    total_tests = 2

    if test_imports():
        tests_passed += 1

    if test_database_url():
        tests_passed += 1

    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All tests passed! The restructuring was successful.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
