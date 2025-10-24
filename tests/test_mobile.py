"""Mobile OS normalization tests."""

import pytest

from os_normalizer import OSData, normalize_os
from tests.case_utils import build_params

MOBILE_OSDATA_CASES = [
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
            os_key="cpe:2.3:o:google:android:14:*:*:*:*:*:*:*",
        ),
    ),
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
            os_key="cpe:2.3:o:apple:iphone_os:17.5.1:*:*:*:*:*:*:*",
        ),
    ),
    (
        "iPadOS 16.7.6",
        None,
        OSData(
            family="ios",
            vendor="Apple",
            product="iOS/iPadOS",
            version_major=16,
            version_minor=7,
            version_patch=6,
            precision="patch",
            confidence=0.8,
            evidence={"hit": "ios"},
            os_key="cpe:2.3:o:apple:iphone_os:16.7.6:*:*:*:*:*:*:*",
        ),
    ),
    # Legacy generator coverage (mobile)
    (
        "Android 13",
        None,
        OSData(
            family="android",
            vendor="Google",
            product="Android",
            version_major=13,
            precision="major",
            confidence=0.7,
            evidence={"hit": "android"},
            os_key="cpe:2.3:o:google:android:13:*:*:*:*:*:*:*",
        ),
    ),
    (
        "Android 12.1",
        None,
        OSData(
            family="android",
            vendor="Google",
            product="Android",
            version_major=12,
            version_minor=1,
            precision="minor",
            confidence=0.75,
            evidence={"hit": "android"},
            os_key="cpe:2.3:o:google:android:12.1:*:*:*:*:*:*:*",
        ),
    ),
    (
        "HarmonyOS 4.2.0",
        None,
        OSData(
            family="harmonyos",
            vendor="Huawei",
            product="HarmonyOS",
            version_major=4,
            version_minor=2,
            version_patch=0,
            precision="patch",
            confidence=0.8,
            evidence={"hit": "harmonyos"},
            os_key="cpe:2.3:o:huawei:harmonyos:4.2.0:*:*:*:*:*:*:*",
        ),
    ),
    (
        "Huawei HARMONYOS 5.0.0.107 SP8",
        None,
        OSData(
            family="harmonyos",
            vendor="Huawei",
            product="HarmonyOS",
            version_major=5,
            version_minor=0,
            version_patch=0,
            version_build="107",
            precision="build",
            confidence=0.85,
            evidence={"hit": "harmonyos"},
            os_key="cpe:2.3:o:huawei:harmonyos:5.0.0:107:*:*:*:*:*:*:*",
        ),
    ),
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("mobile", MOBILE_OSDATA_CASES))
def test_mobile_normalize_os(text: str, data: dict | None, expected: OSData) -> None:
    """Ensure mobile inputs normalize into the expected OSData payloads."""
    result = normalize_os(text, data)
    assert result == expected
