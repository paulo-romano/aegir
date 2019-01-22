import json
import tornado

import pytest

from aegir.core.handlers import RequestHandler


class TestRequestHandler:
    """Aegir core RequestHandler tests."""

    def test_headers_must_be_json_utf8(self, mocker):
        set_header = mocker.patch.object(RequestHandler, 'set_header')

        handler = RequestHandler(mocker.MagicMock(), mocker.MagicMock())
        handler.set_default_headers()

        assert set_header.called is True
        assert mocker.call(
            'Content-Type',
            'application/json; charset=UTF-8'
        ) in set_header.call_args_list

    def test_prepare_must_set_request_arguments(self, mocker):
        body = '{"message": "ok"}'
        request = mocker.MagicMock()
        request.body = body
        json_data = {'message': 'ok'}

        json_loads = mocker.patch('json.loads', return_value=json_data)

        handler = RequestHandler(mocker.MagicMock(), request)
        handler.prepare()

        assert json_loads.called is True
        assert mocker.call(body) in json_loads.call_args_list

        assert request.arguments.update.called is True
        assert mocker.call(json_data) in \
            request.arguments.update.call_args_list

    @pytest.mark.parametrize('body', (
        None,
        '',
        [],
    ))
    def test_prepare_must_not_set_request_arguments(self, body, mocker):
        request = mocker.MagicMock()
        request.body = body

        handler = RequestHandler(mocker.MagicMock(), request)
        handler.prepare()

        assert request.arguments.update.called is False

    @pytest.mark.parametrize('ex_class', (
        Exception,
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ))
    def test_prepare_must_send_error_if_has_parse_exception(
            self, ex_class, mocker):
        request = mocker.MagicMock()
        request.body = '{"message": "ok"}'

        json_loads = mocker.patch('json.loads', side_effect=ex_class)

        send_error = mocker.patch.object(RequestHandler, 'send_error')

        handler = RequestHandler(mocker.MagicMock(), request)
        handler.prepare()

        assert json_loads.called is True

        assert send_error.called is True
        assert mocker.call(400, message='Invalid request body.') in \
            send_error.call_args_list

    def test_write_error_must_log_message(self, mocker):
        message = 'Wrong side of haven'
        status_code = 500
        logging_error = mocker.patch('aegir.core.utils.log.error')

        super_write_error = \
            mocker.patch.object(tornado.web.RequestHandler, 'write_error')

        handler = RequestHandler(mocker.MagicMock(), mocker.MagicMock())
        handler.write_error(status_code, message=message)

        assert logging_error.called is True
        assert mocker.call(message) in logging_error.call_args_list

        assert super_write_error.called is True
        assert mocker.call(status_code, message=message) in \
            super_write_error.call_args_list

    def test_finish_must_close_sqlalchemy_session(self, mocker):
        mocked_session = \
            mocker.patch('aegir.core.handlers.session', mocker.MagicMock())

        mocker.patch('tornado.web.RequestHandler.flush')

        mocked_log = mocker.patch('aegir.core.handlers.log')

        handler = RequestHandler(mocker.MagicMock(), mocker.MagicMock())
        handler.finish()

        assert mocked_session.close.called is True
        assert mocked_log.debug.called is True
        assert mocker.call('SQLAlchemy session closed.') \
            in mocked_log.debug.call_args_list
