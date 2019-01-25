import json

from aegir.core import services
from aegir.core.exceptions import NotFound
from aegir.core.handlers import RequestHandler


class PDV(RequestHandler):
    async def post(self):
        pdvs = self.request.arguments['pdvs']

        created = await services.create_pdvs(pdvs)

        self.write(json.dumps({
            'created': created
        }))

    async def get(self):
        pdv_id = self.get_argument('id')
        pdv = await services.get_pdv_by_id(pdv_id)
        if not pdv:
            raise NotFound(f'PDV with id "{pdv_id}" not found')

        self.write(pdv.as_dict)
