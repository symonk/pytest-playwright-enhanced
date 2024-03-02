import pytest


def test_can_overwrite_context_kwargs(pytester: pytest.Pytester) -> None:
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
