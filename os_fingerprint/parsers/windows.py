"""Windows specific parsing logic."""

import re
from typing import Dict, Any

from os_fingerprint.models import OSParse
from os_fingerprint.helpers import update_confidence


# Regex patterns used only by the Windows parser
WIN_EDITION_RE = re.compile(
    r"\b(professional|enterprise|home|education|server|ltsc)\b", re.I
)
WIN_SP_RE = re.compile(r"\bSP\s?([0-9]+)\b", re.I)
WIN_BUILD_RE = re.compile(r"\bbuild\s?(\d{4,6})\b", re.I)
WIN_NT_RE = re.compile(r"\bnt\s?(\d+)\.(\d+)\b", re.I)


def parse_windows(text: str, data: Dict[str, Any], p: OSParse) -> OSParse:
    """
    Populate an OSParse instance with Windows‑specific details.
    """
    t = text.lower()
    p.kernel_name = "nt"

    # Basic product detection
    if "windows 11" in t:
        p.product = "Windows 11"
    elif "windows 10" in t:
        p.product = "Windows 10"
    elif "windows 8.1" in t:
        p.product = "Windows 8.1"
    elif "windows 8" in t:
        p.product = "Windows 8"
    elif "windows 7" in t:
        p.product = "Windows 7"
    elif "windows" in t and p.product is None:
        p.product = "Windows"

    # Edition (Professional, Enterprise, etc.)
    m = WIN_EDITION_RE.search(text)
    if m:
        p.edition = m.group(1).title()

    # Service Pack
    sp = WIN_SP_RE.search(text)
    if sp:
        p.version_patch = int(sp.group(1))
        p.evidence["service_pack"] = sp.group(0)

    # NT version (e.g. nt 6.3)
    nt = WIN_NT_RE.search(text)
    if nt:
        major, minor = int(nt.group(1)), int(nt.group(2))
        p.evidence["nt_version"] = f"{major}.{minor}"
        # Map coarse NT version to a generic product name if not already set
        from os_fingerprint.constants import WINDOWS_NT_MAP

        coarse = WINDOWS_NT_MAP.get((major, minor))
        if coarse and not p.product:
            p.product = coarse[0]

    # Build number
    build_match = WIN_BUILD_RE.search(text)
    if build_match:
        build_num = int(build_match.group(1))
        p.version_build = str(build_num)

        # Construct a kernel version string for recent Windows releases
        if p.product == "Windows 10/11" or "10.0" in text:
            p.kernel_version = f"10.0.{build_num}"
        else:
            p.kernel_version = None

        # Map build number to specific product/channel using the map from constants
        from os_fingerprint.constants import WINDOWS_BUILD_MAP

        for lo, hi, product_name, marketing in WINDOWS_BUILD_MAP:
            if lo <= build_num <= hi:
                p.product = product_name
                p.channel = marketing
                break

    # Precision hierarchy – prefer more specific info when available
    if p.version_build:
        p.precision = "build"
    elif p.version_patch is not None:
        p.precision = "patch"
    elif p.product and any(x in p.product for x in ("7", "8", "10", "11")):
        # Extract major version from the product string
        digits = re.findall(r"\d+", p.product)
        if digits:
            p.version_major = int(digits[0])
        p.precision = "major"
    elif p.product:
        p.precision = "product"
    else:
        p.precision = "family"

    # Vendor is always Microsoft for Windows
    p.vendor = "Microsoft"

    # Fallback architecture extraction if not already set elsewhere
    if not p.arch:
        from os_fingerprint.helpers import extract_arch_from_text

        p.arch = extract_arch_from_text(text)

    # Boost confidence based on how precise the parsing was
    update_confidence(p, p.precision)

    return p
