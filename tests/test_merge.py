"""Tests for merging and updating OSData objects."""

from os_normalizer import merge_os, normalize_os, update_os


def test_merge_linux_uname_then_os_release() -> None:
    uname = "Linux host 5.15.0-122-generic x86_64"
    osrel = {
        "os_release": 'NAME="Ubuntu"\nID=ubuntu\nVERSION_ID="22.04.4"\nVERSION_CODENAME=jammy\nPRETTY_NAME="Ubuntu 22.04.4 LTS"'
    }
    p_uname = normalize_os(uname)
    p_osrel = normalize_os(uname, osrel)

    merged = merge_os(p_uname, p_osrel)

    # Key expectations after merge
    assert merged.family == "linux"
    assert merged.vendor == "Canonical"
    assert merged.product == "Ubuntu"
    assert (merged.version_major, merged.version_minor, merged.version_patch) == (22, 4, 4)
    assert merged.channel == "LTS"
    assert merged.kernel_name == "linux"
    assert merged.kernel_version == "5.15.0-122-generic"
    assert merged.arch == "x86_64"
    assert merged.distro == "ubuntu"
    assert merged.codename == "Jammy"
    assert merged.pretty_name == "Ubuntu 22.04.4 LTS"
    assert merged.os_key == "cpe:2.3:o:canonical:ubuntu_linux:22.04:*:*:*:*:*:x64:*"


def test_update_os_inplace_linux() -> None:
    uname = "Linux node 6.5.7-arch1-1 x86_64"
    p = normalize_os(uname)
    assert p.product == "Linux"
    # Apply an os-release update for Fedora
    p2 = update_os(
        p,
        text=uname,
        data={"os_release": {"NAME": "Fedora Linux", "ID": "fedora", "VERSION_ID": "39"}},
        inplace=True,
    )
    assert p2 is p
    assert p.vendor == "Fedora Project"
    assert p.product == "Fedora Linux"
    assert p.version_major == 39
    assert p.distro == "fedora"
    assert p.os_key == "cpe:2.3:o:fedoraproject:fedora:39:*:*:*:*:*:x64:*"


def test_merge_windows_build_then_title() -> None:
    p1 = normalize_os("Windows NT 10.0 build 22631 Enterprise x64")
    p2 = normalize_os("Microsoft Windows 11 23h2 10.0.22631.2715 on x64")
    merged = merge_os(p1, p2)
    assert merged.product == "Windows 11"
    assert merged.channel is None
    assert merged.kernel_version == "23H2"
    assert merged.os_key == "cpe:2.3:o:microsoft:windows_11_23h2:10.0.22631.2715:*:*:*:*:*:x64:*"


def test_merge_macos_darwin_then_alias() -> None:
    # Darwin provides kernel + arch; alias text provides codename
    p1 = normalize_os("Darwin 24.0.0 arm64")
    p2 = normalize_os("macOS Sequoia")
    merged = merge_os(p1, p2)
    assert merged.vendor == "Apple"
    assert merged.product == "macOS"
    assert merged.version_major == 15
    assert merged.codename == "Sequoia"
    assert merged.kernel_name == "darwin"
    assert merged.kernel_version == "24.0.0"
    assert merged.arch == "arm64"
    assert merged.os_key == "cpe:2.3:o:apple:macos:15.0:*:*:*:*:*:arm64:*"


def test_merge_cisco_show_then_image() -> None:
    # Show output with version and model, separate image file reference
    show = "Cisco IOS XE Software, Version 17.9.1a (Amsterdam) C9300-24T, universalk9"
    image = "Cisco IOS XE image: c9300-universalk9.17.9.1a.SPA.bin"
    p1 = normalize_os(show)
    p2 = normalize_os(image)
    merged = merge_os(p1, p2)
    assert merged.vendor == "Cisco"
    assert merged.product == "IOS XE"
    assert merged.version_major == 17
    assert merged.version_minor == 9
    assert merged.version_build == "17.9.1a"
    assert merged.edition == "universalk9"
    assert merged.codename == "Amsterdam"
    assert "C9300" in (merged.hw_model or "").upper()
    assert merged.build_id == "c9300-universalk9.17.9.1a.SPA.bin"
    assert merged.os_key == "cpe:2.3:o:cisco:ios_xe:17.9.1a:*:universalk9:*:*:*:*:*"


def test_merge_juniper_version_then_pkg() -> None:
    vtext = "Junos: 20.4R3-S3"
    pkg = "Junos install pkg jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T"
    p1 = normalize_os(vtext)
    p2 = normalize_os(pkg)
    merged = merge_os(p1, p2)
    assert merged.vendor == "Juniper"
    assert merged.product == "Junos"
    assert merged.version_major == 20
    assert merged.version_minor == 4
    assert merged.version_build.lower() == "20.4r3-s3"
    assert merged.hw_model == "EX4300-48T"
    assert merged.build_id == "jinstall-ex-4300-20.4R3-S3.tgz"
    assert merged.os_key == "cpe:2.3:o:juniper:junos:20.4r3-s3:*:*:*:*:*:*:*"


def test_merge_fortinet_two_sources() -> None:
    show = "FortiGate-100F v7.2.7 build1600 (GA)"
    img = "FortiGate image FGT_7.2.7-build1600"
    p1 = normalize_os(show)
    p2 = normalize_os(img)
    merged = merge_os(p1, p2)
    assert merged.vendor == "Fortinet"
    assert merged.product == "FortiOS"
    assert (merged.version_major, merged.version_minor, merged.version_patch) == (7, 2, 7)
    assert merged.channel == "GA"
    assert merged.hw_model == "FG-100F"
    assert merged.build_id == "FGT_7.2.7-build1600"
    assert merged.os_key == "cpe:2.3:o:fortinet:fortios:7.2.7:*:*:*:*:*:*:*"


def test_merge_netgear_firmware_model() -> None:
    fw = "NETGEAR Firmware V1.0.9.88_10.2.88"
    mdl = "Netgear R7000"
    p1 = normalize_os(fw)
    p2 = normalize_os(mdl)
    merged = merge_os(p1, p2)
    assert merged.vendor == "Netgear"
    assert merged.product == "Firmware"
    assert merged.hw_model == "R7000"
    assert merged.version_build == "1.0.9.88_10.2.88"
    assert merged.os_key == "cpe:2.3:o:netgear:firmware:1.0.9.88_10.2.88:*:*:*:*:*:*:*"


def test_merge_debian_from_uname_and_os_release() -> None:
    uname = "Linux debian 6.1.0-18-amd64 x86_64"
    osrel = {
        "os_release": 'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="12"\nPRETTY_NAME="Debian GNU/Linux 12 (bookworm)"'
    }
    p1 = normalize_os(uname)
    p2 = normalize_os(uname, osrel)
    merged = merge_os(p1, p2)
    assert merged.vendor == "Debian"
    assert merged.product == "Debian GNU/Linux"
    assert merged.version_major == 12
    assert merged.distro == "debian"
    assert merged.kernel_version.startswith("6.1.0")
    assert merged.os_key == "cpe:2.3:o:debian:debian_linux:12:*:*:*:*:*:x64:*"


def test_merge_freebsd_arch_and_channel() -> None:
    v = "FreeBSD 13.2-RELEASE"
    arch = "FreeBSD 13.2 amd64"
    p1 = normalize_os(v)
    p2 = normalize_os(arch)
    merged = merge_os(p1, p2)
    assert merged.vendor == "FreeBSD"
    assert merged.product == "FreeBSD"
    assert merged.version_major == 13
    assert merged.version_minor == 2
    assert merged.channel == "RELEASE"
    assert merged.arch == "x86_64"
