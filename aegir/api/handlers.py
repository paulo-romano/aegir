import json

from aegir.core import services
from aegir.core.handlers import RequestHandler


class PDV(RequestHandler):
    async def post(self):
        pdvs = self.request.arguments['pdvs']

        created = await services.create_pdvs(pdvs)

        self.write(json.dumps({
            'created': created
        }))
