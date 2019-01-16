import click

from aegir.core.commands.shell import shell as shell_command
from aegir.core.commands.pdvs import pdvs as pdvs_group
from aegir.core.commands.db import db as db_group
from aegir.core.commands.runserver import runserver as runserver_command


@click.group()
def aegir_commands():
    pass


aegir_commands.add_command(shell_command)
aegir_commands.add_command(pdvs_group)
aegir_commands.add_command(db_group)
aegir_commands.add_command(runserver_command)

__all__ = [
    aegir_commands,
]
