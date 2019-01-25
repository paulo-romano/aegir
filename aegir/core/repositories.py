from aegir.core import parsers
from aegir.core.models import Owner, PDV
from aegir.core.utils import log


class Repository:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
            log.debug('Work commited.')
        except Exception:
            log.exception('Error while commit work.')
            self.session.rollback()


class OwnerRepository(Repository):
    async def create(self, name, document):
        owner = Owner(name=name, document=document)
        self.session.add(owner)
        self.session.flush()
        return owner

    async def get_by_document(self, document):
        return self.session.query(Owner).filter_by(document=document).first()

    async def get_or_create_from_pdv_dict(self, pdv_dict):
        owner = await self.get_by_document(document=pdv_dict.get('document'))
        if not owner:
            owner = await self.create(
                pdv_dict.get('ownerName'), pdv_dict.get('document')
            )

        return owner


class PDVRepository(Repository):
    async def create(self, owner, name, coverage_area, address):
        pdv = PDV(
            owner=owner,
            name=name,
            coverage_area=await parsers.geojson_to_wkt(coverage_area),
            address=await parsers.geojson_to_wkt(address),
        )
        self.session.add(pdv)
        self.session.flush()
        return pdv

    async def create_from_pdv_dict(self, pdv_dict):
        with OwnerRepository(self.session) as repo:
            owner = await repo.get_or_create_from_pdv_dict(pdv_dict)

        pdv = await self.create(
            owner=owner,
            name=pdv_dict.get('tradingName'),
            coverage_area=pdv_dict.get('coverageArea'),
            address=pdv_dict.get('address'),
        )

        return pdv
