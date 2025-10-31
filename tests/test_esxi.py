"""VMware ESXi normalization tests."""

import pytest

from os_normalizer import OSData, normalize_os
from tests.case_utils import build_params

ESXI_CASES = [
    (
        "VMkernel esx-prod03 7.0.3 #20842708 SMP Release build-20842708 Oct 24 2023 03:17:39 x86_64 x86_64 x86_64",
        {},
        OSData(
            family="esxi",
            vendor="VMware",
            product="VMware ESXi",
            version_major=7,
            version_minor=0,
            version_patch=3,
            version_build="20842708",
            kernel_name="vmkernel",
            kernel_version="7.0.3",
            arch="x86_64",
            precision="build",
            confidence=0.85,
            evidence={"hit": "esxi"},
            os_key="cpe:2.3:o:vmware:esxi:7.0.3:20842708:*:*:*:*:x64:*",
        ),
    ),
    (
        "VMware ESXi 8.0.1 build-22088125",
        {},
        OSData(
            family="esxi",
            vendor="VMware",
            product="VMware ESXi",
            version_major=8,
            version_minor=0,
            version_patch=1,
            version_build="22088125",
            kernel_name="vmkernel",
            kernel_version="8.0.1",
            precision="build",
            confidence=0.85,
            evidence={"hit": "esxi"},
            os_key="cpe:2.3:o:vmware:esxi:8.0.1:22088125:*:*:*:*:*:*",
        ),
    ),
    (
        "Product: VMware ESXi\nVersion: 7.0.3\nBuild: 20842708\nUpdate: 3",
        {},
        OSData(
            family="esxi",
            vendor="VMware",
            product="VMware ESXi",
            version_major=7,
            version_minor=0,
            version_patch=3,
            version_build="20842708",
            kernel_name="vmkernel",
            kernel_version="7.0.3",
            channel="Update 3",
            precision="build",
            confidence=0.85,
            evidence={"hit": "esxi"},
            os_key="cpe:2.3:o:vmware:esxi:7.0.3:20842708:*:*:*:*:*:*",
        ),
    ),
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("esxi", ESXI_CASES))
def test_esxi_normalization(text: str, data: dict | None, expected: OSData) -> None:
    result = normalize_os(text, data)
    assert result == expected
