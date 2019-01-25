class AegirException(Exception):
    def __init__(self, status_code, message):
        super().__init__(status_code, message)


class BadRequest(AegirException):
    def __init__(self, message):
        super().__init__(400, message)
