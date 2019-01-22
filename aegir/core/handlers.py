import json
import tornado

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
            message = 'Invalid request body.'
            self.send_error(400, message=message)

    def finish(self, chunk=None):
        """Log request finished status."""
        session.close()
        log.debug('SQLAlchemy session closed.')
        log.info(f'{self} request finished.')
        return super().finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Write error logging message if it exists in kwargs."""
        message = kwargs.get('message')
        if message:
            log.error(message)

        return super().write_error(status_code, **kwargs)


class MainHandler(RequestHandler):
    """Main handler used do verify if server start correctly."""
    async def get(self):
        self.write({'message': 'I am working...'})
