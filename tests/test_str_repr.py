"""Tests for the OSData __str__ (and __repr__) formatting.

These tests instantiate OSData directly to validate formatting behavior,
independent of parsing logic.
"""

from os_normalizer import OSData


def test_str_windows_11_build():
    p = OSData(
        family="windows",
        vendor="Microsoft",
        product="Windows 11",
        edition="Enterprise",
        version_major=10,
        version_minor=0,
        version_build="22631",
        kernel_name="nt",
        kernel_version="23H2",
        arch="x86_64",
        precision="build",
        confidence=0.85,
    )
    assert str(p) == "Microsoft Windows 11 Enterprise (23H2) 10.0.22631 x86_64"


def test_str_windows_7_build():
    p = OSData(
        family="windows",
        vendor="Microsoft",
        product="Windows 7",
        edition="Professional",
        version_major=6,
        version_minor=1,
        version_build="7600",
        kernel_name="nt",
        kernel_version="6.1",
        arch="x86_64",
        precision="build",
        confidence=0.85,
        evidence={"hit": "windows", "nt_version": "6.1"},
        os_key="cpe:2.3:o:microsoft:windows_7:6.1.7600:*:*:*:*:*:x64:*",
    )
    assert str(p) == "Microsoft Windows 7 Professional 6.1.7600 x86_64"


def test_str_linux_ubuntu_patch():
    p = OSData(
        family="linux",
        vendor="Canonical",
        product="Ubuntu",
        version_major=22,
        version_minor=4,
        version_patch=4,
        channel="LTS",
        kernel_name="linux",
        kernel_version="5.15.0-122-generic",
        arch="x86_64",
        precision="patch",
        confidence=0.8,
    )
    assert str(p) == "Canonical Ubuntu 22.4.4 (LTS) x86_64 [kernel: linux 5.15.0-122-generic] {patch:0.80}"


def test_str_macos_major_arm64():
    p = OSData(
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
    )
    assert str(p) == "Apple macOS 15 (Sequoia) arm64 [kernel: darwin 24.0.0] {major:0.70}"


def test_str_network_ios_xe_build():
    p = OSData(
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
    )
    assert str(p) == (
        "Cisco IOS XE 17.9.1 build 17.9.1a universalk9 (Amsterdam) "
        "[kernel: ios-xe] [hw: C9300-24T] "
        "[build: c9300-universalk9.17.9.1a.SPA.bin] {build:0.85}"
    )


def test_repr_delegates_to_str():
    p = OSData(vendor="Acme", product="WidgetOS", precision="product", confidence=0.6)
    # __repr__ is prefixed with OSData(...)
    assert repr(p).startswith("OSData(")
    assert "Acme WidgetOS" in repr(p)
