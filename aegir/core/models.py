from geoalchemy2 import Geography
from sqlalchemy import Column, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID

from aegir.core.db import ModelBase


class Owner(ModelBase):
    __tablename__ = 'owner'

    id = Column(UUID(as_uuid=True), unique=True, nullable=False,
                primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(255), nullable=False)
    document = Column(String(18), unique=True, nullable=False)


class PDV(ModelBase):
    __tablename__ = 'pdv'

    id = Column(UUID(as_uuid=True), unique=True, nullable=False,
                primary_key=True, server_default=text('gen_random_uuid()'))
    owner = Column(ForeignKey('owner.id'), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Geography(geometry_type='POINT', srid=4326),
                     nullable=False)
    coverage_area = Column(Geography(geometry_type='MULTIPOLYGON', srid=4326),
                           nullable=False)
