from aegir.core.handlers import MainHandler
from aegir.api.urls import url_patterns as api_urls

url_patterns = [
    (r"^/$", MainHandler),
]

url_patterns += api_urls

__all__ = [
    'url_patterns',
]
