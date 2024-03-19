from __future__ import annotations

import pytest


def artifact_files(
    pytester: pytest.Pytester,
    extension: str,
    default_dir: str = "playwright-enhanced-results/",
) -> set[str]:
    """Returns a distinct list of the file names in the artifacts
    directory that match the file extension"""
    if not extension.startswith("."):
        extension = "." + extension
    p = pytester.path.joinpath(default_dir)
    return {f.name for f in p.glob(f"*{extension}")}
