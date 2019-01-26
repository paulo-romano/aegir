import json

import pytest

from aegir.core.exceptions import NotFound
from aegir.core.models import PDV as PDVModel
from aegir.api.handlers import PDV


class TestPDVPost:
    @pytest.mark.asyncio
    async def test_must_create_pdvs_from_body(
            self, mocker, mocked_sqlalchemy_session, mocked_coroutine_factory):

        expected_id = 'test_id'

        fake_pdv = mocker.MagicMock()
        fake_pdv.id = expected_id

        pdv_dict = mocker.MagicMock()

        pdvs = [pdv_dict]

        request = mocker.MagicMock()
        request.arguments = {'pdvs': pdvs}

        mocker.patch('aegir.core.services.session', mocked_sqlalchemy_session)

        mocker.patch(
            'aegir.core.repositories.PDVRepository'
            '.get_or_create_from_pdv_dict',
            mocked_coroutine_factory(fake_pdv)
        )

        mocked_write = mocker.patch('aegir.api.handlers.PDV.write')

        handler = PDV(application=mocker.MagicMock(), request=request)
        await handler.post()

        assert mocked_write.called is True
        assert mocker.call(json.dumps({
            'created': [expected_id]
        })) in mocked_write.call_args_list


class TestPDVGetByID:
    @pytest.mark.asyncio
    async def test_must_get_pdv_by_id(self, mocker, mocked_coroutine_factory):
        expected_pdv = PDVModel()

        mocker.patch(
            'aegir.core.services.get_pdv_by_id',
            mocked_coroutine_factory(expected_pdv)
        )

        mocker.patch('aegir.core.models.PDV.as_dict', {})

        mocked_get_argument = mocker.patch.object(PDV, 'get_argument')

        handler = PDV(mocker.MagicMock(), mocker.MagicMock())
        await handler.get()

        assert mocked_get_argument.called is True
        assert mocker.call('id', None) in mocked_get_argument.call_args_list

    @pytest.mark.asyncio
    async def test_must_rise_not_found_error(
            self, mocker, mocked_coroutine_factory):

        mocker.patch(
            'aegir.core.services.get_pdv_by_id',
            mocked_coroutine_factory(None)
        )

        mocker.patch.object(PDV, 'get_argument')

        handler = PDV(mocker.MagicMock(), mocker.MagicMock())
        with pytest.raises(NotFound):
            await handler.get()

    @pytest.mark.asyncio
    async def test_must_filter_by_lat_lng(
            self, mocker, mocked_coroutine_factory):
        expected_pdvs = [PDVModel()]

        mocker.patch(
            'aegir.core.services.filter_pdv_by_lat_and_long',
            mocked_coroutine_factory(expected_pdvs)
        )

        mocker.patch('aegir.core.models.PDV.as_dict', {})

        def new_get_argument(*args):
            return None if args[1] == 'id' else 1

        mocker.patch.object(PDV, 'get_argument', new_get_argument)

        mocked_write = mocker.patch.object(PDV, 'write')

        handler = PDV(mocker.MagicMock(), mocker.MagicMock())
        await handler.get()

        assert mocked_write.called is True
