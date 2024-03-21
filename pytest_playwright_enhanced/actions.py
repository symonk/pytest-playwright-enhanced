from __future__ import annotations

from argparse import Action
from argparse import ArgumentError
from argparse import Namespace

import pytest


class VideoAction(Action):
    """A Custom action that can accept either:
    yes, no or a custom widthXheight.
    """

    def __call__(
        self: VideoAction,
        parser: pytest.Parser,  # noqa: ARG002
        namespace: Namespace,
        values: str,
        option_string: list[str],  # noqa: ARG002
    ) -> str:
        video_action = values.lower()
        if video_action not in {"yes", "no"} and "x" not in video_action:
            raise ArgumentError(
                self,
                "can only be 'yes', 'no' or a width x height string such as '800x640'",
            )
        if "x" in video_action:
            width, _, height = video_action.partition("x")
            try:
                int(width), int(height)
            except ValueError:
                raise ArgumentError(
                    self, "width x height option must both be valid integers"
                ) from None

        setattr(namespace, self.dest, video_action)
