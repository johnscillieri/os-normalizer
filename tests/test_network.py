"""Network OS normalization tests."""

import pytest

from os_normalizer import OSData, normalize_os
from tests.case_utils import build_params

NETWORK_OSDATA_CASES = [
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
            os_key="cpe:2.3:o:cisco:ios_xe:17.9.1a:*:universalk9:*:*:*:*:*",
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
            os_key="cpe:2.3:o:cisco:nx-os:9.3\\(5\\):*:*:*:*:*:*:*",
        ),
    ),
    (
        "Junos: 20.4R3-S3 jinstall-ex-4300-20.4R3-S3.tgz EX4300-48T",
        None,
        OSData(
            family="network-os",
            vendor="Juniper",
            product="Junos",
            version_major=20,
            version_minor=4,
            version_build="20.4R3-S3",
            kernel_name="junos",
            hw_model="EX4300-48T",
            build_id="jinstall-ex-4300-20.4R3-S3.tgz",
            precision="build",
            confidence=0.85,
            evidence={"hit": "network-os", "version_raw": "20.4R3-S3"},
            os_key="cpe:2.3:o:juniper:junos:20.4r3-s3:*:*:*:*:*:*:*",
        ),
    ),
    (
        "FortiGate-100F v7.2.7 build1600 (GA) FGT_7.2.7-build1600",
        None,
        OSData(
            family="network-os",
            vendor="Fortinet",
            product="FortiOS",
            channel="GA",
            version_major=7,
            version_minor=2,
            version_patch=7,
            version_build="7.2.7+build.1600",
            kernel_name="fortios",
            hw_model="FG-100F",
            build_id="FGT_7.2.7-build1600",
            precision="build",
            confidence=0.85,
            evidence={"hit": "network-os"},
            os_key="cpe:2.3:o:fortinet:fortios:7.2.7:*:*:*:*:*:*:*",
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
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("network", NETWORK_OSDATA_CASES))
def test_network_normalize_os(text: str, data: dict | None, expected: OSData) -> None:
    """Ensure network inputs normalize into the expected OSData payloads."""
    result = normalize_os(text, data)
    assert result == expected
