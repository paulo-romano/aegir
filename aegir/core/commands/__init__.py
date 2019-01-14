import click

from aegir.core.commands.shell import shell as shell_command
from aegir.core.commands.pdvs import pdvs as pdvs_group


@click.group()
def aegir_commands():
    pass


aegir_commands.add_command(shell_command)
aegir_commands.add_command(pdvs_group)

__all__ = [
    aegir_commands,
]
