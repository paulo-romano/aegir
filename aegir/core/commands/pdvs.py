import asyncio
import json

import click

from aegir.core import services


@click.group(
    help='PDVs related commands.'
)
def pdvs():
    pass


@pdvs.command(
    name='load'
)
@click.argument('file_path')
def load(file_path):
    try:
        with open(file_path) as f:
            file_as_dict = json.load(f)

        pdvs_items = file_as_dict.get('pdvs')

        if pdvs_items:
            created = asyncio.run(services.create_pdvs(pdvs_items))
            print(f'Created PDVs: {len(created)}')
            if created:
                for id_ in created:
                    print(f'==> ID: {id_}')
    except Exception as ex:
        print(f'Error while creating PDVs. Exception {ex}')
