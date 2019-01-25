from geoalchemy2 import Geography
from sqlalchemy import Column, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from aegir.core import parsers
from aegir.core.db import ModelBase
from aegir.core.exceptions import BadRequest


class Owner(ModelBase):
    __tablename__ = 'owner'

    id = Column(UUID(as_uuid=True), unique=True, nullable=False,
                primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(255), nullable=False)
    document = Column(String(18), unique=True, nullable=False)
    pdvs = relationship('PDV', back_populates="owner")

    @validates('name', 'document')
    def required(self, field, value):
        if not value:
            raise BadRequest(f'Field "{field}" is required.')

        return value

    @property
    def as_dict(self):
        return {
            'id': str(self.id),
            'ownerName': self.name,
            'document': self.document
        }


class PDV(ModelBase):
    __tablename__ = 'pdv'

    id = Column(UUID(as_uuid=True), unique=True, nullable=False,
                primary_key=True, server_default=text('gen_random_uuid()'))
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    owner = relationship('Owner', back_populates='pdvs')
    name = Column(String(255), nullable=False)
    address = Column(Geography(geometry_type='POINT', srid=4326),
                     nullable=False)
    coverage_area = Column(Geography(geometry_type='MULTIPOLYGON', srid=4326),
                           nullable=False)

    @validates('owner_id', 'name', 'address', 'coverage_area')
    def required(self, field, value):
        if not value:
            raise BadRequest(f'Field "{field}" is required.')

        return value

    @property
    async def as_dict(self):
        base = self.owner.as_dict
        base.pop('id', None)
        base.update({
            'id': str(self.id),
            'tradingName': self.name,
            'coverageArea': await parsers.to_geojson(self.coverage_area),
            'address': await parsers.to_geojson(self.address)
        })
        return base
