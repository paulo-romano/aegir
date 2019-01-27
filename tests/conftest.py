import pytest


@pytest.fixture
def mocked_sqlalchemy_session(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mocked_coroutine_factory():
    """Create a mocked coroutine that return given value."""
    def mocked_coroutine(return_value):
        async def coroutine(*_args, **_kwargs):
            return return_value

        return coroutine
    return mocked_coroutine
