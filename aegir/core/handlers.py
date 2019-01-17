import logging
import json
import tornado


class RequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def prepare(self):
        logging.info(f'{self} request started.')

        try:
            if self.request.body:
                logging.debug(f'{self} request body: {self.request.body}')

                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
        except Exception:
            message = 'Invalid request body.'
            self.send_error(400, message=message)

    def finish(self, chunk=None):
        logging.info(f'{self} request finished.')
        return super().finish(chunk)

    def write_error(self, status_code, **kwargs):
        message = kwargs.get('message')
        if message:
            logging.error(message)

        return super().write_error(status_code, **kwargs)


class MainHandler(RequestHandler):
    async def get(self):
        self.write({'message': 'I am working...'})
