import pathlib

import pytest


@pytest.mark.skip(reason="this is set in conftest.py globally now for test purposes")
def test_driver_path_not_set_if_omitted(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import os
        def test_not_set():
            assert "PLAYWRIGHT_BROWSERS_PATH" not in os.environ
"""
    )
    pytester.runpytest().assert_outcomes(passed=1)


def test_driver_download_host_not_set_if_omitted(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import os
        def test_not_set():
            assert "PLAYWRIGHT_DOWNLOAD_HOST" not in os.environ
"""
    )
    pytester.runpytest().assert_outcomes(passed=1)


def test_driver_path_set_if_provided(
    pytester: pytest.Pytester, tmp_path: pathlib.Path
) -> None:
    pytester.makepyfile(
        """
        import os
        def test_not_set():
            assert "PLAYWRIGHT_BROWSERS_PATH" in os.environ
"""
    )
    pytester.runpytest("--drivers-path", tmp_path).assert_outcomes(passed=1)


def test_driver_download_host_set_if_provided(
    pytester: pytest.Pytester, tmp_path: pathlib.Path
) -> None:
    pytester.makepyfile(
        """
        import os
        def test_not_set():
            assert "PLAYWRIGHT_DOWNLOAD_HOST" in os.environ
"""
    )
    pytester.runpytest("--download-host", tmp_path).assert_outcomes(passed=1)
