"""BSD normalization tests."""

import pytest

from os_normalizer import OSData, normalize_os
from tests.case_utils import build_params

BSD_OSDATA_CASES = [
    (
        "FreeBSD 12.4-RELEASE",
        None,
        OSData(
            family="bsd",
            vendor="FreeBSD",
            product="FreeBSD",
            channel="RELEASE",
            version_major=12,
            version_minor=4,
            kernel_name="freebsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
            os_key="cpe:2.3:o:freebsd:freebsd:12.4:*:*:*:*:*:*:*",
        ),
    ),
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
            os_key="cpe:2.3:o:openbsd:openbsd:7.5:*:*:*:*:*:*:*",
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
            channel="RC1",
            version_major=13,
            version_minor=2,
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
            channel="STABLE",
            version_major=13,
            version_minor=3,
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
            channel="CURRENT",
            version_major=7,
            version_minor=6,
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
            channel="BETA",
            version_major=10,
            version_minor=0,
            kernel_name="netbsd",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
        ),
    ),
    (
        "FreeBSD host with os-release",
        {
            "os_release": 'NAME="FreeBSD"\nVERSION="13.2-RELEASE"\nID=freebsd\nVERSION_ID="13.2"\nID_LIKE="freebsd"\nPRETTY_NAME="FreeBSD 13.2-RELEASE"'
        },
        OSData(
            family="bsd",
            vendor="FreeBSD",
            product="FreeBSD",
            channel="RELEASE",
            version_major=13,
            version_minor=2,
            kernel_name="freebsd",
            like_distros=["freebsd"],
            distro="freebsd",
            pretty_name="FreeBSD 13.2-RELEASE",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
            os_key="cpe:2.3:o:freebsd:freebsd:13.2:*:*:*:*:*:*:*",
        ),
    ),
    (
        "OpenBSD os-release with codename",
        {
            "os_release": 'NAME="OpenBSD"\nVERSION="7.5"\nID=openbsd\nVERSION_ID="7.5"\nVERSION_CODENAME=song\nPRETTY_NAME="OpenBSD 7.5 (Song)"'
        },
        OSData(
            family="bsd",
            vendor="OpenBSD",
            product="OpenBSD",
            codename="Song",
            version_major=7,
            version_minor=5,
            kernel_name="openbsd",
            distro="openbsd",
            pretty_name="OpenBSD 7.5 (Song)",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
            os_key="cpe:2.3:o:openbsd:openbsd:7.5:*:*:*:*:*:*:*",
        ),
    ),
    (
        "NetBSD os-release stable train",
        {
            "os_release": 'NAME="NetBSD"\nVERSION="10.0_STABLE"\nID=netbsd\nVERSION_ID="10.0"\nPRETTY_NAME="NetBSD 10.0_STABLE"'
        },
        OSData(
            family="bsd",
            vendor="NetBSD",
            product="NetBSD",
            channel="STABLE",
            version_major=10,
            version_minor=0,
            kernel_name="netbsd",
            distro="netbsd",
            pretty_name="NetBSD 10.0_STABLE",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "bsd"},
            os_key="cpe:2.3:o:netbsd:netbsd:10.0:*:*:*:*:*:*:*",
        ),
    ),
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("bsd", BSD_OSDATA_CASES))
def test_bsd_normalize_os(text: str, data: dict | None, expected: OSData) -> None:
    """Ensure bsd inputs normalize into the expected OSData payloads."""
    result = normalize_os(text, data)
    assert result == expected
