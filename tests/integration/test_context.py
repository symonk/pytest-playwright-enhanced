import pytest

pytestmark = pytest.mark.context


def test_context_kwargs_fixture_override(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.fixture(scope='function')
        def pw_context_args():
            return {'foo': 'bar'}

        def test_context_kwargs(pw_context_args):
            assert pw_context_args == {'foo': 'bar'}
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_context_kwargs_defaults(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_context_kwargs_defaults(pw_context_kwargs):
            expected = {}
            assert pw_context_kwargs == expected

""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_context_kwargs_marker_overrides(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest

        @pytest.mark.context_kwargs(accept_downloads=False)
        def test_override_context_kw(pw_context_kwargs) -> None:
            assert pw_context_kwargs == {'accept_downloads': False}
    """)
    pytester.runpytest().assert_outcomes(passed=1)


def test_context_kwargs_with_args_raises_pwe_error(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        @pytest.mark.context_kwargs(100, 200)
        def test_will_fail_with_raises_context_kwargs(pw_context_kwargs):
            ...
""")
    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    expected = "*pytest_playwright_enhanced.exceptions.PWEMarkerError: `@pytest.mark.context_kwargs` only supports keyword args. Test(test_will_fail_with_raises_context_kwargs*) used args=(100, 200)"
    result.stdout.fnmatch_lines([expected])
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_context_kwargs_dynamic_callback_is_merged(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest

        def cb(item):
            return {"item": item.name}

        @pytest.mark.context_kwargs(item="overridden", callback=cb)
        def test_merged_dynamic_callback(request, pw_context_kwargs):
            assert pw_context_kwargs['item'] == request.node.name
""")
    pytester.runpytest().assert_outcomes(passed=1)
