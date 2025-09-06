"""Orchestrator module for OS fingerprinting.

Provides a thin wrapper around the original `normalize_os` implementation
found in the repository root (`os_normalizer.py`). This keeps backward
compatibility while allowing package users to import via:

    from os_fingerprint import normalize_os

or

    from os_fingerprint.orchestrator import normalize_os
"""

# Import the original implementation from the top‑level module.
from os_normalizer import normalize_os as _original_normalize_os


def normalize_os(*args, **kwargs):
    """Delegate to the original `normalize_os` function."""
    return _original_normalize_os(*args, **kwargs)
