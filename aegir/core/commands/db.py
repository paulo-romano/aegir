import click
from sqlalchemy import create_engine

from aegir.core.db import ModelBase


@click.group(
    help='Database related commands.'
)
def db():
    pass


def make_engine(database=''):
    return create_engine(f'postgresql://postgres@localhost/{database}',
                         echo=False)


def create_database(name='aegir'):
    """Create database with given name."""
    engine = make_engine()
    conn = engine.connect()
    conn.connection.connection.set_isolation_level(0)
    conn.execute(f'create database {name}')
    conn.connection.connection.set_isolation_level(1)
    conn.close()


def create_database_extensions():
    engine = make_engine('aegir')
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
    ModelBase.metadata.create_all(make_engine('aegir'))
    print('Database created.')
