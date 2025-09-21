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
]


@pytest.mark.parametrize(("text", "data", "expected"), build_params("mobile", MOBILE_OSDATA_CASES))
def test_mobile_normalize_os(text: str, data: dict | None, expected: OSData) -> None:
    """Ensure mobile inputs normalize into the expected OSData payloads."""
    result = normalize_os(text, data)
    assert result == expected
