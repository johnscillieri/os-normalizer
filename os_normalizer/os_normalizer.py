from datetime import UTC, datetime
from typing import Any

from os_normalizer.helpers import extract_arch_from_text
from os_normalizer.models import OSParse
from os_normalizer.parsers.bsd import parse_bsd
from os_normalizer.parsers.linux import parse_linux
from os_normalizer.parsers.macos import parse_macos
from os_normalizer.parsers.mobile import parse_mobile
from os_normalizer.parsers.network import parse_network
from os_normalizer.parsers.windows import parse_windows

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
def detect_family(text: str, data: dict[str, Any]) -> tuple[str | None, float, dict[str, Any]]:
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
    if "windows" in t or "nt " in t or t.startswith("win") or data.get("os", "").lower() == "windows":
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


def normalize_os(text: str, data: dict | None = None) -> OSParse:
    text = text.strip()
    data = data or {}
    t = text.lower()

    p = OSParse()

    # Family detection
    fam, base_conf, ev = detect_family(t, data)
    p.family = fam
    p.confidence = max(p.confidence, base_conf)
    p.evidence.update(ev)

    if fam == "network-os":
        p = parse_network(text, data, p)
    elif fam == "windows":
        p = parse_windows(text, data, p)
    elif fam == "macos":
        p = parse_macos(text, data, p)
    elif fam == "linux":
        p = parse_linux(text, data, p)
    elif fam in ("android", "ios"):
        p = parse_mobile(text, data, p)
    elif fam == "bsd":
        p = parse_bsd(text, data, p)
    else:
        p.precision = "unknown"

    # Fallback arch from text if not already set elsewhere
    if not p.arch:
        p.arch = extract_arch_from_text(text)

    return p


def choose_best_fact(candidates: list[OSParse]) -> OSParse:
    if not candidates:
        raise ValueError("No candidates")
    return sorted(
        candidates,
        key=lambda c: (PRECISION_ORDER.get(c.precision, 0), c.confidence),
        reverse=True,
    )[0]


if __name__ == "__main__":
    now = datetime.now(tz=UTC)
    samples = [
        {
            "text": "Windows NT 10.0 build 22631 Enterprise x64",
        },
        {
            "text": "Darwin 24.0.0; macOS Sequoia arm64",
        },
        {
            "text": "Linux host 5.15.0-122-generic x86_64",
            "data": {
                "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"',
            },
        },
        {
            "text": "Cisco IOS XE Software, Version 17.9.4a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.09.04a.SPA.bin",
        },
        {
            "text": "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600",
        },
        {
            "text": "Cisco Nexus Operating System (NX-OS) Software nxos.9.3.5.bin N9K-C93180YC-FX",
        },
        {
            "text": "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T",
        },
        {
            "text": "Huawei VRP V800R012C00SPC500 S5720-28X-SI-AC",
        },
        {
            "text": "NETGEAR Firmware V1.0.9.88_10.2.88 R7000",
        },
        {
            "text": "Darwin Mac-Studio.local 24.6.0 Darwin Kernel Version 24.6.0: Mon Jul 14 11:30:40 PDT 2025; root:xnu-11417.140.69~1/RELEASE_ARM64_T6041 arm64",
        },
    ]

    for s in samples:
        parsed = normalize_os(text=s.get("text"), data=s.get("data"))
        print("----", s.get("text"))
        print(parsed)
        print()

