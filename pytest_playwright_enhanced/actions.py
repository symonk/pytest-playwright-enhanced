from __future__ import annotations

from argparse import Action
from argparse import ArgumentError
from argparse import Namespace

import pytest


class VideoAction(Action):
    """A Custom action that can accept either:
    yes, no or a custom widthXheight.
    """

    def __init__(
        self: VideoAction,
        option_strings: str,
        dest: str,
        nargs: str | None = None,
        **kwargs: dict,
    ) -> None:
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    # Todo: Tidy this implementation.
    def __call__(
        self: VideoAction,
        parser: pytest.Parser,  # noqa: ARG002
        namespace: Namespace,
        values: str,
        option_string: str | None = None,  # noqa: ARG002
    ) -> str:
        to_lower = values.lower()
        if to_lower in {"yes", "no"}:
            setattr(namespace, self.dest, to_lower)
            return
        if "x" in to_lower:
            # Attempt to parse a width by height.
            width, _, height = to_lower.partition("x")
            try:
                int(width)
                int(height)
                setattr(namespace, self.dest, to_lower)
                return
            except ValueError:
                raise ArgumentError(
                    self, "width x height option must both be valid integers"
                ) from None
        raise ArgumentError(
            self, "can only be 'yes', 'no' or a width x height string such as '800x640'"
        )
