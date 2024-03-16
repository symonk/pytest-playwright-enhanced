from pytest_playwright_enhanced.launch_kwargs_strategy import chromium_launch_strategy
from pytest_playwright_enhanced.launch_kwargs_strategy import firefox_launch_strategy
from pytest_playwright_enhanced.launch_kwargs_strategy import webkit_launch_strategy


def test_chrome_strategy_retains_chromium_sandbox() -> None:
    mapping = {"chromium_sandbox": True}
    assert chromium_launch_strategy(mapping) == mapping


def test_firefox_removes_chromium_sandbox() -> None:
    mapping = {"chromium_sandbox": True}
    assert firefox_launch_strategy(mapping) == {}


def test_webkit_strategy_removes_chromium_sandbox() -> None:
    mapping = {"chromium_sandbox": True}
    assert webkit_launch_strategy(mapping) == {}
