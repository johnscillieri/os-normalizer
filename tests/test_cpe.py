"""Tests for CPE 2.3 generation via OSData.os_key."""

from os_normalizer import normalize_os


def test_cpe_windows_11_with_channel():
    text = "Windows NT 10.0 build 22631 Enterprise x64"
    p = normalize_os(text)
    # Expect product to include channel and version to reflect kernel+build; target_hw maps to x64
    assert p.os_key == "cpe:2.3:o:microsoft:windows_11_23h2:10.0.22631:*:*:*:*:*:x64:*"


def test_cpe_windows_11_from_cpe_title():
    text = "Microsoft Windows 11 22h2 10.0.22621.2715 on x64"
    p = normalize_os(text)
    assert p.os_key == "cpe:2.3:o:microsoft:windows_11_22h2:10.0.22621.2715:*:*:*:*:*:x64:*"


def test_cpe_ubuntu_22_04_lts():
    text = "Linux host 5.15.0-122-generic x86_64"
    data = {
        "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"',
    }
    p = normalize_os(text, data)
    assert p.os_key == "cpe:2.3:o:canonical:ubuntu_linux:22.04:*:*:*:*:*:x64:*"


def test_cpe_macos_15_sequoia():
    text = "Darwin 24.0.0; macOS Sequoia arm64"
    p = normalize_os(text)
    assert p.os_key == "cpe:2.3:o:apple:macos:15.0:*:*:*:*:*:arm64:*"


def test_cpe_cisco_ios_xe():
    text = (
        "Cisco IOS XE Software, Version 17.9.1a (Amsterdam) C9300-24T, universalk9, c9300-universalk9.17.9.1a.SPA.bin"
    )
    p = normalize_os(text)
    assert p.os_key == "cpe:2.3:o:cisco:ios_xe:17.9.1a:*:universalk9:*:*:*:*:*"


def test_cpe_juniper_junos():
    text = "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T"
    p = normalize_os(text)
    assert p.os_key == "cpe:2.3:o:juniper:junos:20.4r3-s3:*:*:*:*:*:*:*"


def test_cpe_fortinet_fortios():
    text = "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600"
    p = normalize_os(text)
    assert p.os_key == "cpe:2.3:o:fortinet:fortios:7.2.7:*:*:*:*:*:*:*"
