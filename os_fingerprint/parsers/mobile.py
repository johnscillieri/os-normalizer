"""Mobile device specific parsing logic."""

import re
from typing import Dict, Any

from os_fingerprint.models import OSParse
from os_fingerprint.helpers import (
    update_confidence,
    parse_semver_like,
    precision_from_parts,
)


def parse_mobile(text: str, data: Dict[str, Any], p: OSParse) -> OSParse:
    """
    Populate an OSParse instance with mobile device‑specific details.
    """
    t = text.lower()

    # Detect if it's iOS or Android
    if "ios" in t or "ipados" in t:
        p.product = "iOS/iPadOS"
        p.vendor = "Apple"
    elif "android" in t:
        p.product = "Android"
        p.vendor = "Google"
    else:
        # Default for unknown mobile OS
        p.product = "Mobile OS"
        p.vendor = None

    # Extract version info using semver-like parsing
    x, y, z = parse_semver_like(t)
    p.version_major, p.version_minor, p.version_patch = x, y, z
    p.precision = precision_from_parts(x, y, z, None) if x else "product"

    # Boost confidence based on precision
    update_confidence(p, p.precision)

    # Fallback arch from text if not already set elsewhere
    if not p.arch:
        from os_fingerprint.helpers import extract_arch_from_text

        p.arch = extract_arch_from_text(text)

    return p
