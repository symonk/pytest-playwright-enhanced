from pytest_playwright_enhanced import PlaywrightPageMixin


def test_playwright_page_mixin() -> None:
    class Foo(PlaywrightPageMixin): ...

    assert isinstance(Foo(), PlaywrightPageMixin)
