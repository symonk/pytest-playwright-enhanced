import pytest


@pytest.mark.skip(reason="not implemented")
def test_binary_acquire_hook_fires(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest_inprocess("--acquire-drivers=yes")  # noqa F841
    # Todo: implement!


def test_binary_acquisition_is_off_by_default(pytester: pytest.Pytester) -> None:
    hook_recorder = pytester.inline_run()
    calls = hook_recorder.getcalls("pytest_playwright_acquire_binaries")
    assert not calls
