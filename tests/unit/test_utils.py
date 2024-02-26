import pytest

from pytest_playwright_enhanced.utils import safe_to_run_plugin


def test_safe_to_run_plugin_help(pytestconfig: pytest.Config) -> None:
    pytestconfig.option.help = True
    pytestconfig.option.showfixtures = False
    pytestconfig.option.collectonly = False
    assert not safe_to_run_plugin(pytestconfig)


def test_safe_to_run_plugin_show_fixtures(pytestconfig: pytest.Config) -> None:
    pytestconfig.option.help = False
    pytestconfig.option.showfixtures = True
    pytestconfig.option.collectonly = False
    assert not safe_to_run_plugin(pytestconfig)


def test_safe_to_run_plugin_collection(pytestconfig: pytest.Config) -> None:
    pytestconfig.option.help = False
    pytestconfig.option.showfixtures = False
    pytestconfig.option.collectonly = True
    assert not safe_to_run_plugin(pytestconfig)


def test_safe_to_run_plugin(pytestconfig: pytest.Config) -> None:
    pytestconfig.option.help = False
    pytestconfig.option.showfixtures = False
    pytestconfig.option.collectonly = False
    assert safe_to_run_plugin(pytestconfig)
