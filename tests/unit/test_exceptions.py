import re

import pytest

from pytest_playwright_enhanced.exceptions import PWEMarkerError


def test_browser_kwargs_err(request: pytest.FixtureRequest) -> None:
    expected = re.escape(
        rf"`@pytest.mark.marker` only supports keyword args. Test({request.node.name}) used args=(5000,)"
    )
    with pytest.raises(PWEMarkerError, match=expected):
        raise PWEMarkerError((5000,), "marker", request.node.name)
