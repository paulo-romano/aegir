from aegir.api.urls import url_patterns
from aegir.api.handlers import PDV


class TestAPIUrls:
    def test_must_contains_pdv_handle(self):

        index_url = list(
            filter(lambda item: item[0] == r"^/api/pdv$", url_patterns)
        )[0]
        assert index_url[1] == PDV
