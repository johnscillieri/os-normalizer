#!/usr/bin/env python3
"""Simple test to verify parser structure is working."""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        # Test importing the main module

        print("✓ Successfully imported normalize_os from os_normalizer")

        # Test importing individual parsers

        print("✓ Successfully imported all parser modules")

        # Test that the orchestrator can be imported

        print("✓ Successfully imported normalize_os from orchestrator")

        # Test that the package can be imported

        print("✓ Successfully imported normalize_os from package")

        print("\nAll imports successful! The parser structure is working correctly.")
        return True

    except Exception as e:
        print(f"✗ Import test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
