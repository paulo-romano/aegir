import click

from aegir.core.app import run


@click.command(
    name='runserver',
    help='Execute Aegir server.'
)
def runserver():
    run()
