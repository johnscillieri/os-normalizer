"""Network gear specific parsing logic."""

import re
from typing import Any

from os_fingerprint.helpers import update_confidence
from os_fingerprint.models import OSParse

# Regex patterns used only by the network parser
# Cisco
CISCO_IOS_XE_RE = re.compile(r"(ios[\s-]?xe)", re.IGNORECASE)
CISCO_IOS_RE = re.compile(r"\bios(?!\s?xe)\b", re.IGNORECASE)
CISCO_NXOS_RE = re.compile(r"\bnx-?os\b|\bNexus Operating System\b", re.IGNORECASE)
CISCO_VERSION_RE = re.compile(
    r"\bVersion\s+([0-9]+\.[0-9.()a-zA-Z]+)\b|\bnxos\.(\d+\.\d+(?:\.\d+|\(\d+\)))", re.IGNORECASE
)
CISCO_IMAGE_RE = re.compile(r"\b([a-z0-9][a-z0-9_.-]+\.bin)\b", re.IGNORECASE)
CISCO_MODEL_RE = re.compile(
    r"\b(N9K-[A-Z0-9-]+|C\d{3,4}[\w-]+|ASR\d{3,4}[\w-]*|ISR\d{3,4}[\w/-]*|Catalyst\s?\d{3,4}[\w-]*)\b",
    re.IGNORECASE,
)
CISCO_EDITION_RE = re.compile(
    r"\b(universalk9|ipbase|adv(ip)?services|metroipaccess|securityk9|datak9)\b", re.IGNORECASE
)

# Juniper
JUNOS_RE = re.compile(r"\bjunos\b", re.IGNORECASE)
JUNOS_VER_RE = re.compile(r"\b(\d{1,2}\.\d{1,2}R\d+(?:-\w+\d+)?)\b", re.IGNORECASE)
JUNOS_PKG_RE = re.compile(r"\b(jinstall-[a-z0-9-]+\.tgz)\b", re.IGNORECASE)
JUNOS_MODEL_RE = re.compile(r"\b(EX\d{3,4}-\d{2}[A-Z]?|QFX\d{3,4}\w*|SRX\d{3,4}\w*|MX\d{2,3}\w*)\b", re.IGNORECASE)

# Fortinet
FORTI_RE = re.compile(r"\bforti(os|gate)\b", re.IGNORECASE)
FORTI_VER_RE = re.compile(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", re.IGNORECASE)
FORTI_BUILD_RE = re.compile(r"\bbuild\s?(\d{3,5})\b", re.IGNORECASE)
FORTI_IMG_RE = re.compile(r"\b(FGT_[0-9.]+-build\d{3,5})\b", re.IGNORECASE)
FORTI_MODEL_RE = re.compile(r"\b(FortiGate-?\d+[A-Z]?|FG-\d+[A-Z]?)\b", re.IGNORECASE)
FORTI_CHANNEL_RE = re.compile(r"\((GA|Patch|Beta)\)", re.IGNORECASE)

# Huawei VRP
HUAWEI_RE = re.compile(r"\bhuawei\b|\bvrp\b", re.IGNORECASE)
HUAWEI_VER_RE = re.compile(r"\bV(\d{3})R(\d{3})C(\d+)(SPC\d+)?\b", re.IGNORECASE)
HUAWEI_RAWVER_RE = re.compile(r"\bV\d{3}R\d{3}C\d+(?:SPC\d+)?\b", re.IGNORECASE)
HUAWEI_MODEL_RE = re.compile(r"\b(S\d{4}-\d{2}[A-Z-]+|CE\d{4}[A-Z-]*|AR\d{3,4}[A-Z-]*)\b", re.IGNORECASE)

# Netgear
NETGEAR_RE = re.compile(r"\bnetgear\b|\bfirmware\b", re.IGNORECASE)
NETGEAR_VER_RE = re.compile(r"\bV(\d+\.\d+\.\d+(?:_\d+\.\d+\.\d+)?)\b", re.IGNORECASE)
NETGEAR_MODEL_RE = re.compile(r"\b([RN][0-9]{3,4}[A-Z]?)\b", re.IGNORECASE)


def parse_network(text: str, data: dict[str, Any], p: OSParse) -> OSParse:
    """Populate an OSParse instance with network gear specific details."""
    t = text

    # Vendor detection
    if "cisco" in t or CISCO_IOS_XE_RE.search(t) or CISCO_IOS_RE.search(t) or CISCO_NXOS_RE.search(t):
        p.vendor = "Cisco"
        p.family = p.family or "network-os"

        # Detect product line
        if CISCO_IOS_XE_RE.search(t):
            p.product, p.kernel_name = "IOS XE", "ios-xe"
        elif CISCO_NXOS_RE.search(t):
            p.product, p.kernel_name = "NX-OS", "nx-os"
        elif CISCO_IOS_RE.search(t):
            p.product, p.kernel_name = "IOS", "ios"
        else:
            p.product = p.product or "Cisco OS"

        # Version (Version X or nxos.X from text)
        vm = CISCO_VERSION_RE.search(t)
        if vm:
            ver = vm.group(1) or vm.group(2)
            if ver:
                p.evidence["version_raw"] = ver
                num = re.findall(r"\d+", ver)
                if len(num) >= 1:
                    p.version_major = int(num[0])
                if len(num) >= 2:
                    p.version_minor = int(num[1])
                if len(num) >= 3:
                    p.version_patch = int(num[2])
                p.version_build = ver
                p.precision = (
                    "patch" if p.version_patch is not None else ("minor" if p.version_minor is not None else "major")
                )

        # Image filename
        img = CISCO_IMAGE_RE.search(t)
        if img:
            p.build_id = img.group(1)
            p.precision = "build"

        # If NX-OS and we only got version via filename, parse nxos.A.B.C.bin
        if not p.version_major and p.build_id:
            m = re.search(r"nxos\.(\d+)\.(\d+)\.(\d+)", p.build_id, re.IGNORECASE)
            if m:
                p.version_major = int(m.group(1))
                p.version_minor = int(m.group(2))
                p.version_patch = int(m.group(3))
                p.version_build = f"{p.version_major}.{p.version_minor}.{p.version_patch}"
                p.precision = "patch"

        # Model
        mm = CISCO_MODEL_RE.search(t)
        if mm:
            p.hw_model = mm.group(1)

        # Edition (universalk9/ipbase)
        fl = CISCO_EDITION_RE.search(t)
        if fl:
            p.edition = fl.group(1).lower()

        # Train codename
        from os_fingerprint.constants import CISCO_TRAIN_NAMES

        for train in CISCO_TRAIN_NAMES:
            if train.lower() in t:
                p.codename = train
                break

        # Boost confidence based on precision
        update_confidence(p, p.precision if p.precision in ("build", "patch") else "minor")

    elif JUNOS_RE.search(t):
        p.vendor = "Juniper"
        p.product = "Junos"
        p.family = p.family or "network-os"
        p.kernel_name = "junos"

        vm = JUNOS_VER_RE.search(t)
        if vm:
            ver = vm.group(1)
            p.evidence["version_raw"] = ver
            nums = re.findall(r"\d+", ver)
            if nums:
                p.version_major = int(nums[0])
            if len(nums) >= 2:
                p.version_minor = int(nums[1])
            # R3-S3 suffix kept in version_build
            p.version_build = ver
            p.precision = "minor"

        pkg = JUNOS_PKG_RE.search(t)
        if pkg:
            p.build_id = pkg.group(1)
            p.precision = "build"

        mdl = JUNOS_MODEL_RE.search(t)
        if mdl:
            p.hw_model = mdl.group(1)

        # Boost confidence based on precision
        update_confidence(p, p.precision if p.precision in ("build", "minor") else "major")

    elif FORTI_RE.search(t):
        p.vendor = "Fortinet"
        p.product = "FortiOS"
        p.family = p.family or "network-os"
        p.kernel_name = "fortios"

        ver = FORTI_VER_RE.search(t)
        if ver:
            v = ver.group(1)
            nums = re.findall(r"\d+", v)
            if nums:
                p.version_major = int(nums[0])
            if len(nums) >= 2:
                p.version_minor = int(nums[1])
            if len(nums) >= 3:
                p.version_patch = int(nums[2])
            p.version_build = v
            p.precision = (
                "patch" if p.version_patch is not None else ("minor" if p.version_minor is not None else "major")
            )

        bld = FORTI_BUILD_RE.search(t)
        if bld:
            p.version_build = (p.version_build or "") + f"+build.{bld.group(1)}"
            p.precision = "build"

        img = FORTI_IMG_RE.search(t)
        if img:
            p.build_id = img.group(1)
            p.precision = "build"

        mdl = FORTI_MODEL_RE.search(t)
        if mdl:
            p.hw_model = mdl.group(1).replace("FortiGate-", "FG-")

        ch = FORTI_CHANNEL_RE.search(t)
        if ch:
            p.channel = ch.group(1).upper()

        # Boost confidence based on precision
        update_confidence(p, p.precision if p.precision in ("build", "patch") else "minor")

    elif HUAWEI_RE.search(t):
        p.vendor = "Huawei"
        p.product = "VRP"
        p.family = p.family or "network-os"
        p.kernel_name = "vrp"

        raw = HUAWEI_RAWVER_RE.search(t)
        if raw:
            p.version_build = raw.group(0)

        vm = HUAWEI_VER_RE.search(t)
        if vm:
            maj, r, c = vm.group(1), vm.group(2), vm.group(3)
            p.version_major = int(maj)
            p.version_minor = int(r)
            # Cxx not numeric; keep patch None, store composite in version_build
            p.precision = "minor"

        mdl = HUAWEI_MODEL_RE.search(t)
        if mdl:
            p.hw_model = mdl.group(1)

        p.build_id = p.version_build or p.build_id

        # Boost confidence based on precision
        update_confidence(p, p.precision if p.precision in ("minor", "build") else "major")

    elif NETGEAR_RE.search(t):
        p.vendor = "Netgear"
        p.product = "Firmware"
        p.family = p.family or "network-os"
        p.kernel_name = "firmware"

        vm = NETGEAR_VER_RE.search(t)
        if vm:
            v = vm.group(1)
            nums = re.findall(r"\d+", v)
            if nums:
                p.version_major = int(nums[0])
            if len(nums) >= 2:
                p.version_minor = int(nums[1])
            if len(nums) >= 3:
                p.version_patch = int(nums[2])
            p.version_build = v
            p.precision = (
                "patch" if p.version_patch is not None else ("minor" if p.version_minor is not None else "major")
            )

        mdl = NETGEAR_MODEL_RE.search(t)
        if mdl:
            p.hw_model = mdl.group(1)

        # Boost confidence based on precision
        update_confidence(p, "minor" if p.precision == "major" else p.precision)

    else:
        # Unknown network vendor; keep coarse
        p.vendor = p.vendor or "Unknown-Network"
        p.product = p.product or "Network OS"
        p.precision = "family"

    return p
