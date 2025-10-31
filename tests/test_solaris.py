"""Solaris normalization tests."""

import pytest

from os_normalizer import OSData, normalize_os
from tests.case_utils import build_params

SOLARIS_CASES = [
    (
        "SunOS sol11-prod 5.11 11.4.0.15.0 i86pc i386 i86pc",
        {},
        OSData(
            family="solaris",
            vendor="Oracle",
            product="Oracle Solaris",
            version_major=11,
            version_minor=4,
            version_patch=0,
            version_build="15.0",
            kernel_name="sunos",
            kernel_version="5.11",
            arch="x86",
            precision="build",
            confidence=0.85,
            evidence={"hit": "solaris"},
            os_key="cpe:2.3:o:oracle:solaris:11.4.0:15.0:*:*:*:*:x86:*",
        ),
    ),
    (
        "Oracle Solaris 11.3 SPARC\nSunOS sparc-lab 5.11 11.3 sun4v sparc sun4v",
        {},
        OSData(
            family="solaris",
            vendor="Oracle",
            product="Oracle Solaris",
            version_major=11,
            version_minor=3,
            kernel_name="sunos",
            kernel_version="5.11",
            arch="sparc",
            precision="minor",
            confidence=0.75,
            evidence={"hit": "solaris"},
            os_key="cpe:2.3:o:oracle:solaris:11.3:*:*:*:*:*:sparc:*",
        ),
    ),
    (
        "SunOS legacy10 5.10 Generic_150400-64 sun4u sparc SUNW,Sun-Fire-V490",
        {},
        OSData(
            family="solaris",
            vendor="Oracle",
            product="Oracle Solaris",
            version_major=10,
            version_build="150400-64",
            kernel_name="sunos",
            kernel_version="5.10",
            arch="sparc",
            precision="build",
            confidence=0.85,
            evidence={"hit": "solaris"},
            os_key="cpe:2.3:o:oracle:solaris:10:150400-64:*:*:*:*:*:sparc:*",
        ),
    ),
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("solaris", SOLARIS_CASES))
def test_solaris_normalization(text: str, data: dict | None, expected: OSData) -> None:
    result = normalize_os(text, data)
    assert result == expected
