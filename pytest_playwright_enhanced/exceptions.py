from __future__ import annotations

import typing


class PlaywrightEnhancedError(Exception):
    """Base class for all PWE exceptions."""


class PWEMarkerError(PlaywrightEnhancedError):
    """Raised when passing args to a PWE pytest marker, only keyword args are supported."""

    def __init__(
        self: PWEMarkerError, args: tuple[typing.Any, ...], marker: str, test: str
    ) -> None:
        super().__init__(
            f"`@pytest.mark.{marker}` only supports keyword args. Test({test}) used {args=}"
        )
