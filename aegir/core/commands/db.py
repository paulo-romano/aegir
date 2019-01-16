import click
from sqlalchemy import create_engine

from aegir import settings
from aegir.core.db import ModelBase


@click.group(
    help='Database related commands.'
)
def db():
    pass


def make_engine(database=''):
    return create_engine(f'postgresql://postgres@localhost/{database}',
                         echo=False)


def create_database():
    """Create database with given name."""
    engine = make_engine()
    conn = engine.connect()
    conn.connection.connection.set_isolation_level(0)
    conn.execute(f'create database {settings.POSTGRES_DATABASE}')
    conn.connection.connection.set_isolation_level(1)
    conn.close()


def create_database_extensions():
    engine = make_engine(settings.POSTGRES_DATABASE)
    conn = engine.connect()
    conn.execute('CREATE EXTENSION postgis')
    conn.execute('CREATE EXTENSION pgcrypto')
    conn.close()


@db.command(
    name='create'
)
def create():
    create_database()
    create_database_extensions()
    ModelBase.metadata.create_all(make_engine(settings.POSTGRES_DATABASE))
    print('Database created.')
