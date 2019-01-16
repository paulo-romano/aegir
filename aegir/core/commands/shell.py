import click

from IPython import embed

from aegir.core.models import (
    Owner,
    PDV
)
from aegir.core.db import session


def get_user_ns():
    """Return object to be pre-imported by aegir shell."""
    return {
        'session': session,
        'Owner': Owner,
        'PDV': PDV
    }


def get_banners():
    """Return banners text to be presented in ipython banner."""
    return {
        'banner1': '::: Aegir Shell Tool :::\n',
        'banner2': 'Available Objects:\n'
                   '    - session: SQLAlchemy session.\n'
                   '\n'
                   'Available Models:\n'
                   '    - Owner\n'
                   '    - PDV\n'
    }


@click.command(
    name='shell',
    help='Execute a python interactive shell with Aegir context.'
)
def shell():
    embed(using=False, user_ns=get_user_ns(), **get_banners())
