from aegir.core import parsers
from aegir.core.exceptions import ValidationError
from aegir.core.validations import RequestPayloadValidation


class PDVKeyRequired(RequestPayloadValidation):
    """Validate if PDVs key was informed in request body."""

    async def validate(self, payload):
        if not payload.get('pdvs'):
            raise ValidationError('PDVs key is required.')


class PDVFieldRequired(RequestPayloadValidation):
    """Validate if has field required errors."""

    def __init__(self, *fields):
        self._fields = fields
        super().__init__()

    async def validate(self, payload):
        messages = []
        pdvs = payload.get('pdvs', [])
        for pdv in pdvs:
            for field in self._fields:
                if field not in pdv.keys():
                    messages.append(f'PDV on position {pdvs.index(pdv)} '
                                    f'has no "{field}" field')

        if messages:
            raise ValidationError(messages)


class PDVGeoJSONFieldValidation(RequestPayloadValidation):
    """Validate if geojson field value is valid."""

    def __init__(self, *fields):
        self._fields = fields
        super().__init__()

    async def validate(self, payload):
        messages = []
        pdvs = payload.get('pdvs', [])
        for pdv in pdvs:
            for field in self._fields:
                try:
                    parsers.geojson_to_wkt(pdv[field])
                except Exception:
                    messages.append(f'PDV on position {pdvs.index(pdv)} '
                                    f'has no valid value for "{field}" field')

        if messages:
            raise ValidationError(messages)
