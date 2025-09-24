"""Shared helpers for OS normalization test fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Sequence


def safe_id(text: str) -> str:
    """Return a short, pytest-friendly identifier."""
    return text.replace(" ", "_").replace("/", "_").replace(".", "_")[:30]


def build_params(group: str, cases: Sequence[tuple[str, dict | None, object]]) -> list:
    """Create pytest parameters with stable IDs for a set of cases."""
    params: list = []
    for idx, (raw, data, expected) in enumerate(cases):
        params.append(
            pytest.param(
                raw,
                data,
                expected,
                id=f"{group}_{idx:03d}_{safe_id(raw)}",
            )
        )
    return params
