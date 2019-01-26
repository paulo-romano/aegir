from sqlalchemy import func

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
    async def create(self, public_id, owner, name, coverage_area, address):
        pdv = PDV(
            public_id=public_id,
            owner=owner,
            name=name,
            coverage_area=parsers.geojson_to_wkt(coverage_area),
            address=parsers.geojson_to_wkt(address),
        )
        self.session.add(pdv)
        self.session.flush()
        return pdv

    async def get_by_public_id(self, pdv_id):
        return self.session.query(PDV) \
            .filter_by(public_id=pdv_id) \
            .first()

    async def get_or_create_from_pdv_dict(self, pdv_dict):
        with OwnerRepository(self.session) as repo:
            owner = await repo.get_or_create_from_pdv_dict(pdv_dict)

        pdv = await self.get_by_public_id(
            pdv_dict.get('id')
        )

        if not pdv:
            pdv = await self.create(
                public_id=pdv_dict.get('id'),
                owner=owner,
                name=pdv_dict.get('tradingName'),
                coverage_area=pdv_dict.get('coverageArea'),
                address=pdv_dict.get('address'),
            )

        return pdv

    async def filter_pdv_by_lat_and_long(self, lat, lng):
        return self.session.query(PDV) \
            .filter(
                func.ST_Intersects(
                    func.Geometry(PDV.coverage_area),
                    func.Geometry(
                        func.ST_GeographyFromText(f'POINT({lat} {lng})')
                    )
                )
            ) \
            .all()
