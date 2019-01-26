import pytest

from aegir.core import services
from aegir.core.models import PDV


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


class TestGetPDVByID:
    @pytest.mark.asyncio
    async def test_must_get_pdv_by_id(self, mocker, mocked_coroutine_factory):
        pdv_id = 'fake_id'
        expected_pdv = PDV()
        mocker.patch(
            'aegir.core.repositories.PDVRepository.get_by_id',
            mocked_coroutine_factory(expected_pdv)
        )

        pdv = await services.get_pdv_by_id(pdv_id)

        assert pdv == expected_pdv

    @pytest.mark.asyncio
    async def test_must_filter_by_lat_lng(
            self, mocker, mocked_coroutine_factory):
        lat = 1
        lng = 1
        expected_pdvs = [PDV()]
        mocker.patch(
            'aegir.core.repositories.PDVRepository.filter_pdv_by_lat_and_long',
            mocked_coroutine_factory(expected_pdvs)
        )

        pdv = await services.filter_pdv_by_lat_and_long(lat, lng)

        assert pdv == expected_pdvs
