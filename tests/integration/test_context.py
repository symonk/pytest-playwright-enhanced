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


def test_context_kwargs_defaults(): ...  # noqa: ANN201


def test_context_kwargs_marker_overrides(): ...  # noqa: ANN201
