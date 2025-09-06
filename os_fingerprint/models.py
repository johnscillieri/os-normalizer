"""Data model definitions for OS fingerprinting."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class OSObservation:
    """Raw observation data supplied to the normalizer."""

    observation_id: str
    asset_anchor_kind: str
    asset_anchor_value: str
    source: str
    observed_at: datetime
    raw_os_string: Optional[str] = None
    raw_os_json: Optional[Dict[str, Any]] = None
    agent_version: Optional[str] = None
    collection_method: Optional[str] = None
    hash: Optional[str] = None


@dataclass
class OSParse:
    """Structured representation of a parsed operating system."""

    observation_id: str

    # Core identity
    family: Optional[str] = None  # windows, linux, macos, ios, android, bsd, network-os
    vendor: Optional[str] = (
        None  # Microsoft, Apple, Canonical, Cisco, Juniper, Fortinet, Huawei, Netgear…
    )
    product: Optional[str] = (
        None  # Windows 11, Ubuntu, macOS, IOS XE, Junos, FortiOS, VRP, Firmware
    )
    edition: Optional[str] = None  # Pro/Enterprise/LTSC; universalk9/ipbase; etc.
    codename: Optional[str] = None  # Sequoia; Ubuntu codename; Cisco train
    channel: Optional[str] = None  # LTS/Beta/GA/R3‑S3 etc.

    # Versions
    version_major: Optional[int] = None
    version_minor: Optional[int] = None
    version_patch: Optional[int] = None
    version_build: Optional[str] = None  # Windows build; network image tag

    # Kernel / image details
    kernel_name: Optional[str] = None
    kernel_version: Optional[str] = None
    arch: Optional[str] = None
    flavor: Optional[str] = None  # desktop/server/mobile/firewall/router/switch
    distro: Optional[str] = None
    like_distros: List[str] = field(default_factory=list)
    pretty_name: Optional[str] = None

    # Network device extras
    hw_model: Optional[str] = None
    build_id: Optional[str] = None

    # Meta information
    precision: str = "unknown"  # family|product|major|minor|patch|build
    confidence: float = 0.0
    evidence: Dict[str, Any] = field(default_factory=dict)

    # Canonical key for deduplication / indexing
    os_key: Optional[str] = None
