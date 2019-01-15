from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base


ModelBase = declarative_base()

engine = create_engine('postgresql://postgres@localhost/aegir')

ModelBase.metadata.bind = engine

session = orm.scoped_session(orm.sessionmaker())(bind=engine)


__all__ = [
    ModelBase,
    engine,
    session,
]
