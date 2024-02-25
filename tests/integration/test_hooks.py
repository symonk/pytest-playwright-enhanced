import pytest


def test_binary_acquire_hook_fires(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--acquire-drivers")
    result.stdout.fnmatch_lines(["DOWNLOADING BINARIES!"])


def test_binary_acquisition_is_off_by_default(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest()
    result.stdout.no_fnmatch_lines(["DOWNLOADING BINARIES!"])
