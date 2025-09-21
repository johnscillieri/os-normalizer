"""Tests for the OSData __str__ (and __repr__) formatting.

These tests instantiate OSData directly to validate formatting behavior,
independent of parsing logic.
"""

from os_normalizer import OSData


def test_str_windows_build():
    p = OSData(
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
    )
    assert str(p) == ("Microsoft Windows 11 build 22631 Enterprise (23H2) x86_64 [kernel: nt 10.0.22631] {build:0.85}")


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
    assert str(p) == ("Canonical Ubuntu 22.4.4 (LTS) x86_64 [kernel: linux 5.15.0-122-generic] {patch:0.80}")


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
