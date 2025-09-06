"""macOS specific parsing logic."""

import re
from typing import Dict, Any

from os_fingerprint.models import OSParse
from os_fingerprint.helpers import update_confidence


# Regex patterns used only by the macOS parser
DARWIN_RE = re.compile(r"\bdarwin\s?(\d+)(?:\.(\d+))?(?:\.(\d+))?\b", re.I)


def parse_macos(text: str, data: Dict[str, Any], p: OSParse) -> OSParse:
    """
    Populate an OSParse instance with macOS‑specific details.
    """
    t = text
    p.product = "macOS"
    p.vendor = "Apple"

    # Aliases like "Sequoia" - using the ALIASES from constants
    from os_fingerprint.constants import ALIASES

    for alias, normalized in ALIASES.items():
        if alias in t and normalized.startswith("macOS"):
            parts = normalized.split()
            if len(parts) == 2 and parts[1].isdigit():
                p.version_major = int(parts[1])
                # Use the precision function from helpers to determine precision
                from os_fingerprint.helpers import precision_from_parts

                p.precision = max(
                    p.precision,
                    "major",
                    key=lambda x: {
                        "family": 0,
                        "product": 1,
                        "major": 2,
                        "minor": 3,
                        "patch": 4,
                        "build": 5,
                    }[x],
                )  # type: ignore

    # Darwin version
    m = DARWIN_RE.search(t)
    if m:
        dmaj = int(m.group(1))
        p.kernel_name = "darwin"
        p.kernel_version = ".".join([g for g in m.groups() if g])

        # Use MACOS_DARWIN_MAP from constants
        from os_fingerprint.constants import MACOS_DARWIN_MAP

        if dmaj in MACOS_DARWIN_MAP:
            prod, ver, code = MACOS_DARWIN_MAP[dmaj]
            p.product = prod
            if ver.isdigit():
                p.version_major = int(ver)
                p.precision = "major"
            else:
                x, y, *z = ver.split(".")
                p.version_major = int(x)
                p.version_minor = int(y)
                p.precision = "minor"
            p.codename = code

    # Fallback version extraction from text
    if not p.version_major:
        mm = re.search(r"\bmacos\s?(\d+)(?:\.(\d+))?", t, re.I)
        if mm:
            p.version_major = int(mm.group(1))
            if mm.group(2):
                p.version_minor = int(mm.group(2))
                p.precision = "minor"
            else:
                p.precision = "major"

    # Fallback codename from text
    if not p.codename:
        from os_fingerprint.constants import MACOS_DARWIN_MAP

        for dmaj, (_, _, code) in MACOS_DARWIN_MAP.items():
            if code.lower() in t:
                p.codename = code
                ver = MACOS_DARWIN_MAP[dmaj][1]
                if ver.isdigit():
                    p.version_major = int(ver)
                    p.precision = max(
                        p.precision,
                        "major",
                        key=lambda x: {
                            "family": 0,
                            "product": 1,
                            "major": 2,
                            "minor": 3,
                            "patch": 4,
                            "build": 5,
                        }[x],
                    )  # type: ignore

    # Fallback arch from text if not already set elsewhere
    if not p.arch:
        from os_fingerprint.helpers import extract_arch_from_text

        p.arch = extract_arch_from_text(text)

    # Boost confidence based on precision
    update_confidence(p, p.precision)
    return p
