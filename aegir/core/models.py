from geoalchemy2 import Geography
from sqlalchemy import Column, String, ForeignKey, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from aegir.core import parsers
from aegir.core.db import ModelBase


class Owner(ModelBase):
    __tablename__ = 'owner'

    id = Column(UUID(as_uuid=True), unique=True, nullable=False,
                primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(255), nullable=False)
    document = Column(String(18), unique=True, nullable=False)
    pdvs = relationship('PDV', back_populates="owner")

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
    public_id = Column(Integer, unique=True, nullable=False)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    owner = relationship('Owner', back_populates='pdvs')
    name = Column(String(255), nullable=False)
    address = Column(Geography(geometry_type='POINT', srid=4326),
                     nullable=False)
    coverage_area = Column(Geography(geometry_type='MULTIPOLYGON', srid=4326),
                           nullable=False)

    @property
    def as_dict(self):
        base = {'id': self.public_id}
        owner = self.owner.as_dict
        owner.pop('id', None)
        base.update(owner)
        base.update({
            'id': str(self.public_id),
            'tradingName': self.name,
            'coverageArea': parsers.to_geojson(self.coverage_area),
            'address': parsers.to_geojson(self.address)
        })
        return base
