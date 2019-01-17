import tornado.httpserver
import tornado.ioloop
import tornado.web

from aegir import settings
from aegir.urls import url_patterns


class Application(tornado.web.Application):
    """Aegir application class."""

    def __init__(self):
        tornado.web.Application.__init__(
            self, url_patterns,
            debug=settings.DEBUG
        )


def run():
    """Run Aegir application server."""
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(settings.SERVER_PORT, settings.SERVER_ADDRESS)
    print(
        f'Server started at '
        f'http://{settings.SERVER_ADDRESS}:{settings.SERVER_PORT}'
    )

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
