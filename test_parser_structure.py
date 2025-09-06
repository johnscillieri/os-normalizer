#!/usr/bin/env python3
"""Simple test to verify parser structure is working."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        # Test importing the main module
        from os_normalizer import normalize_os

        print("✓ Successfully imported normalize_os from os_normalizer")

        # Test importing individual parsers
        from os_fingerprint.parsers.windows import parse_windows
        from os_fingerprint.parsers.linux import parse_linux
        from os_fingerprint.parsers.macos import parse_macos
        from os_fingerprint.parsers.bsd import parse_bsd
        from os_fingerprint.parsers.mobile import parse_mobile
        from os_fingerprint.parsers.network import parse_network

        print("✓ Successfully imported all parser modules")

        # Test that the orchestrator can be imported
        from os_fingerprint.orchestrator import (
            normalize_os as orchestrator_normalize_os,
        )

        print("✓ Successfully imported normalize_os from orchestrator")

        # Test that the package can be imported
        from os_fingerprint import normalize_os as package_normalize_os

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
