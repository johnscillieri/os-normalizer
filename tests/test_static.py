"""Build a static set of test cases to verify correct parsing"""

from typing import Any

import pytest

from os_fingerprint import normalize_os

# ----------------------------------------------------------------------
# Test Cases Grouped by OS Family (Clean & Readable)
# ----------------------------------------------------------------------

# fmt: off
WINDOWS_CASES = [
    (
        "Windows NT 10.0 build 19044 Enterprise x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10", "precision": "build"},
    ),
    (
        "Windows NT 6.1 Build 7601 SP2 x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7", "precision": "build"},
    ),
    (
        "Windows NT 6.3 Build 9600 Professional x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 8.1", "precision": "build"},
    ),
    (
        "Windows 11 Pro x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Win7 SP2 x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7"}
    ),
    (
        "Windows 10 Home x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows NT 6.2 Build 9200 Enterprise x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 8"}
    ),
    (
        "Windows Server 2019 Datacenter x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2019"}
    ),
    (
        "Windows 7 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7"}
    ),
    (
        "Windows NT 10.0 build 22631 Pro ARM64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Windows NT 5.1 Build 2600 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows XP"},
    ),
    (
        "Windows NT 5.2 Build 3790 Server x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2003"},
    ),
    (
        "Windows NT 6.0 Build 6000 Enterprise x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Vista"},
    ),
    (
        "Windows NT 10.0 build 19041 Home x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows NT 10.0 build 19042 Pro x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows NT 10.0 build 19043 Education x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"},
    ),
    (
        "Windows Server 2016 Datacenter x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2016"},
    ),
    (
        "Win11 Pro ARM64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Windows NT 5.0 Build 2195 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2000"},
    ),
    (
        "Windows NT 4.0 Build 1381 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows NT 4.0"},
    ),
    (
        "Windows ME Build 3000 Home x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows ME"}
    ),
    (
        "Windows 98 Build 1998 Pro x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 98"}
    ),
    (
        "Windows NT 6.4 Build 25395 Windows 11 IoT Enterprise LTSC x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"},
    ),
    (
        "Windows NT 6.4 Build 10586 Professional x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"},
    ),
    (
        "Windows NT 6.2 Build 9200 Enterprise N x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 8"},
    ),
    (
        "Windows NT 6.1 Build 7600 Professional x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7"},
    ),
    (
        "Windows NT 5.0 Build 3790.0 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2000"},
    ),
    (
        "Windows NT 10.0 build 26100 Pro x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Windows 11 Enterprise x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Windows 11 Home ARM64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"}
    ),
    (
        "Windows 10 Pro x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows 10 Enterprise x64", {
        "family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows Server 2022 Standard x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2022"},
    ),
    (
        "Windows Server 2019 Standard x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2019"},
    ),
    (
        "Windows Server 2012 R2 Datacenter x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows Server 2012"},
    ),
    (
        "Windows NT 10.0 build 19045 Pro x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
    (
        "Windows NT 10.0 build 22631 Enterprise x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11"},
    ),
    (
        "Windows NT 10.0 build 19045 Enterprise x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"},
    ),
    (
        "Windows NT 6.1 SP2 Build 7601 Professional x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7"},
    ),
    (
        "Windows NT 10.0 SP2 Build 19045 Pro x64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10"}
    ),
]

MACOS_CASES = [
    ("Darwin 22.3.0; macOS", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS Ventura Darwin 22.0.0", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS Monterey Darwin 21.0.0", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 23.4.0; macOS Big Sur", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS Sequoia Darwin 24.0.0", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 8.0.0; Mac OS X", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 9.0.0; Mac OS X", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 19.6.0; macOS Catalina", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 20.6.0; macOS Big Sur", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 21.6.0; macOS Monterey", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 22.6.0; macOS Ventura", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 23.6.0; macOS Sonoma", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 24.6.0; macOS Sequoia", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 22.5.0; macOS", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 23.5.0; macOS", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 24.5.0; macOS", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 22.0.0; macOS arm64", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 23.0.0; macOS x86_64", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("Darwin 24.0.0; macOS x86_64", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS 14.0", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS 13.5", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS 12.6", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
    ("macOS 11.7", {"family": "macos", "vendor": "Apple", "product": "macOS"}),
]

LINUX_CASES = [
    (
        "Linux host 5.15.0-122-generic x86_64",
        {"family": "linux", "vendor": "canonical", "product": "Ubuntu"},
        {"os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy'},
    ),
    (
        "Linux host 5.10.0-30-amd64",
        {"family": "linux", "vendor": "debian", "product": "Debian GNU/Linux"},
        {"os_release": 'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="12"\nVERSION_CODENAME=bookworm'},
    ),
    (
        "Linux node 6.5.7-arch1-1",
        {"family": "linux", "vendor": "Arch", "product": "Arch Linux"},
        {"os_release": 'NAME="Arch Linux"\nID=arch\nVERSION_ID="rolling"'},
    ),
    (
        "Linux host 4.18.0-553.8.1.el8_10.x86_64",
        {"family": "linux", "vendor": "Red Hat", "product": "Red Hat Enterprise Linux"},
        {
            "os_release": '''NAME="Red Hat Enterprise Linux"
            ID=rhel
            VERSION_ID="8.10"
            PRETTY_NAME="Red Hat Enterprise Linux 8.10 (Ootpa)"'''
        },
    ),
    (
        "Linux host 5.4.0-105-amd64",
        {"family": "linux", "vendor": "Rocky", "product": "Rocky Linux"},
        {"os_release": 'NAME="Rocky Linux"\nID=rocky\nVERSION_ID="9.4"\nPRETTY_NAME="Rocky Linux 9.4 (Blue Onyx)"'},
    ),
    (
        "Linux host 5.15.0-122-generic aarch64",
        {"family": "linux", "vendor": "AlmaLinux", "product": "AlmaLinux"},
        {
            "os_release": 'NAME="AlmaLinux"\nID=almalinux\nVERSION_ID="9.4"\nPRETTY_NAME="AlmaLinux 9.4 (Seafoam Ocelot)"'
        },
    ),
    (
        "Linux host 5.15.0-122-generic arm64",
        {"family": "linux", "vendor": "Amazon", "product": "Amazon Linux"},
        {"os_release": 'NAME="Amazon Linux"\nID=amzn\nVERSION_ID="2023"\nPRETTY_NAME="Amazon Linux 2023"'},
    ),
    (
        "Linux host 3.10.0-862.el7.x86_64",
        {"family": "linux", "vendor": "Red Hat", "product": "CentOS Linux"},
        {"os_release": 'NAME="CentOS Linux"\nID=centos\nVERSION_ID="7"\nPRETTY_NAME="CentOS Linux 7 (Core)"'},
    ),
    (
        "Linux host 5.14.0-70.fc33.x86_64",
        {"family": "linux", "vendor": "Fedora Project", "product": "Fedora Linux"},
        {
            "os_release": 'NAME="Fedora Linux"\nID=fedora\nVERSION_ID="33"\nPRETTY_NAME="Fedora Linux 33 (Workstation Edition)"'
        },
    ),
    (
        "Linux host 4.19.0-18-amd64",
        {"family": "linux", "vendor": "Debian", "product": "Debian GNU/Linux"},
        {
            "os_release": 'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="10"\nPRETTY_NAME="Debian GNU/Linux 10 (buster)"'
        },
    ),
]

MOBILE_BSD_CASES = [
    ("Android 14 build UPB5.230623.003", {"family": "android", "product": "Android"}),
    ("iOS 17.5.1", {"family": "ios"}),
    ("iPadOS 16.7.6", {"family": "ios"}),
    ("FreeBSD 12.4-RELEASE", {"family": "bsd"}),
    ("OpenBSD 7.5", {"family": "bsd"}),
]

NETWORK_OS_CASES = [
    (
        "Cisco IOS XE Software, Version 17.9.1a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.9.1a.SPA.bin",
        {"family": "network-os", "vendor": "Cisco", "product": "IOS XE"},
    ),
    (
        "Cisco Nexus Operating System (NX-OS) Software nxos.9.3(5).bin N9K-C93180YC-FX",
        {"family": "network-os", "product": "NX-OS"},
    ),
    (
        "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T",
        {"family": "network-os", "vendor": "Juniper"}
    ),
    (
        "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600",
        {"family": "network-os", "vendor": "Fortinet"}
    ),
]
# fmt: on


# ----------------------------------------------------------------------
# Generate Test Cases with Descriptive IDs & Debug Info
# ----------------------------------------------------------------------


def create_test_parameters() -> list:
    """Create parameterized test cases with readable, unique names and debug context."""
    test_cases = []

    def safe_id(s: str) -> str:
        # Limit length and sanitize for pytest display
        return s.replace(" ", "_").replace("/", "_").replace(".", "_")[:30]

    # Windows
    for i, (raw, exp) in enumerate(WINDOWS_CASES):
        test_cases.append(
            pytest.param(
                raw,
                None,
                exp,
                id=f"win_{i:02d}_{safe_id(raw)}",
            )
        )

    # macOS
    for i, (raw, exp) in enumerate(MACOS_CASES):
        test_cases.append(
            pytest.param(
                raw,
                None,
                exp,
                id=f"mac_{i:02d}_{safe_id(raw)}",
            )
        )

    # Linux
    for i, entry in enumerate(LINUX_CASES):
        if len(entry) == 2:
            raw, exp = entry
            data = {}
        else:
            raw, exp, data = entry
        test_cases.append(
            pytest.param(
                raw,
                data,
                exp,
                id=f"lin_{i:02d}_{safe_id(raw)}",
            )
        )

    # Mobile/BSD
    for i, (raw, exp) in enumerate(MOBILE_BSD_CASES):
        test_cases.append(
            pytest.param(
                raw,
                None,
                exp,
                id=f"mob_{i:02d}_{safe_id(raw)}",
            )
        )

    # Network OS
    for i, (raw, exp) in enumerate(NETWORK_OS_CASES):
        test_cases.append(
            pytest.param(
                raw,
                None,
                exp,
                id=f"net_{i:02d}_{safe_id(raw)}",
            )
        )

    return test_cases


# ----------------------------------------------------------------------
# ✅ Main Test - Clear Failure Messages with Context
# ----------------------------------------------------------------------


@pytest.mark.parametrize(("text", "data", "expected"), create_test_parameters())
def test_static_os_fingerprinting(text: str, data: dict | None, expected: dict[str, Any]) -> None:
    """Test that raw OS strings are correctly normalized into structured fingerprints.

    Each case includes:
      - obs.raw: the input string (visible in test ID)
      - expected: the target fields (family/vendor/product/precision)

    On failure, detailed context is shown.
    """
    result = normalize_os(text, data)

    # Always check family
    assert result.family == expected["family"], (
        f"Input: '{text}' - Expected family='{expected['family']}', got '{result.family}'"
    )

    # Optional checks with helpful messages
    if "vendor" in expected:
        exp_vendor = (expected["vendor"] or "").lower()
        act_vendor = (result.vendor or "").lower()
        assert act_vendor == exp_vendor, f"Input: '{text}' - Expected vendor='{exp_vendor}', got '{act_vendor}'"

    if "product" in expected:
        exp_prod = (expected["product"] or "").lower()
        act_prod = (result.product or "").lower()
        assert act_prod == exp_prod, f"Input: '{text}' - Expected product='{exp_prod}', got '{act_prod}'"

    if "precision" in expected:
        assert result.precision == expected["precision"], (
            f"Input: '{text}' - Expected precision='{expected['precision']}', got '{result.precision}'"
        )

    # Confidence checks (only if precision provided)
    prec = expected.get("precision")
    if prec == "build":
        assert result.confidence >= 0.8, f"Input: '{text}' - build-level match should have high confidence"
    elif prec == "product":
        assert result.confidence >= 0.6
    elif prec == "family":
        assert result.confidence >= 0.4
