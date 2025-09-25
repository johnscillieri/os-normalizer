"""Windows specific parsing logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from os_normalizer.constants import (
    WINDOWS_BUILD_MAP,
    WINDOWS_NT_CLIENT_MAP,
    WINDOWS_NT_SERVER_MAP,
    WINDOWS_PRODUCT_PATTERNS,
    WINDOWS_SERVER_BUILD_MAP,
)
from os_normalizer.helpers import extract_arch_from_text, update_confidence

if TYPE_CHECKING:
    from os_normalizer.models import OSData

VERSION_PATTERN = re.compile(r"\b(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?\b")
NT_PATTERN = re.compile(r"\bnt\s*(\d+)(?:\.(\d+))?", re.IGNORECASE)
BUILD_PATTERN = re.compile(r"\bbuild\s*(?:number\s*)?(\d{3,5})\b", re.IGNORECASE)
SP_PATTERN = re.compile(r"\bsp(\d)\b", re.IGNORECASE)

EDITION_KEYWORDS: list[tuple[str, str]] = [
    ("iot enterprise", "Enterprise"),
    ("enterprise", "Enterprise"),
    ("education", "Education"),
    ("datacenter", "Datacenter"),
    ("standard", "Standard"),
    ("professional", "Professional"),
    (" pro ", "Professional"),
    (" home ", "Home"),
]


@dataclass(frozen=True)
class ProductDefaults:
    version_major: int | None = None
    version_minor: int | None = None
    version_patch: int | None = None
    version_build: str | None = None
    kernel_version: str | None = None
    precision: str | None = None
    confidence: float | None = None


PRODUCT_DEFAULTS: dict[str, ProductDefaults] = {
    "Windows 7": ProductDefaults(6, 1, None, "7601", "6.1", "build", 0.85),
    "Windows 7 SP1": ProductDefaults(6, 1, None, "7601", "6.1", "build", 0.7),
    "Windows 8": ProductDefaults(6, 2, None, "9200", "6.2", "build", 0.7),
    "Windows 8.1": ProductDefaults(6, 3, None, "9600", "6.3", "build", 0.7),
    "Windows 10": ProductDefaults(10, None, None, None, None, "major", 0.7),
    "Windows 11": ProductDefaults(11, None, None, None, None, "major", 0.7),
    "Windows 98": ProductDefaults(4, 10, None, "1998", "4.10", "build", 0.85),
    "Windows ME": ProductDefaults(4, 90, None, "3000", "4.9", "build", 0.85),
    "Windows Server 2012": ProductDefaults(6, 2, None, "9200", "6.2", "product", 0.6),
    "Windows Server 2012 R2": ProductDefaults(6, 3, None, "9600", "6.3", "product", 0.6),
    "Windows Server 2016": ProductDefaults(10, 0, None, None, None, "product", 0.6),
    "Windows Server 2019": ProductDefaults(None, None, None, None, None, "product", 0.6),
    "Windows Server 2022": ProductDefaults(None, None, None, None, None, "product", 0.6),
}


def parse_windows(text: str, data: dict[str, Any], p: OSData) -> OSData:
    """Populate an OSData instance with Windows-specific details."""
    tl = text.lower()

    p.vendor = p.vendor or "Microsoft"
    p.kernel_name = "nt"

    arch = extract_arch_from_text(text)
    if arch:
        p.arch = arch

    product, alias = _detect_product(tl)
    server_hint = "server" in tl or (product and "server" in product.lower())

    edition = _detect_edition(tl)
    if edition:
        p.edition = edition

    nt_major: int | None = None
    nt_minor: int | None = None
    version_build: str | None = None
    version_patch: int | None = None
    channel: str | None = None
    explicit_version = False

    best = _select_best_version(text)
    if best:
        nt_major, nt_minor, version_build, version_patch = best
        explicit_version = True

    nt_match = NT_PATTERN.search(text)
    if nt_match:
        maj = int(nt_match.group(1))
        minr = int(nt_match.group(2)) if nt_match.group(2) else 0
        if nt_major is None:
            nt_major = maj
            nt_minor = minr
        else:
            nt_minor = nt_minor if nt_minor is not None else minr
        explicit_version = True

    if version_build is None:
        build_match = BUILD_PATTERN.search(text)
        if build_match:
            version_build = str(int(build_match.group(1)))
            explicit_version = True

    build_num = int(version_build) if version_build and version_build.isdigit() else None
    if build_num is not None:
        product_from_build, channel, is_server_build = _lookup_build(build_num, server_hint)
        if product_from_build and not product:
            product = product_from_build
        if is_server_build:
            server_hint = True

    if product is None and nt_major is not None and nt_minor is not None:
        product = _product_from_nt(nt_major, nt_minor, server_hint)

    if product:
        sp_match = SP_PATTERN.search(tl)
        if sp_match and "windows 7" in product.lower():
            product = f"Windows 7 SP{sp_match.group(1)}"

    if product:
        p.product = product

    if p.edition is None and edition:
        p.edition = edition

    defaults = PRODUCT_DEFAULTS.get(p.product or "")

    if nt_major is not None:
        p.version_major = nt_major
    if nt_minor is not None:
        p.version_minor = nt_minor
    if version_patch is not None:
        p.version_patch = version_patch
    if version_build is not None:
        p.version_build = version_build

    if defaults:
        if p.version_major is None and defaults.version_major is not None:
            p.version_major = defaults.version_major
        if p.version_minor is None and defaults.version_minor is not None:
            p.version_minor = defaults.version_minor
        if p.version_patch is None and defaults.version_patch is not None:
            p.version_patch = defaults.version_patch
        if p.version_build is None and defaults.version_build is not None:
            p.version_build = defaults.version_build

    kernel_version: str | None = None
    if explicit_version and nt_major is not None:
        if nt_major >= 10 and channel:
            kernel_version = channel
        elif nt_minor is not None:
            kernel_version = f"{nt_major}.{nt_minor}"
    if not kernel_version and defaults and defaults.kernel_version:
        kernel_version = defaults.kernel_version
    if kernel_version:
        p.kernel_version = kernel_version

    if p.product in ("Windows 10", "Windows 11") and p.version_minor is None:
        p.version_minor = 0

    precision = _derive_precision(p.version_major, p.version_minor, p.version_patch, p.version_build)
    if defaults and not explicit_version and defaults.precision:
        precision = defaults.precision
    p.precision = precision

    explicit_confidence = explicit_version and (nt_major is not None or version_build is not None)
    if explicit_version and nt_major is not None:
        norm_major = min(10, nt_major)
        norm_minor = nt_minor if nt_minor is not None else 0
        p.evidence["nt_version"] = f"{norm_major}.{norm_minor}"

    if explicit_confidence:
        update_confidence(p, p.precision)
    else:
        fallback_conf = defaults.confidence if defaults else None
        if fallback_conf is None:
            fallback_conf = _fallback_confidence_for_precision(p.precision)
        p.confidence = max(p.confidence, fallback_conf)

    return p


def _detect_product(tl: str) -> tuple[str | None, bool]:
    for product, patterns in WINDOWS_PRODUCT_PATTERNS:
        for token in patterns:
            if token in tl:
                alias = token.startswith("win") and not token.startswith("windows")
                return product, alias
    return None, False


def _detect_edition(tl: str) -> str | None:
    for token, label in EDITION_KEYWORDS:
        if token.strip() in {"pro", "home"}:
            pattern = rf"\b{token.strip()}\b"
            if re.search(pattern, tl):
                return label
        elif token in tl:
            return label
    return None


def _select_best_version(text: str) -> tuple[int, int, str | None, int | None] | None:
    best: tuple[int, int, str | None, int | None] | None = None
    best_score = -1
    for match in VERSION_PATTERN.finditer(text):
        major, minor, build, patch = match.groups()
        score = 2 if patch is not None else 1
        if score > best_score:
            best_score = score
            bpatch = int(patch) if patch is not None else None
            best = (int(major), int(minor), str(int(build)), bpatch)
    return best


def _lookup_build(build_num: int, server_hint: bool) -> tuple[str | None, str | None, bool]:
    candidate: tuple[str | None, str | None, bool] = (None, None, False)
    tables_to_try: list[tuple[int, int, str, str]] = []
    if server_hint:
        tables_to_try.extend(WINDOWS_SERVER_BUILD_MAP)
    tables_to_try.extend(WINDOWS_BUILD_MAP)
    for start, end, prod, channel in tables_to_try:
        if start <= build_num <= end:
            is_server = prod.lower().startswith("windows server")
            candidate = (prod, channel, is_server)
            break
    return candidate


def _product_from_nt(major: int, minor: int, server_hint: bool) -> str | None:
    key = (major, minor)
    if server_hint and key in WINDOWS_NT_SERVER_MAP:
        return WINDOWS_NT_SERVER_MAP[key]
    return WINDOWS_NT_CLIENT_MAP.get(key)


def _derive_precision(
    major: int | None,
    minor: int | None,
    patch: int | None,
    build: str | None,
) -> str:
    if build:
        return "build"
    if patch is not None and patch != 0:
        return "patch"
    if minor not in (None, 0):
        return "minor"
    if major is not None:
        return "major"
    return "product"


def _fallback_confidence_for_precision(precision: str) -> float:
    return {
        "build": 0.7,
        "patch": 0.7,
        "minor": 0.7,
        "major": 0.7,
        "product": 0.6,
    }.get(precision, 0.6)
