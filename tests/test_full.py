"""Full OSData object checks for representative samples"""

import pytest

from os_normalizer import OSData, normalize_os

FULL_OBJECT_CASES: list[tuple[str, dict | None, OSData]] = [
    # Windows — precise build, x64
    (
        "Windows NT 10.0 build 22631 Enterprise x64",
        None,
        OSData(
            family="windows",
            vendor="Microsoft",
            product="Windows 11",
            edition="Enterprise",
            channel="23H2",
            version_build="22631",
            kernel_name="nt",
            kernel_version="10.0.22631",
            arch="x86_64",
            precision="build",
            confidence=0.85,
            evidence={"hit": "windows", "nt_version": "10.0"},
        ),
    ),
    # macOS — alias-only (no Darwin)
    (
        "macOS Sequoia",
        None,
        OSData(
            family="macos",
            vendor="Apple",
            product="macOS",
            codename="Sequoia",
            version_major=15,
            precision="major",
            confidence=0.7,
            evidence={"hit": "macos"},
        ),
    ),
    # Windows — NT 6.1, SP2, x86 (client)
    (
        "Windows NT 6.1 Build 7601 SP2 x86",
        None,
        OSData(
            family="windows",
            vendor="Microsoft",
            product="Windows 7",
            version_patch=2,
            version_build="7601",
            kernel_name="nt",
            kernel_version=None,
            arch="x86",
            precision="build",
            confidence=0.85,
            evidence={"hit": "windows", "nt_version": "6.1", "service_pack": "SP2"},
        ),
    ),
    # Linux — kernel-only, no os-release
    (
        "Linux node 6.5.7-arch1-1",
        None,
        OSData(
            family="linux",
            vendor=None,
            product="Linux",
            kernel_name="linux",
            kernel_version="6.5.7-arch1-1",
            precision="family",
            confidence=0.6,
            evidence={"hit": "linux"},
        ),
    ),
    # Linux — dict-based os_release
    (
        "Linux host 5.4.0-70-generic",
        {"os_release": {"NAME": "Fedora Linux", "ID": "fedora", "VERSION_ID": "33"}},
        OSData(
            family="linux",
            vendor="Fedora Project",
            product="Fedora Linux",
            version_major=33,
            kernel_name="linux",
            kernel_version="5.4.0-70-generic",
            distro="fedora",
            like_distros=[],
            pretty_name="Fedora Linux",
            precision="major",
            confidence=0.7,
            evidence={"hit": "linux"},
        ),
    ),
    # Windows — NT 6.1 Server Datacenter (server detection)
    (
        "Windows NT 6.1 Build 7601 Server Datacenter x64",
        None,
        OSData(
            family="windows",
            vendor="Microsoft",
            product="Windows Server 2008 R2",
            edition="Datacenter",
            version_build="7601",
            kernel_name="nt",
            kernel_version=None,
            arch="x86_64",
            precision="build",
            confidence=0.85,
            evidence={"hit": "windows", "nt_version": "6.1"},
        ),
    ),
    # macOS — Darwin 24 => Sequoia (15), arm64
    (
        "Darwin 24.0.0; macOS Sequoia arm64",
        None,
        OSData(
            family="macos",
            vendor="Apple",
            product="macOS",
            codename="Sequoia",
            version_major=15,
            kernel_name="darwin",
            kernel_version="24.0.0",
            arch="arm64",
            precision="major",
            confidence=0.7,
            evidence={"hit": "macos"},
        ),
    ),
    # macOS — Ventura via Darwin 22, x86_64
    (
        "macOS Ventura Darwin 22.0.0 x86_64",
        None,
        OSData(
            family="macos",
            vendor="Apple",
            product="macOS",
            codename="Ventura",
            version_major=13,
            kernel_name="darwin",
            kernel_version="22.0.0",
            arch="x86_64",
            precision="major",
            confidence=0.7,
            evidence={"hit": "macos"},
        ),
    ),
    # Linux — Ubuntu with os-release, kernel and arch
    (
        "Linux host 5.15.0-122-generic x86_64",
        {
            "os_release": '''NAME="Ubuntu"
ID=ubuntu
VERSION_ID="22.04.4"
VERSION_CODENAME=jammy
PRETTY_NAME="Ubuntu 22.04.4 LTS"'''
        },
        OSData(
            family="linux",
            vendor="Canonical",
            product="Ubuntu",
            version_major=22,
            version_minor=4,
            version_patch=4,
            kernel_name="linux",
            kernel_version="5.15.0-122-generic",
            arch="x86_64",
            distro="ubuntu",
            like_distros=[],
            pretty_name="Ubuntu 22.04.4 LTS",
            codename="Jammy",
            channel="LTS",
            precision="patch",
            confidence=0.8,
            evidence={"hit": "linux"},
        ),
    ),
    # Cisco IOS XE — Amsterdam train, build id and model
    (
        "Cisco IOS XE Software, Version 17.9.1a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.9.1a.SPA.bin",
        None,
        OSData(
            family="network-os",
            vendor="Cisco",
            product="IOS XE",
            edition="universalk9",
            codename="Amsterdam",
            version_major=17,
            version_minor=9,
            version_patch=1,
            version_build="17.9.1a",
            kernel_name="ios-xe",
            hw_model="C9300-24T",
            build_id="c9300-universalk9.17.9.1a.SPA.bin",
            precision="build",
            confidence=0.85,
            evidence={"hit": "network-os", "version_raw": "17.9.1a"},
        ),
    ),
    # Cisco NX-OS — version from filename and model
    (
        "Cisco Nexus Operating System (NX-OS) Software nxos.9.3(5).bin N9K-C93180YC-FX",
        None,
        OSData(
            family="network-os",
            vendor="Cisco",
            product="NX-OS",
            version_major=9,
            version_minor=3,
            version_patch=5,
            version_build="9.3(5)",
            kernel_name="nx-os",
            hw_model="N9K-C93180YC-FX",
            precision="patch",
            confidence=0.8,
            evidence={"hit": "network-os", "version_raw": "9.3(5)"},
        ),
    ),
    # Juniper Junos — build id and model
    (
        "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T",
        None,
        OSData(
            family="network-os",
            vendor="Juniper",
            product="Junos",
            kernel_name="junos",
            version_major=20,
            version_minor=4,
            version_build="20.4R3-S3",
            hw_model="EX4300-48T",
            build_id="jinstall-ex-4300-20.4R3-S3.tgz",
            precision="build",
            confidence=0.85,
            evidence={"hit": "network-os", "version_raw": "20.4R3-S3"},
        ),
    ),
    # Fortinet — version, build, model, channel
    (
        "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600",
        None,
        OSData(
            family="network-os",
            vendor="Fortinet",
            product="FortiOS",
            version_major=7,
            version_minor=2,
            version_patch=7,
            version_build="7.2.7+build.1600",
            kernel_name="fortios",
            hw_model="FG-100F",
            build_id="FGT_7.2.7-build1600",
            channel="GA",
            precision="build",
            confidence=0.85,
            evidence={"hit": "network-os"},
        ),
    ),
    # Huawei VRP — composite version and model
    (
        "Huawei VRP V800R012C00SPC500 S5720-28X-SI-AC",
        None,
        OSData(
            family="network-os",
            vendor="Huawei",
            product="VRP",
            version_major=800,
            version_minor=12,
            version_build="V800R012C00SPC500",
            kernel_name="vrp",
            hw_model="S5720-28X-SI-AC",
            build_id="V800R012C00SPC500",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "network-os"},
        ),
    ),
    # Netgear — firmware version and model
    (
        "NETGEAR Firmware V1.0.9.88_10.2.88 R7000",
        None,
        OSData(
            family="network-os",
            vendor="Netgear",
            product="Firmware",
            version_major=1,
            version_minor=0,
            version_patch=9,
            version_build="1.0.9.88_10.2.88",
            kernel_name="firmware",
            hw_model="R7000",
            precision="patch",
            confidence=0.8,
            evidence={"hit": "network-os"},
        ),
    ),
    # iOS — patch precision
    (
        "iOS 17.5.1",
        None,
        OSData(
            family="ios",
            vendor="Apple",
            product="iOS/iPadOS",
            version_major=17,
            version_minor=5,
            version_patch=1,
            precision="patch",
            confidence=0.8,
            evidence={"hit": "ios"},
        ),
    ),
    # Android — major precision
    (
        "Android 14 build UPB5.230623.003",
        None,
        OSData(
            family="android",
            vendor="Google",
            product="Android",
            version_major=14,
            precision="major",
            confidence=0.7,
            evidence={"hit": "android"},
        ),
    ),
    # BSD — OpenBSD minor precision
    (
        "OpenBSD 7.5",
        None,
        OSData(
            family="bsd",
            vendor="OpenBSD",
            product="OpenBSD",
            version_major=7,
            version_minor=5,
            kernel_name="openbsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — FreeBSD minor precision
    (
        "FreeBSD 12.4-RELEASE",
        None,
        OSData(
            family="bsd",
            vendor="FreeBSD",
            product="FreeBSD",
            version_major=12,
            version_minor=4,
            channel="RELEASE",
            kernel_name="freebsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — NetBSD minor precision
    (
        "NetBSD 9.3",
        None,
        OSData(
            family="bsd",
            vendor="NetBSD",
            product="NetBSD",
            version_major=9,
            version_minor=3,
            kernel_name="netbsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — FreeBSD RC channel
    (
        "FreeBSD 13.2-RC1",
        None,
        OSData(
            family="bsd",
            vendor="FreeBSD",
            product="FreeBSD",
            version_major=13,
            version_minor=2,
            channel="RC1",
            kernel_name="freebsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — FreeBSD STABLE channel
    (
        "FreeBSD 13.3-STABLE",
        None,
        OSData(
            family="bsd",
            vendor="FreeBSD",
            product="FreeBSD",
            version_major=13,
            version_minor=3,
            channel="STABLE",
            kernel_name="freebsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — OpenBSD current (lowercase, space separator)
    (
        "OpenBSD 7.6 current",
        None,
        OSData(
            family="bsd",
            vendor="OpenBSD",
            product="OpenBSD",
            version_major=7,
            version_minor=6,
            channel="CURRENT",
            kernel_name="openbsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    # BSD — NetBSD BETA with underscore separator
    (
        "NetBSD 10.0_BETA",
        None,
        OSData(
            family="bsd",
            vendor="NetBSD",
            product="NetBSD",
            version_major=10,
            version_minor=0,
            channel="BETA",
            kernel_name="netbsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
]


@pytest.mark.parametrize(("text", "data", "expected"), FULL_OBJECT_CASES)
def test_full_osdata_objects(text: str, data: dict | None, expected: OSData) -> None:
    """Assert complete OSData objects for representative inputs."""
    result = normalize_os(text, data)
    assert result == expected
