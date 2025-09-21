"""Comprehensive normalization tests grouped by platform."""

from typing import Any

import pytest

from os_normalizer import OSData, normalize_os

# ----------------------------------------------------------------------
# Test Cases Grouped by OS Family (Clean & Readable)
# ----------------------------------------------------------------------

WINDOWS_CASES = [
    (
        "Windows NT 10.0 build 19044 Enterprise x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "precision": "build",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "10.0.19044",
            "channel": "2004/20H2/21H1/21H2/22H2",
        },
    ),
    (
        "Windows NT 6.1 Build 7601 SP1 x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 7",
            "precision": "build",
            "arch": "x86",
            "kernel_name": "nt",
            "kernel_version": "6.1.7601",
        },
    ),
    (
        "Windows NT 6.3 Build 9600 Professional x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 8.1",
            "precision": "build",
            "arch": "x86_64",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "6.3.9600",
        },
    ),
    (
        "Windows 11 Pro x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11", "arch": "x86_64", "kernel_name": "nt"},
    ),
    (
        "Win7 SP1 x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 7", "arch": "x86", "kernel_name": "nt"},
    ),
    (
        "Windows 10 Home x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Home",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows NT 6.2 Build 9200 Enterprise x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 8",
            "arch": "x86",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "6.2.9200",
        },
    ),
    (
        "Windows Server 2019 Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2019",
            "arch": "x86_64",
            "edition": "Datacenter",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows 7 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 7",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows NT 10.0 build 22631 Pro ARM64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "arm64",
            "kernel_name": "nt",
            "kernel_version": "10.0.22631",
            "channel": "23H2",
            "edition": "Professional",
        },
    ),
    (
        "Windows NT 5.1 Build 2600 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows XP",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "5.1.2600",
        },
    ),
    (
        "Windows NT 5.2 Build 3790 Server x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2003",
            "arch": "x86_64",
            "kernel_name": "nt",
            "kernel_version": "5.2.3790",
        },
    ),
    (
        "Windows NT 6.0 Build 6000 Enterprise x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Vista",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "6.0.6000",
        },
    ),
    (
        "Windows NT 10.0 build 19041 Home x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Home",
            "kernel_name": "nt",
            "kernel_version": "10.0.19041",
            "channel": "2004/20H2/21H1/21H2/22H2",
        },
    ),
    (
        "Windows NT 10.0 build 19042 Pro x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "kernel_name": "nt",
            "kernel_version": "10.0.19042",
            "channel": "2004/20H2/21H1/21H2/22H2",
            "edition": "Professional",
        },
    ),
    (
        "Windows NT 10.0 build 19043 Education x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Education",
            "kernel_name": "nt",
            "kernel_version": "10.0.19043",
            "channel": "2004/20H2/21H1/21H2/22H2",
        },
    ),
    (
        "Windows Server 2016 Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2016",
            "arch": "x86_64",
            "edition": "Datacenter",
            "kernel_name": "nt",
        },
    ),
    (
        "Win11 Pro ARM64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 11", "arch": "arm64", "kernel_name": "nt"},
    ),
    (
        "Windows NT 5.0 Build 2195 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 2000",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "5.0.2195",
        },
    ),
    (
        "Windows NT 4.0 Build 1381 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows NT 4.0",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "4.0.1381",
        },
    ),
    (
        "Windows ME Build 3000 Home x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows ME", "arch": "x86", "edition": "Home"},
    ),
    (
        "Windows 98 Build 1998 Pro x86",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 98", "arch": "x86"},
    ),
    (
        "Windows NT 10.0 Build 25395 Windows 11 IoT Enterprise LTSC x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "10.0.25395",
            "channel": "23H2",
        },
    ),
    (
        "Windows NT 10.0 Build 10586 Professional x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "10.0.10586",
            "channel": "1511",
        },
    ),
    (
        "Windows NT 6.2 Build 9200 Enterprise N x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 8",
            "arch": "x86",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "6.2.9200",
        },
    ),
    (
        "Windows NT 6.1 Build 7600 Professional x86_64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 7",
            "arch": "x86_64",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "6.1.7600",
        },
    ),
    (
        "Windows NT 5.0 Build 2195 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 2000",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows NT 10.0 build 26100 Pro x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "x86_64",
            "kernel_name": "nt",
            "kernel_version": "10.0.26100",
            "channel": "24H2",
            "edition": "Professional",
        },
    ),
    (
        "Windows 11 Enterprise x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows 11 Home ARM64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "arm64",
            "edition": "Home",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows 10 Pro x86_64",
        {"family": "windows", "vendor": "Microsoft", "product": "Windows 10", "arch": "x86_64", "kernel_name": "nt"},
    ),
    (
        "Windows 10 Enterprise x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows Server 2022 Standard x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2022",
            "arch": "x86_64",
            "edition": "Standard",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows Server 2019 Standard x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2019",
            "arch": "x86_64",
            "edition": "Standard",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows Server 2012 R2 Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2012 R2",
            "arch": "x86_64",
            "edition": "Datacenter",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows NT 10.0 build 22631 Enterprise x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 11",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "10.0.22631",
            "channel": "23H2",
        },
    ),
    (
        "Windows NT 10.0 build 19045 Enterprise x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "arch": "x86_64",
            "edition": "Enterprise",
            "kernel_name": "nt",
            "kernel_version": "10.0.19045",
            "channel": "2004/20H2/21H1/21H2/22H2",
        },
    ),
    (
        "Windows NT 6.1 SP1 Build 7601 Professional x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 7",
            "arch": "x86",
            "edition": "Professional",
            "kernel_name": "nt",
            "kernel_version": "6.1.7601",
        },
    ),
    # Explicit server variants for ambiguous NT versions
    (
        "Windows NT 6.1 Build 7601 Server Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2008 R2",
            "precision": "build",
            "arch": "x86_64",
            "edition": "Datacenter",
            "kernel_name": "nt",
        },
    ),
    (
        "Windows NT 6.0 Build 6001 Server Standard x86",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2008",
            "precision": "build",
            "arch": "x86",
            "edition": "Standard",
            "kernel_name": "nt",
            "kernel_version": "6.0.6001",
        },
    ),
    (
        "Windows NT 6.2 Build 9200 Server Standard x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2012",
            "precision": "build",
            "arch": "x86_64",
            "edition": "Standard",
            "kernel_name": "nt",
            "kernel_version": "6.2.9200",
        },
    ),
    (
        "Windows NT 6.3 Build 9600 Server Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2012 R2",
            "precision": "build",
            "arch": "x86_64",
            "edition": "Datacenter",
            "kernel_name": "nt",
            "kernel_version": "6.3.9600",
        },
    ),
    (
        "Windows NT 10.0 Build 19045 Pro x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows 10",
            "edition": "Professional",
            "arch": "x86_64",
            "kernel_name": "nt",
            "kernel_version": "10.0.19045",
            "channel": "2004/20H2/21H1/21H2/22H2",
        },
    ),
    # Server build mapping (NT 10.0+)
    (
        "Windows NT 10.0 build 14393 Server Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2016",
            "precision": "build",
            "kernel_version": "10.0.14393",
            "channel": "1607",
        },
    ),
    (
        "Windows NT 10.0 build 17763 Server Standard x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2019",
            "precision": "build",
            "kernel_version": "10.0.17763",
            "channel": "1809",
        },
    ),
    (
        "Windows NT 10.0 build 20348 Server Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2022",
            "precision": "build",
            "kernel_version": "10.0.20348",
            "channel": "21H2",
        },
    ),
    (
        "Windows NT 10.0 build 26100 Server Datacenter x64",
        {
            "family": "windows",
            "vendor": "Microsoft",
            "product": "Windows Server 2025",
            "precision": "build",
            "kernel_version": "10.0.26100",
            "channel": "24H2",
        },
    ),
]

MACOS_CASES = [
    (
        "Darwin Mac-Studio.local 25.0.0 Darwin Kernel Version 25.0.0: Mon Aug 25 21:17:54 PDT 2025; root:xnu-12377.1.9~3/RELEASE_ARM64_T6041 arm64",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 26,
            "codename": "Tahoe",
            "kernel_name": "darwin",
            "kernel_version": "25.0.0",
            "arch": "arm64",
        },
    ),
    (
        "Darwin 22.3.0; macOS",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 13,
            "codename": "Ventura",
            "kernel_name": "darwin",
            "kernel_version": "22.3.0",
        },
    ),
    (
        "macOS Ventura Darwin 22.0.0",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 13,
            "codename": "Ventura",
            "kernel_name": "darwin",
            "kernel_version": "22.0.0",
        },
    ),
    (
        "macOS Monterey Darwin 21.0.0",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 12,
            "codename": "Monterey",
            "kernel_name": "darwin",
            "kernel_version": "21.0.0",
        },
    ),
    (
        "Darwin 23.4.0; macOS Big Sur",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 14,
            "codename": "Sonoma",
            "kernel_name": "darwin",
            "kernel_version": "23.4.0",
        },
    ),
    (
        "macOS Sequoia Darwin 24.0.0",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 15,
            "codename": "Sequoia",
            "kernel_name": "darwin",
            "kernel_version": "24.0.0",
        },
    ),
    (
        "Darwin 8.0.0; Mac OS X",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "kernel_name": "darwin",
            "kernel_version": "8.0.0",
        },
    ),
    (
        "Darwin 9.0.0; Mac OS X",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "kernel_name": "darwin",
            "kernel_version": "9.0.0",
        },
    ),
    (
        "Darwin 19.6.0; macOS Catalina",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "minor",
            "version_major": 10,
            "version_minor": 15,
            "codename": "Catalina",
            "kernel_name": "darwin",
            "kernel_version": "19.6.0",
        },
    ),
    (
        "Darwin 20.6.0; macOS Big Sur",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 11,
            "codename": "Big Sur",
            "kernel_name": "darwin",
            "kernel_version": "20.6.0",
        },
    ),
    (
        "Darwin 21.6.0; macOS Monterey",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 12,
            "codename": "Monterey",
            "kernel_name": "darwin",
            "kernel_version": "21.6.0",
        },
    ),
    (
        "Darwin 22.6.0; macOS Ventura",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 13,
            "codename": "Ventura",
            "kernel_name": "darwin",
            "kernel_version": "22.6.0",
        },
    ),
    (
        "Darwin 23.6.0; macOS Sonoma",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 14,
            "codename": "Sonoma",
            "kernel_name": "darwin",
            "kernel_version": "23.6.0",
        },
    ),
    (
        "Darwin 24.6.0; macOS Sequoia",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 15,
            "codename": "Sequoia",
            "kernel_name": "darwin",
            "kernel_version": "24.6.0",
        },
    ),
    (
        "Darwin 22.5.0; macOS",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 13,
            "codename": "Ventura",
            "kernel_name": "darwin",
            "kernel_version": "22.5.0",
        },
    ),
    (
        "Darwin 23.5.0; macOS",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 14,
            "codename": "Sonoma",
            "kernel_name": "darwin",
            "kernel_version": "23.5.0",
        },
    ),
    (
        "Darwin 24.5.0; macOS",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 15,
            "codename": "Sequoia",
            "kernel_name": "darwin",
            "kernel_version": "24.5.0",
        },
    ),
    (
        "Darwin 22.0.0; macOS arm64",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 13,
            "codename": "Ventura",
            "kernel_name": "darwin",
            "kernel_version": "22.0.0",
            "arch": "arm64",
        },
    ),
    (
        "Darwin 23.0.0; macOS x86_64",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 14,
            "codename": "Sonoma",
            "kernel_name": "darwin",
            "kernel_version": "23.0.0",
            "arch": "x86_64",
        },
    ),
    (
        "Darwin 24.0.0; macOS x86_64",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "major",
            "version_major": 15,
            "codename": "Sequoia",
            "kernel_name": "darwin",
            "kernel_version": "24.0.0",
            "arch": "x86_64",
        },
    ),
    (
        "macOS 14.0",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "minor",
            "version_major": 14,
            "version_minor": 0,
        },
    ),
    (
        "macOS 13.5",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "minor",
            "version_major": 13,
            "version_minor": 5,
        },
    ),
    (
        "macOS 12.6",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "minor",
            "version_major": 12,
            "version_minor": 6,
        },
    ),
    (
        "macOS 11.7",
        {
            "family": "macos",
            "vendor": "Apple",
            "product": "macOS",
            "precision": "minor",
            "version_major": 11,
            "version_minor": 7,
        },
    ),
]

LINUX_CASES = [
    (
        "Linux host 5.15.0-122-generic x86_64",
        {
            "family": "linux",
            "vendor": "Canonical",
            "product": "Ubuntu",
            "precision": "patch",
            "version_major": 22,
            "version_minor": 4,
            "version_patch": 4,
            "codename": "Jammy",
            "distro": "ubuntu",
            "pretty_name": "Ubuntu",
            "kernel_name": "linux",
            "kernel_version": "5.15.0-122-generic",
            "arch": "x86_64",
        },
        {"os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy'},
    ),
    (
        "Linux host 5.10.0-30-amd64",
        {
            "family": "linux",
            "vendor": "Debian",
            "product": "Debian GNU/Linux",
            "precision": "major",
            "version_major": 12,
            "codename": "Bookworm",
            "distro": "debian",
            "pretty_name": "Debian GNU/Linux",
            "kernel_name": "linux",
            "kernel_version": "5.10.0-30-amd64",
            "arch": "x86_64",
        },
        {"os_release": 'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="12"\nVERSION_CODENAME=bookworm'},
    ),
    (
        "Linux node 6.5.7-arch1-1",
        {
            "family": "linux",
            "vendor": "Arch",
            "product": "Arch Linux",
            "precision": "family",
            "distro": "arch",
            "pretty_name": "Arch Linux",
            "kernel_name": "linux",
            "kernel_version": "6.5.7-arch1-1",
        },
        {"os_release": 'NAME="Arch Linux"\nID=arch\nVERSION_ID="rolling"'},
    ),
    (
        "Linux host 4.18.0-553.8.1.el8_10.x86_64",
        {
            "family": "linux",
            "vendor": "Red Hat",
            "product": "Red Hat Enterprise Linux",
            "precision": "minor",
            "version_major": 8,
            "version_minor": 10,
            "codename": "Ootpa",
            "distro": "rhel",
            "pretty_name": "Red Hat Enterprise Linux 8.10 (Ootpa)",
            "kernel_name": "linux",
            "kernel_version": "4.18.0-553.8.1.el8_10.x86_64",
            "arch": "x86_64",
        },
        {
            "os_release": '''NAME="Red Hat Enterprise Linux"
            ID=rhel
            VERSION_ID="8.10"
            PRETTY_NAME="Red Hat Enterprise Linux 8.10 (Ootpa)"'''
        },
    ),
    (
        "Linux host 5.4.0-105-amd64",
        {
            "family": "linux",
            "vendor": "Rocky",
            "product": "Rocky Linux",
            "precision": "minor",
            "version_major": 9,
            "version_minor": 4,
            "codename": "Blue Onyx",
            "distro": "rocky",
            "pretty_name": "Rocky Linux 9.4 (Blue Onyx)",
            "kernel_name": "linux",
            "kernel_version": "5.4.0-105-amd64",
            "arch": "x86_64",
        },
        {"os_release": 'NAME="Rocky Linux"\nID=rocky\nVERSION_ID="9.4"\nPRETTY_NAME="Rocky Linux 9.4 (Blue Onyx)"'},
    ),
    (
        "Linux host 5.15.0-122-generic aarch64",
        {
            "family": "linux",
            "vendor": "AlmaLinux",
            "product": "AlmaLinux",
            "precision": "minor",
            "version_major": 9,
            "version_minor": 4,
            "codename": "Seafoam Ocelot",
            "distro": "almalinux",
            "pretty_name": "AlmaLinux 9.4 (Seafoam Ocelot)",
            "kernel_name": "linux",
            "kernel_version": "5.15.0-122-generic",
            "arch": "arm64",
        },
        {
            "os_release": 'NAME="AlmaLinux"\nID=almalinux\nVERSION_ID="9.4"\nPRETTY_NAME="AlmaLinux 9.4 (Seafoam Ocelot)"'
        },
    ),
    (
        "Linux host 5.15.0-122-generic arm64",
        {
            "family": "linux",
            "vendor": "Amazon",
            "product": "Amazon Linux",
            "precision": "major",
            "version_major": 2023,
            "distro": "amzn",
            "pretty_name": "Amazon Linux 2023",
            "kernel_name": "linux",
            "kernel_version": "5.15.0-122-generic",
            "arch": "arm64",
        },
        {"os_release": 'NAME="Amazon Linux"\nID=amzn\nVERSION_ID="2023"\nPRETTY_NAME="Amazon Linux 2023"'},
    ),
    (
        "Linux host 3.10.0-862.el7.x86_64",
        {
            "family": "linux",
            "vendor": "Red Hat",
            "product": "CentOS Linux",
            "precision": "major",
            "version_major": 7,
            "codename": "Core",
            "distro": "centos",
            "pretty_name": "CentOS Linux 7 (Core)",
            "kernel_name": "linux",
            "kernel_version": "3.10.0-862.el7.x86_64",
            "arch": "x86_64",
        },
        {"os_release": 'NAME="CentOS Linux"\nID=centos\nVERSION_ID="7"\nPRETTY_NAME="CentOS Linux 7 (Core)"'},
    ),
    (
        "Linux host 5.14.0-70.fc33.x86_64",
        {
            "family": "linux",
            "vendor": "Fedora Project",
            "product": "Fedora Linux",
            "precision": "major",
            "version_major": 33,
            "codename": "Workstation Edition",
            "distro": "fedora",
            "pretty_name": "Fedora Linux 33 (Workstation Edition)",
            "kernel_name": "linux",
            "kernel_version": "5.14.0-70.fc33.x86_64",
            "arch": "x86_64",
        },
        {
            "os_release": 'NAME="Fedora Linux"\nID=fedora\nVERSION_ID="33"\nPRETTY_NAME="Fedora Linux 33 (Workstation Edition)"'
        },
    ),
    (
        "Linux host 4.19.0-18-amd64",
        {
            "family": "linux",
            "vendor": "Debian",
            "product": "Debian GNU/Linux",
            "precision": "major",
            "version_major": 10,
            "distro": "debian",
            "codename": "Buster",
            "pretty_name": "Debian GNU/Linux 10 (buster)",
            "kernel_name": "linux",
            "kernel_version": "4.19.0-18-amd64",
            "arch": "x86_64",
        },
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
    ("Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T", {"family": "network-os", "vendor": "Juniper"}),
    ("FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600", {"family": "network-os", "vendor": "Fortinet"}),
]


# ----------------------------------------------------------------------
# Generate Test Cases with Descriptive IDs & Debug Info
# ----------------------------------------------------------------------


def safe_id(s: str) -> str:
    """Produce a short, display-friendly identifier for pytest parameter IDs."""
    return s.replace(" ", "_").replace("/", "_").replace(".", "_")[:30]


def create_test_parameters() -> list:
    """Create parameterized test cases with readable, unique names and debug context."""
    test_cases = []

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

    for key, expected_value in expected.items():
        actual_value = getattr(result, key)
        assert actual_value == expected_value, (
            f"Input: '{text}' - Expected {key}='{expected_value}', got '{actual_value}'"
        )

    # Confidence checks (only if precision provided)
    prec = expected.get("precision")
    if prec == "build":
        assert result.confidence >= 0.8, f"Input: '{text}' - build-level match should have high confidence"
    elif prec == "product":
        assert result.confidence >= 0.6
    elif prec == "family":
        assert result.confidence >= 0.4


# ----------------------------------------------------------------------
# Full OSData equality cases grouped by platform
# ----------------------------------------------------------------------

FULL_OBJECT_CASE_GROUPS: dict[str, list[tuple[str, dict | None, OSData]]] = {
    "windows": [
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
                kernel_version="6.1.7601",
                arch="x86",
                precision="build",
                confidence=0.85,
                evidence={"hit": "windows", "nt_version": "6.1", "service_pack": "SP2"},
            ),
        ),
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
                kernel_version="6.1.7601",
                arch="x86_64",
                precision="build",
                confidence=0.85,
                evidence={"hit": "windows", "nt_version": "6.1"},
            ),
        ),
    ],
    "macos": [
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
    ],
    "linux": [
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
    ],
    "network-os": [
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
    ],
    "mobile": [
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
    ],
    "bsd": [
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
    ],
}


def create_full_object_parameters() -> list:
    """Flatten grouped full-object cases into pytest parameters."""
    params = []
    for group, cases in FULL_OBJECT_CASE_GROUPS.items():
        for idx, (raw, data, expected) in enumerate(cases):
            params.append(
                pytest.param(
                    raw,
                    data,
                    expected,
                    id=f"full_{group}_{idx:02d}_{safe_id(raw)}",
                )
            )
    return params


@pytest.mark.parametrize(("text", "data", "expected"), create_full_object_parameters())
def test_full_osdata_objects(text: str, data: dict | None, expected: OSData) -> None:
    """Assert complete OSData objects for representative inputs."""
    result = normalize_os(text, data)
    assert result == expected
