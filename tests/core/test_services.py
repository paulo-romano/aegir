import pytest

from aegir.core import services


class TestCreatePDVs:
    @pytest.mark.asyncio
    async def test_must_create_pdvs(
            self, mocker, mocked_sqlalchemy_session,
            mocked_coroutine_factory):

        expected_id = 'test_id'

        fake_pdv = mocker.MagicMock()
        fake_pdv.id = expected_id

        pdv_dict = mocker.MagicMock()

        pdvs = [pdv_dict]

        mocker.patch('aegir.core.services.session', mocked_sqlalchemy_session)

        mocker.patch(
            'aegir.core.repositories.PDVRepository'
            '.get_or_create_from_pdv_dict',
            mocked_coroutine_factory(fake_pdv)
        )

        assert expected_id in await services.create_pdvs(pdvs)
