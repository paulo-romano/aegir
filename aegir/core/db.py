from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base

from aegir import settings

ModelBase = declarative_base()

engine = create_engine(
    f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
    f'@{settings.POSTGRES_HOST}/{settings.POSTGRES_DATABASE}'
)

ModelBase.metadata.bind = engine

session = orm.scoped_session(orm.sessionmaker())(bind=engine)


__all__ = [
    'ModelBase',
    'engine',
    'session',
]
