from __future__ import annotations

import pytest


def artifact_files(pytester: pytest.Pytester, extension: str) -> set[str]:
    """Returns a distinct list of the file names in the artifacts
    directory that match the file extension"""
    default_dir = "playwright-enhanced-results/"
    p = pytester.path.joinpath(default_dir)
    return {f.name for f in p.glob(f"*.{extension}")}
