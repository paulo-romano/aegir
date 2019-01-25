import json

import pytest

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
