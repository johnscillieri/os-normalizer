"""Data model definitions for OS fingerprinting."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class OSParse:
    """Structured representation of a parsed operating system."""

    # Core identity
    family: str | None = None  # windows, linux, macos, ios, android, bsd, network-os
    vendor: str | None = None  # Microsoft, Apple, Canonical, Cisco, Juniper, Fortinet, Huawei, Netgear…
    product: str | None = None  # Windows 11, Ubuntu, macOS, IOS XE, Junos, FortiOS, VRP, Firmware
    edition: str | None = None  # Pro/Enterprise/LTSC; universalk9/ipbase; etc.
    codename: str | None = None  # Sequoia; Ubuntu codename; Cisco train
    channel: str | None = None  # LTS/Beta/GA/R3-S3 etc.

    # Versions
    version_major: int | None = None
    version_minor: int | None = None
    version_patch: int | None = None
    version_build: str | None = None  # Windows build; network image tag

    # Kernel / image details
    kernel_name: str | None = None
    kernel_version: str | None = None
    arch: str | None = None
    distro: str | None = None
    like_distros: list[str] = field(default_factory=list)
    pretty_name: str | None = None

    # Network device extras
    hw_model: str | None = None
    build_id: str | None = None

    # Meta information
    precision: str = "unknown"  # family|product|major|minor|patch|build
    confidence: float = 0.0
    evidence: dict[str, Any] = field(default_factory=dict)

    # Canonical key for deduplication / indexing
    os_key: str | None = None
