"""Linux specific parsing logic."""

import re
from typing import Dict, Any

from os_fingerprint.models import OSParse
from os_fingerprint.helpers import update_confidence, parse_os_release


# Regex patterns used only by the Linux parser
KERNEL_RE = re.compile(r"\b(kernel|uname)\b.*?\b(\d+\.\d+(?:\.\d+)?(?:-\S+)?)", re.I)
# Looser Linux fallback: "Linux host 5.15.0-122-generic x86_64"
LINUX_VER_FALLBACK_RE = re.compile(
    r"\bLinux\b[^\n]*?\b(\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9._-]+)?)\b", re.I
)


def parse_linux(text: str, data: Dict[str, Any], p: OSParse) -> OSParse:
    """
    Populate an OSParse instance with Linux‑specific details.
    """
    p.kernel_name = "linux"
    osrel = None
    if isinstance(data.get("os_release"), str):
        osrel = parse_os_release(data["os_release"])
    elif isinstance(data.get("os_release"), dict):
        osrel = {k.upper(): v for k, v in data["os_release"].items()}

    # Kernel version from strict "kernel/uname ..." line
    m = KERNEL_RE.search(text)
    if m:
        p.kernel_version = m.group(2)
    else:
        # Fallback: typical "Linux host 5.15.0-122-generic ..." lines
        m2 = LINUX_VER_FALLBACK_RE.search(text)
        if m2:
            p.kernel_version = m2.group(1)

    if osrel:
        distro_id = osrel.get("ID")
        if distro_id:
            p.distro = distro_id.lower()
        like = osrel.get("ID_LIKE")
        if like:
            p.like_distros = (
                [s.lower() for s in like]
                if isinstance(like, list)
                else [str(like).lower()]
            )
        p.pretty_name = osrel.get("PRETTY_NAME") or osrel.get("NAME")

        vid = osrel.get("VERSION_ID")
        if vid:
            parts = re.split(r"[.]+", vid)
            if len(parts) >= 1 and parts[0].isdigit():
                p.version_major = int(parts[0])
            if len(parts) >= 2 and parts[1].isdigit():
                p.version_minor = int(parts[1])
            if len(parts) >= 3 and parts[2].isdigit():
                p.version_patch = int(parts[2])
        vcode = osrel.get("VERSION_CODENAME")
        if vcode:
            p.codename = vcode.title()
        if p.pretty_name and "LTS" in p.pretty_name.upper():
            p.channel = "LTS"

        vendor_by_distro = {
            "ubuntu": "Canonical",
            "debian": "Debian",
            "rhel": "Red Hat",
            "rocky": "Rocky",
            "almalinux": "AlmaLinux",
            "centos": "Red Hat",
            "amzn": "Amazon",
            "amazon": "Amazon",
            "sles": "SUSE",
            "opensuse": "SUSE",
            "arch": "Arch",
            "fedora": "Fedora Project",
        }
        if p.distro:
            p.vendor = vendor_by_distro.get(p.distro)

        p.product = (
            p.pretty_name.split()[0] if p.pretty_name else (p.distro or "Linux")
        ).replace('"', "")
        p.precision = (
            "patch"
            if p.version_patch is not None
            else (
                "minor"
                if p.version_minor is not None
                else ("major" if p.version_major is not None else "family")
            )
        )
        update_confidence(p, p.precision)
    else:
        p.product = "Linux"
        p.precision = "family"
        update_confidence(p, p.precision)

    # Fallback arch from text if not already set elsewhere
    if not p.arch:
        from os_fingerprint.helpers import extract_arch_from_text

        p.arch = extract_arch_from_text(text)

    return p
