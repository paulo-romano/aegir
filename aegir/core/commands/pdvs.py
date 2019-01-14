import click


@click.group(
    help='PDVs related commands.'
)
def pdvs():
    pass


@pdvs.command(
    name='load'
)
def load():
    raise NotImplementedError('Command not implemented yet.')
