import json

from aegir.api.validations import PDVKeyRequired, PDVFieldRequired, \
    PDVGeoJSONFieldValidation
from aegir.core import services
from aegir.core.exceptions import NotFound
from aegir.core.handlers import RequestHandler
from aegir.core.validations import (
    validate_request,
)


class PDV(RequestHandler):
    @validate_request(
        PDVKeyRequired,
        PDVFieldRequired(
            'tradingName', 'ownerName', 'document', 'coverageArea', 'address'
        ),
        PDVGeoJSONFieldValidation('coverageArea', 'address'),
    )
    async def post(self):
        pdvs = self.request.arguments['pdvs']

        created = await services.create_pdvs(pdvs)

        self.write(json.dumps({
            'created': created
        }))

    async def get(self):
        pdv_id = self.get_argument('id', None)
        lat = self.get_argument('lat', None)
        lng = self.get_argument('lng', None)

        if pdv_id:
            pdv = await services.get_pdv_by_id(pdv_id)
            if not pdv:
                raise NotFound(f'PDV with id "{pdv_id}" not found')

            self.write(pdv.as_dict)

        elif lat and lng:
            pdvs = await services.filter_pdv_by_lat_and_long(lat, lng)

            self.write({
                'pdvs': [pdv.as_dict for pdv in pdvs]
            })
