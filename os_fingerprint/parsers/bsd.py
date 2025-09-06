"""BSD specific parsing logic."""

import re
from typing import Dict, Any

from os_fingerprint.models import OSParse
from os_fingerprint.helpers import (
    update_confidence,
    parse_semver_like,
    precision_from_parts,
)


def parse_bsd(text: str, data: Dict[str, Any], p: OSParse) -> OSParse:
    """
    Populate an OSParse instance with BSD‑specific details.
    """
    t = text

    # For BSD family, we don't know the specific BSD variant yet
    p.product = "BSD"

    # Extract version info using semver-like parsing
    x, y, z = parse_semver_like(t)
    p.version_major, p.version_minor, p.version_patch = x, y, z
    p.precision = precision_from_parts(x, y, z, None) if x else "family"

    # Vendor is not specific to BSD family (could be FreeBSD, OpenBSD, etc.)
    p.vendor = None

    # Boost confidence based on precision
    update_confidence(p, p.precision)

    # Fallback arch from text if not already set elsewhere
    if not p.arch:
        from os_fingerprint.helpers import extract_arch_from_text

        p.arch = extract_arch_from_text(text)

    return p
