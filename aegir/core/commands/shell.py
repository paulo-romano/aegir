import click

from IPython import embed


@click.command(
    name='shell',
    help='Execute a python interactive shell with Aegir context.'
)
def shell():
    embed()
