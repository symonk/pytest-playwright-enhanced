import pytest


def test_can_overwrite_context_kwargs(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.fixture(scope='function')
        def context_arguments():
            return {'foo': 'bar'}

        def test_context_kwargs(context_arguments):
            assert context_arguments == {'foo': 'bar'}
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
