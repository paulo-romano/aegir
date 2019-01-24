from aegir.core.handlers import MainHandler


class TestCoreUrl:
    def test_index_url_must_be_main_handler(self):
        from aegir.urls import url_patterns

        index_url = list(
            filter(lambda item: item[0] == r"^/$", url_patterns)
        )[0]
        assert index_url[1] == MainHandler
