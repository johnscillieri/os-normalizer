"""Windows specific parsing logic.

Refactored for clarity: vendor/edition detection, NT mapping, and build
mapping are handled by focused helpers. Behavior is preserved while
avoiding ambiguous NT mappings when server signals are present.
"""

import re
from typing import Any

from os_normalizer.constants import (
    WINDOWS_BUILD_MAP,
    WINDOWS_NT_CLIENT_MAP,
    WINDOWS_NT_SERVER_MAP,
    WINDOWS_PRODUCT_PATTERNS,
    WINDOWS_SERVER_BUILD_MAP,
)
from os_normalizer.helpers import update_confidence
from os_normalizer.models import OSData

# Regex patterns used only by the Windows parser
WIN_EDITION_RE = re.compile(
    r"\b(professional|pro|enterprise|home|education|ltsc|datacenter|standard)\b",
    re.IGNORECASE,
)
WIN_SP_RE = re.compile(r"\bSP\s?([0-9]+)\b", re.IGNORECASE)
WIN_BUILD_RE = re.compile(r"\bbuild\s?(\d{4,6})\b", re.IGNORECASE)
WIN_NT_RE = re.compile(r"\bnt\s?(\d+)\.(\d+)\b", re.IGNORECASE)
WIN_FULL_NT_BUILD_RE = re.compile(r"\b(10)\.(0)\.(\d+)(?:\.(\d+))?\b")
WIN_GENERIC_VERSION_RE = re.compile(r"\b(\d+)\.(\d+)\.(\d{3,6})(?:\.(\d+))?\b")
WIN_CHANNEL_RE = re.compile(
    r"\b(24H2|23H2|22H2|21H2|21H1|20H2|2004|1909|1903|1809|1803|1709|1703|1607|1511|1507)\b",
    re.IGNORECASE,
)


def parse_windows(text: str, data: dict[str, Any], p: OSData) -> OSData:
    """Populate an OSData instance with Windows-specific details."""
    p.kernel_name = "nt"
    p.vendor = "Microsoft"

    # 1) Product and edition from free text
    lower_text = text.lower()
    p.product = _detect_product_from_text(lower_text)
    p.edition = _detect_edition(text)

    # 2) NT version mapping (client vs server)
    server_like = _is_server_like(text.lower())
    _apply_nt_mapping(text, p, server_like)

    # 3) Full kernel version (e.g., 10.0.22621.2715) + channel token if present
    marketing = _apply_full_kernel_and_channel(text, p)

    # 4) Build number + marketing channel (fallback when only 'build 22631' is present)
    marketing = marketing or _apply_build_mapping(text, p, server_like)

    # 5) Precision and version_major if applicable
    _finalize_precision_and_version(p)

    if not p.kernel_version:
        if p.version_major is not None and p.version_major >= 10:
            if marketing:
                p.kernel_version = marketing
            elif p.version_build:
                p.kernel_version = p.version_build
        elif p.version_major is not None and p.version_minor is not None:
            p.kernel_version = f"{p.version_major}.{p.version_minor}"

    # 6) Service Pack
    _apply_service_pack_label(lower_text, p)

    # 7) Update confidence
    update_confidence(p, p.precision)
    return p


def _detect_product_from_text(t: str) -> str:
    for product, patterns in WINDOWS_PRODUCT_PATTERNS:
        if any(pat in t for pat in patterns):
            return product

    return "Windows" if "windows" in t else "Unknown"


def _detect_edition(text: str) -> str | None:
    m = WIN_EDITION_RE.search(text)
    if not m:
        return None
    token = m.group(1).lower()
    norm = {
        "pro": "Professional",
        "professional": "Professional",
        "enterprise": "Enterprise",
        "home": "Home",
        "education": "Education",
        "ltsc": "LTSC",
        "datacenter": "Datacenter",
        "standard": "Standard",
    }
    return norm.get(token, token.title())


def _is_server_like(t: str) -> bool:
    return any(
        kw in t
        for kw in (
            "server",
            "datacenter",
            "standard",
            "essentials",
            "foundation",
            "core",  # server core often appears
            "hyper-v",
        )
    )


def _apply_nt_mapping(text: str, p: OSData, server_like: bool) -> None:
    nt = WIN_NT_RE.search(text)
    if not nt:
        return
    major, minor = int(nt.group(1)), int(nt.group(2))
    p.evidence["nt_version"] = f"{major}.{minor}"

    # If product already explicitly set (e.g., "Windows Server 2019"), keep it
    if p.product and p.product not in ("Windows", "Windows 10/11"):
        return

    product = WINDOWS_NT_SERVER_MAP.get((major, minor)) if server_like else WINDOWS_NT_CLIENT_MAP.get((major, minor))
    if product:
        p.product = product


def _apply_full_kernel_and_channel(text: str, p: OSData) -> str | None:
    # Full NT kernel version, e.g., 10.0.22621.2715
    m = WIN_FULL_NT_BUILD_RE.search(text)
    if m:
        build = m.group(3)
        suffix = m.group(4)
        p.version_build = p.version_build or build
        # Record evidence for NT 10.0 if not set via NT mapping
        if "nt_version" not in p.evidence:
            p.evidence["nt_version"] = "10.0"
        if p.version_major is None:
            p.version_major = 10
        if p.version_minor is None:
            p.version_minor = 0
        if suffix and not p.build_id:
            p.build_id = f"{build}.{suffix}"

    # Marketing channel token in free text, e.g., 22H2 (case-insensitive)
    channel = None
    ch = WIN_CHANNEL_RE.search(text)
    if ch:
        channel = ch.group(1).upper()

    m2 = WIN_GENERIC_VERSION_RE.search(text)
    if m2:
        major, minor, build, suffix = m2.groups()
        p.version_build = p.version_build or build
        p.evidence.setdefault("nt_version", f"{major}.{minor}")
        if p.version_major is None:
            p.version_major = int(major)
        if p.version_minor is None:
            p.version_minor = int(minor)
        if suffix and not p.build_id:
            p.build_id = f"{build}.{suffix}"

    return channel


def _apply_build_mapping(text: str, p: OSData, server_like: bool) -> str | None:
    m = WIN_BUILD_RE.search(text)
    if not m:
        return None
    build_num = int(m.group(1))
    p.version_build = str(build_num)

    if p.version_major is None or p.version_minor is None:
        nt_mm = WIN_NT_RE.search(text)
        if nt_mm:
            p.version_major = p.version_major or int(nt_mm.group(1))
            p.version_minor = p.version_minor or int(nt_mm.group(2))

    marketing: str | None = None

    if server_like:
        for lo, hi, product_name, marketing_label in WINDOWS_SERVER_BUILD_MAP:
            if lo <= build_num <= hi:
                if not p.product or p.product in ("Windows", "Windows 10/11"):
                    p.product = product_name
                marketing = marketing_label
                break
    else:
        for lo, hi, product_name, marketing_label in WINDOWS_BUILD_MAP:
            if lo <= build_num <= hi:
                if build_num >= 10240:
                    p.product = product_name
                marketing = marketing_label.split("/")[-1] if marketing_label else None
                break

    return marketing


def _apply_service_pack_label(text_lower: str, p: OSData) -> None:
    label = None

    if "sp1" in text_lower:
        label = "SP1"
    elif "sp2" in text_lower:
        label = "SP2"

    if label and p.product and label.lower() not in p.product.lower():
        p.product = f"{p.product} {label}"


def _finalize_precision_and_version(p: OSData) -> None:
    if p.version_build:
        p.precision = "build"
        return
    if p.version_patch is not None:
        p.precision = "patch"
        return
    if p.product and any(x in p.product for x in ("7", "8", "10", "11")):
        digits = re.findall(r"\d+", p.product)
        if digits:
            p.version_major = int(digits[0])
        p.precision = "major"
        return
    if p.product:
        p.precision = "product"
    else:
        p.precision = "family"
