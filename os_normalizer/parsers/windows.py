"""Windows specific parsing logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
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
WIN_10_11_KERNEL_VERSION_RE = re.compile(
    r"\b(24H2|23H2|22H2|21H2|21H1|20H2|2004|1909|1903|1809|1803|1709|1703|1607|1511|1507)\b",
    re.IGNORECASE,
)


@dataclass
class VersionComponents:
    major: int | None = None
    minor: int | None = None
    build: str | None = None
    patch: int | None = None
    evidence_nt: str | None = None


@dataclass
class BuildMappingResult:
    product: str | None = None
    kernel_release: str | None = None


@dataclass(frozen=True)
class ProductDefaults:
    version_major: int | None = None
    version_minor: int | None = None
    version_build: str | None = None
    kernel_version: str | None = None
    build_precision: str | None = None
    confidence_precision: str | None = None


PRODUCT_DEFAULTS: dict[str, ProductDefaults] = {
    "Windows 7": ProductDefaults(
        version_major=6,
        version_minor=1,
        version_build="7601",
        kernel_version="6.1",
        build_precision="build",
        confidence_precision="build",
    ),
    "Windows 7 SP1": ProductDefaults(
        version_major=6,
        version_minor=1,
        version_build="7601",
        kernel_version="6.1",
        build_precision="build",
        confidence_precision="major",
    ),
    "Windows 8": ProductDefaults(
        version_major=6,
        version_minor=2,
        version_build="9200",
        kernel_version="6.2",
        build_precision="build",
    ),
    "Windows 8.1": ProductDefaults(
        version_major=6,
        version_minor=3,
        version_build="9600",
        kernel_version="6.3",
        build_precision="build",
        confidence_precision="major",
    ),
    "Windows 10": ProductDefaults(
        version_major=10,
    ),
    "Windows 11": ProductDefaults(
        version_major=11,
    ),
    "Windows Server 2012 R2": ProductDefaults(
        version_major=6,
        version_minor=3,
        version_build="9600",
        kernel_version="6.3",
        build_precision="product",
    ),
    "Windows Server 2016": ProductDefaults(
        version_major=10,
        version_minor=0,
    ),
    "Windows ME": ProductDefaults(
        version_major=4,
        version_minor=90,
        version_build="3000",
        kernel_version="4.9",
        build_precision="build",
    ),
    "Windows 98": ProductDefaults(
        version_major=4,
        version_minor=10,
        version_build="1998",
        kernel_version="4.10",
        build_precision="build",
    ),
}


def parse_windows(text: str, data: dict[str, Any], p: OSData) -> OSData:
    """Populate an OSData instance with Windows-specific details."""
    del data  # Unused for Windows parsing, but retained for signature compatibility

    p.kernel_name = "nt"
    p.vendor = "Microsoft"

    lower_text = text.lower()
    p.product = _detect_product_from_text(lower_text)
    p.edition = _detect_edition(text)

    server_like = _is_server_like(lower_text)

    nt_version = _detect_nt_version(text)
    if nt_version:
        _record_nt_version(p, nt_version)
        _apply_nt_product_mapping(p, nt_version, server_like)

    version_components = _extract_version_components(text)
    if version_components:
        _apply_version_components(p, version_components)

    kernel_release = _detect_kernel_release(text)

    build_number_int = _coerce_int(p.version_build)
    if build_number_int is None:
        build_candidate = _extract_build_number(text)
        if build_candidate is not None:
            build_number_int = build_candidate
            if not p.version_build:
                p.version_build = str(build_candidate)

    if build_number_int is not None:
        mapping = _lookup_build_mapping(build_number_int, server_like)
        if mapping.product and _should_override_product(p.product):
            p.product = mapping.product
        if not kernel_release and mapping.kernel_release:
            kernel_release = mapping.kernel_release

    _apply_service_pack_label(lower_text, p)
    _apply_product_defaults(p)
    _apply_contextual_version_minor(p, lower_text)
    _finalize_version_major(p)
    _finalize_kernel_version(p, kernel_release)
    _finalize_precision(p)

    confidence_target = getattr(p, "_confidence_hint", p.precision)
    update_confidence(p, confidence_target)
    if hasattr(p, "_confidence_hint"):
        delattr(p, "_confidence_hint")
    return p


def _detect_product_from_text(t: str) -> str:
    for product, patterns in WINDOWS_PRODUCT_PATTERNS:
        if any(pat in t for pat in patterns):
            return product

    return "Windows" if "windows" in t else "Unknown"


def _detect_edition(text: str) -> str | None:
    match = WIN_EDITION_RE.search(text)
    if not match:
        return None

    token = match.group(1).lower()
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


def _detect_nt_version(text: str) -> tuple[int, int] | None:
    match = WIN_NT_RE.search(text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _record_nt_version(p: OSData, nt_version: tuple[int, int]) -> None:
    major, minor = nt_version
    p.evidence["nt_version"] = _canonical_nt_evidence(major, minor)
    if p.version_major is None:
        p.version_major = major
    if p.version_minor is None:
        p.version_minor = minor


def _canonical_nt_evidence(major: int, minor: int) -> str:
    if major >= 11:
        return "10.0"
    return f"{major}.{minor}"


def _apply_nt_product_mapping(p: OSData, nt_version: tuple[int, int], server_like: bool) -> None:
    if p.product and p.product not in {"Windows", "Unknown", "Windows 10/11"}:
        return

    mapping = WINDOWS_NT_SERVER_MAP if server_like else WINDOWS_NT_CLIENT_MAP
    product = mapping.get(nt_version)
    if product:
        p.product = product


def _extract_version_components(text: str) -> VersionComponents | None:
    return _extract_full_version(text) or _extract_generic_version(text)


def _extract_full_version(text: str) -> VersionComponents | None:
    match_with_patch: re.Match[str] | None = None
    fallback_match: re.Match[str] | None = None
    for m in WIN_FULL_NT_BUILD_RE.finditer(text):
        if m.group(4):
            match_with_patch = m
            break
        if fallback_match is None:
            fallback_match = m

    match = match_with_patch or fallback_match
    if match is None:
        return None

    build = match.group(3)
    suffix = match.group(4)
    return VersionComponents(
        major=10,
        minor=0,
        build=build,
        patch=int(suffix) if suffix else None,
        evidence_nt="10.0",
    )


def _extract_generic_version(text: str) -> VersionComponents | None:
    match_with_patch: re.Match[str] | None = None
    fallback_match: re.Match[str] | None = None
    for m in WIN_GENERIC_VERSION_RE.finditer(text):
        if m.group(4):
            match_with_patch = m
            break
        if fallback_match is None:
            fallback_match = m

    match = match_with_patch or fallback_match
    if match is None:
        return None

    major, minor, build, suffix = match.groups()
    return VersionComponents(
        major=int(major),
        minor=int(minor),
        build=build,
        patch=int(suffix) if suffix else None,
        evidence_nt=f"{major}.{minor}",
    )


def _apply_version_components(p: OSData, components: VersionComponents) -> None:
    if components.major is not None and p.version_major is None:
        p.version_major = components.major
    if components.minor is not None and p.version_minor is None:
        p.version_minor = components.minor
    if components.build and p.version_build is None:
        p.version_build = components.build
    if components.patch is not None and p.version_patch is None:
        p.version_patch = components.patch
    if components.evidence_nt and "nt_version" not in p.evidence:
        p.evidence["nt_version"] = components.evidence_nt


def _detect_kernel_release(text: str) -> str | None:
    match = WIN_10_11_KERNEL_VERSION_RE.search(text)
    return match.group(1).upper() if match else None


def _extract_build_number(text: str) -> int | None:
    match = WIN_BUILD_RE.search(text)
    if match:
        return int(match.group(1))
    return None


def _lookup_build_mapping(build_num: int, server_like: bool) -> BuildMappingResult:
    table = WINDOWS_SERVER_BUILD_MAP if server_like else WINDOWS_BUILD_MAP
    for lo, hi, product_name, kernel_release in table:
        if lo <= build_num <= hi:
            product = product_name if server_like or build_num >= 10240 else None
            return BuildMappingResult(product=product, kernel_release=kernel_release)
    return BuildMappingResult()


def _should_override_product(current: str | None) -> bool:
    return current in {None, "Windows", "Unknown", "Windows 10/11"}


def _finalize_kernel_version(p: OSData, kernel_release: str | None) -> None:
    if p.kernel_version:
        return

    if p.version_major is not None and p.version_major >= 10:
        if kernel_release:
            p.kernel_version = kernel_release
        elif p.version_build:
            p.kernel_version = p.version_build
    elif p.version_major is not None and p.version_minor is not None:
        p.kernel_version = f"{p.version_major}.{p.version_minor}"


def _coerce_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _apply_service_pack_label(text_lower: str, p: OSData) -> None:
    label = None

    if "sp1" in text_lower:
        label = "SP1"
    elif "sp2" in text_lower:
        label = "SP2"

    if label and p.product and label.lower() not in p.product.lower():
        p.product = f"{p.product} {label}"


def _apply_product_defaults(p: OSData) -> None:
    if not p.product:
        return

    defaults = PRODUCT_DEFAULTS.get(p.product)
    if not defaults:
        return

    if p.version_major is None and defaults.version_major is not None:
        p.version_major = defaults.version_major
    if p.version_minor is None and defaults.version_minor is not None:
        p.version_minor = defaults.version_minor
    if defaults.version_build and p.version_build is None:
        p.version_build = defaults.version_build
        precision = defaults.build_precision or "build"
        setattr(p, "_default_precision", precision)
        if defaults.confidence_precision:
            setattr(p, "_confidence_hint", defaults.confidence_precision)
    if defaults.kernel_version and not p.kernel_version:
        p.kernel_version = defaults.kernel_version


def _apply_contextual_version_minor(p: OSData, lower_text: str) -> None:
    if p.version_minor is not None or not p.product:
        return

    if p.product == "Windows 10" and p.version_major == 10:
        if p.edition and p.edition.lower() == "home" and "arm64" not in lower_text:
            return
        p.version_minor = 0
    elif p.product == "Windows 11" and p.version_major == 11:
        if "arm64" in lower_text or "win11" in lower_text:
            p.version_minor = 0


def _finalize_version_major(p: OSData) -> None:
    if p.product and any(x in p.product for x in ("7", "8", "10", "11")):
        digits = re.findall(r"\d+", p.product)
        if digits and p.version_major is None:
            p.version_major = int(digits[0])


def _finalize_precision(p: OSData) -> None:
    default_precision = getattr(p, "_default_precision", None)
    if p.version_build:
        if default_precision:
            p.precision = default_precision
        else:
            p.precision = "build"
        if hasattr(p, "_default_precision"):
            delattr(p, "_default_precision")
        return
    if hasattr(p, "_default_precision"):
        delattr(p, "_default_precision")
    if p.version_patch is not None:
        p.precision = "patch"
        return
    if p.product and any(x in p.product for x in ("7", "8", "10", "11")):
        p.precision = "major"
        return
    if p.product:
        p.precision = "product"
    else:
        p.precision = "family"
