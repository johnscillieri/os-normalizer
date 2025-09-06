"""Utility functions shared across the OS fingerprinting package."""

import re
from typing import Optional, Tuple, Dict, Any

from os_fingerprint.constants import ARCH_SYNONYMS


def norm_arch(s: Optional[str]) -> Optional[str]:
    """Normalise an architecture string using ARCH_SYNONYMS."""
    if not s:
        return None
    a = s.strip().lower()
    return ARCH_SYNONYMS.get(a, a)


def parse_semver_like(text: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """
    Extract up to three integer components from a version‑like string.
    Returns (major, minor, patch) where missing parts are None.
    """
    m = re.search(r"\b(\d+)(?:\.(\d+))?(?:\.(\d+))?\b", text)
    if not m:
        return None, None, None
    major = int(m.group(1))
    minor = int(m.group(2)) if m.group(2) else None
    patch = int(m.group(3)) if m.group(3) else None
    return major, minor, patch


def precision_from_parts(
    major: Optional[int],
    minor: Optional[int],
    patch: Optional[int],
    build: Optional[str],
) -> str:
    """Derive a precision label from version components."""
    if build:
        return "build"
    if patch is not None:
        return "patch"
    if minor is not None:
        return "minor"
    if major is not None:
        return "major"
    return "product"


def canonical_key(p: Any) -> str:
    """
    Generate a deterministic key for an OSParse instance.
    The function expects the object to have vendor, product, version_* and edition fields.
    """
    vendor = (p.vendor or "-").lower()
    product = (p.product or "-").lower()
    version = ".".join([str(x) for x in [p.version_major, p.version_minor, p.version_patch] if x is not None]) or "-"
    edition = (p.edition or "-").lower()
    codename = (p.codename or "-").lower()
    return f"{vendor}:{product}:{version}:{edition}:{codename}"


# Regex for extracting an architecture token from free‑form text
ARCH_TEXT_RE = re.compile(r"\b(x86_64|amd64|x64|x86|i386|i686|arm64|aarch64|armv8|armv7l?|ppc64le)\b", re.I)


def extract_arch_from_text(text: str) -> Optional[str]:
    """Fallback architecture extraction from arbitrary text."""
    m = ARCH_TEXT_RE.search(text)
    if not m:
        return None
    raw = m.group(1).lower()
    return ARCH_SYNONYMS.get(raw, raw)


def parse_os_release(blob_text: str) -> Dict[str, Any]:
    """
    Parse the contents of an /etc/os-release style file.
    Returns a dict with selected keys (ID, ID_LIKE, PRETTY_NAME, VERSION_ID,
    VERSION_CODENAME).
    """
    out: Dict[str, Any] = {}
    for line in blob_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().upper()
        if k == "ID_LIKE":
            out[k] = [s.strip().lower() for s in re.split(r"[ ,]+", v.strip("\"'").strip()) if s]
        else:
            out[k] = v.strip("\"'")
    return out


def update_confidence(p: Any, precision: str) -> None:
    """
    Boost confidence based on the determined precision level.
    The mapping mirrors the original ad‑hoc values used throughout the monolithic file.
    """
    boost_map = {
        "build": 0.85,
        "patch": 0.80,
        "minor": 0.75,
        "major": 0.70,
        "product": 0.60,
    }
    p.confidence = max(p.confidence, boost_map.get(precision, 0.5))
