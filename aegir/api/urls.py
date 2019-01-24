from .handlers import PDV

url_patterns = [
    (r"^/api/pdv$", PDV),
]
