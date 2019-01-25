import json
import tornado

from aegir.core.exceptions import BadRequest, AegirException
from aegir.core.utils import log
from aegir.core.db import session


class RequestHandler(tornado.web.RequestHandler):
    """Base request handle class used to pre configure handlers."""

    def __str__(self):
        return self.__class__.__name__

    def set_default_headers(self):
        """Set content type as application/json."""
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def prepare(self):
        """Parse request body to dict at request begin. """
        log.info(f'{self} request started.')

        try:
            if self.request.body:
                log.debug(f'{self} request body: {self.request.body}')

                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
        except Exception:
            raise BadRequest('Invalid request body.')

    def finish(self, chunk=None):
        """Log request finished status."""
        session.close()
        log.debug('SQLAlchemy session closed.')
        log.info(f'{self} request finished.')
        return super().finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Write error logging message if it exists in kwargs."""
        exc_info = kwargs.get('exc_info')
        if exc_info and issubclass(exc_info[0], AegirException):
            status_code = exc_info[1].args[0]
            message = exc_info[1].args[1]
        else:
            message = 'Unhandled error'

        self.set_status(status_code)
        return self.write({
            'error': message,
        })


class MainHandler(RequestHandler):
    """Main handler used do verify if server start correctly."""
    async def get(self):
        self.write({'message': 'I am working...'})
