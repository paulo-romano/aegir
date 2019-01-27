import logging
from tornado.log import enable_pretty_logging


def configure_log():
    enable_pretty_logging()


log = logging.getLogger("tornado.application")

__all__ = [
    'log',
    'configure_log',
]
