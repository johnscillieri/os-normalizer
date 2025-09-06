from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# ============================================================
# Ontology / Seed maps (only those not already in constants.py)
# ============================================================

# Only keep the constants that are NOT already defined in constants.py:
# ARCH_SYNONYMS, ALIASES, WINDOWS_BUILD_MAP, WINDOWS_NT_MAP, MACOS_DARWIN_MAP, CISCO_TRAIN_NAMES
# These are all already in constants.py, so we don't need to duplicate them here

# ============================================================
# Helpers (only those not already in helpers.py)
# ============================================================

# Only keep the helper functions that are NOT already in helpers.py:
# norm_arch, parse_semver_like, precision_from_parts, canonical_key
# These are all already in helpers.py, so we don't need to duplicate them here

# Architecture extraction from free text (fallback)
# Only keep ARCH_TEXT_RE that is NOT already in helpers.py
# This one is duplicated, so we can remove it from here

PRECISION_ORDER = {
    "build": 6,
    "patch": 5,
    "minor": 4,
    "major": 3,
    "product": 2,
    "family": 1,
    "unknown": 0,
}


# ============================================================
# Family detection (orchestrator logic)
# ============================================================

OS_RELEASE_KEYS = {
    "ID",
    "ID_LIKE",
    "NAME",
    "PRETTY_NAME",
    "VERSION_ID",
    "VERSION_CODENAME",
}


def parse_os_release(blob_text: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for line in blob_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().upper()
        if k not in OS_RELEASE_KEYS:
            continue
        v = v.strip().strip('"').strip("'")
        if k == "ID_LIKE":
            out[k] = [s.strip().lower() for s in re.split(r"[ ,]+", v) if s.strip()]
        else:
            out[k] = v
    return out


def detect_family(text: str, data: Dict[str, Any]) -> Tuple[Optional[str], float, Dict[str, Any]]:
    t = text.lower()
    ev = {}
    # Obvious network signals first
    if any(
        x in t
        for x in [
            "cisco",
            "nx-os",
            "ios xe",
            "ios-xe",
            "junos",
            "fortios",
            "fortigate",
            "huawei",
            "vrp",
            "netgear",
            "firmware v",
        ]
    ):
        # Special handling for 'ios' - if it's just 'ios' without 'cisco', treat as mobile, not network
        if "ios " in t and "cisco" not in t:
            ev["hit"] = "ios"
            return "ios", 0.6, ev

        ev["hit"] = "network-os"
        return "network-os", 0.7, ev
    # Linux
    if "linux" in t or any(k in data for k in ("ID", "ID_LIKE", "PRETTY_NAME", "VERSION_ID", "VERSION_CODENAME")):
        ev["hit"] = "linux"
        return "linux", 0.6, ev
    # Windows
    if "windows" in t or "nt " in t or data.get("os", "").lower() == "windows":
        ev["hit"] = "windows"
        return "windows", 0.6, ev
    # Apple
    if "macos" in t or "os x" in t or "darwin" in t:
        ev["hit"] = "macos"
        return "macos", 0.6, ev
    if "ios" in t or "ipados" in t:
        ev["hit"] = "ios"
        return "ios", 0.6, ev
    # Android
    if "android" in t:
        ev["hit"] = "android"
        return "android", 0.6, ev
    # BSD
    if "freebsd" in t or "openbsd" in t or "netbsd" in t:
        ev["hit"] = "bsd"
        return "bsd", 0.6, ev
    return None, 0.0, ev


# ============================================================
# Orchestrator (main orchestration logic)
# ============================================================


def normalize_os(observation: Any) -> Any:
    text = (observation.raw_os_string or "").strip()
    data = observation.raw_os_json or {}
    t = text.lower()

    # Apply simple aliases (helps macOS)
    # This is already in constants.py, so we can remove it from here
    # ALIASES = { ... } (duplicated)

    # Import models here to avoid circular imports
    from os_fingerprint.models import OSParse, OSObservation

    p = OSParse(
        observation_id=observation.observation_id,
        arch=None,  # Will be set by helpers or fallback
        flavor=data.get("flavor"),
    )

    # Fallback arch from raw string if not supplied
    # ARCH_TEXT_RE and extract_arch_from_text are in helpers.py, so we can remove these
    # p.arch = extract_arch_from_text(text)

    # Family detection
    fam, base_conf, ev = detect_family(t, data)
    p.family = fam
    p.confidence = max(p.confidence, base_conf)
    p.evidence.update(ev)

    # Network vendors (early if detected)
    if fam == "network-os":
        # Import network parsers here to avoid circular imports
        from os_fingerprint.parsers.network import parse_network

        p = parse_network(text, data, p)
    else:
        # Desktop/Server branches
        if fam == "windows":
            from os_fingerprint.parsers.windows import parse_windows

            p = parse_windows(text, data, p)
        elif fam == "macos":
            from os_fingerprint.parsers.macos import parse_macos

            p = parse_macos(text, data, p)
        elif fam == "linux":
            from os_fingerprint.parsers.linux import parse_linux

            p = parse_linux(text, data, p)
        elif fam in ("android", "ios"):
            from os_fingerprint.parsers.mobile import parse_mobile

            p = parse_mobile(text, data, p)

        elif fam == "bsd":
            # For mobile OS, we can also use the generic BSD parser
            from os_fingerprint.parsers.bsd import parse_bsd

            p = parse_bsd(text, data, p)
        else:
            # Try weak hints
            if "windows" in t:
                p.family = "windows"
                from os_fingerprint.parsers.windows import parse_windows

                p = parse_windows(text, data, p)
            elif "darwin" in t or "macos" in t or "os x" in t:
                p.family = "macos"
                from os_fingerprint.parsers.macos import parse_macos

                p = parse_macos(text, data, p)
            elif "linux" in t:
                p.family = "linux"
                from os_fingerprint.parsers.linux import parse_linux

                p = parse_linux(text, data, p)
            elif any(x in t for x in ["cisco", "junos", "fortios", "vrp", "netgear"]):
                p.family = "network-os"
                from os_fingerprint.parsers.network import parse_network

                return normalize_os(observation)  # re-run with family fixed
            else:
                p.precision = "unknown"

    # Canonical key (this is in helpers.py, so we can remove it)
    # p.os_key = canonical_key(p)
    return p


# ============================================================
# Reconciliation (many parses -> one fact)
# ============================================================


def choose_best_fact(candidates: List[Any]) -> Any:
    if not candidates:
        raise ValueError("No candidates")
    return sorted(
        candidates,
        key=lambda c: (PRECISION_ORDER.get(c.precision, 0), c.confidence),
        reverse=True,
    )[0]


# ============================================================
# Manual smoke run
# ============================================================

if __name__ == "__main__":
    # Import the OSObservation class for the test cases
    from os_fingerprint.models import OSObservation

    now = datetime.utcnow()
    samples = [
        OSObservation(
            "1",
            "hostname",
            "pc-01",
            "agent-a",
            now,
            "Windows NT 10.0 build 22631 Enterprise x64",
        ),
        OSObservation(
            "2",
            "hostname",
            "mac-01",
            "agent-b",
            now,
            "Darwin 24.0.0; macOS Sequoia arm64",
        ),
        OSObservation(
            "3",
            "hostname",
            "lin-01",
            "agent-c",
            now,
            "Linux host 5.15.0-122-generic x86_64",
            {
                "arch": None,
                "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"',
            },
        ),
        OSObservation(
            "4",
            "hostname",
            "sw-01",
            "agent-d",
            now,
            "Cisco IOS XE Software, Version 17.9.4a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.09.04a.SPA.bin",
        ),
        OSObservation(
            "5",
            "hostname",
            "fw-01",
            "agent-e",
            now,
            "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600",
        ),
        OSObservation(
            "6",
            "hostname",
            "sw-02",
            "agent-f",
            now,
            "Cisco Nexus Operating System (NX-OS) Software nxos.9.3.5.bin N9K-C93180YC-FX",
        ),
        OSObservation(
            "7",
            "hostname",
            "ex-01",
            "agent-g",
            now,
            "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T",
        ),
        OSObservation(
            "8",
            "hostname",
            "ce-01",
            "agent-h",
            now,
            "Huawei VRP V800R012C00SPC500 S5720-28X-SI-AC",
        ),
        OSObservation(
            "9",
            "hostname",
            "ap-01",
            "agent-i",
            now,
            "NETGEAR Firmware V1.0.9.88_10.2.88 R7000",
        ),
    ]

    for s in samples:
        parsed = normalize_os(s)
        print("----", s.raw_os_string)
        print(parsed)
