import pytest


@pytest.fixture
def mocked_sqlalchemy_session(mocker):
    return mocker.MagicMock()
