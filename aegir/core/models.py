from geoalchemy2 import Geography
from sqlalchemy import Column, String, BigInteger, ForeignKey

from aegir.core.db import ModelBase


class Owner(ModelBase):
    __tablename__ = 'owner'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(String(18), unique=True, nullable=False)


class PDV(ModelBase):
    __tablename__ = 'pdv'

    id = Column(BigInteger, primary_key=True)
    owner = Column(ForeignKey('owner.id'), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Geography(geometry_type='POINT', srid=4326),
                     nullable=False)
    coverage_area = Column(Geography(geometry_type='MULTIPOLYGON', srid=4326),
                           nullable=False)
